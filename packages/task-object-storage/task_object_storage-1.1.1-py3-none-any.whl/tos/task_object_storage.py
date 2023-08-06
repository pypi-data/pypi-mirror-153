"""
Task Object Storage module.

Note that this module has no Robot Framework dependencies, i.e. can be used with
pure Python applications.
"""
import atexit
import re

import pymongo
import pymongo.errors

from tos.components import creators, finders, setters, updaters
from tos.settings import DEFAULT_DB_ADDRESS


def _validate_collection_name(collection):
    """Validate collection name.
    Name should conform to regex: [0-9a-z_.]
    """
    regex = r"^[0-9a-z_.]*$"
    match = re.search(regex, collection)
    if collection and match:
        return True
    return False


class TaskObjectStorage(
    creators.TaskCreators,
    finders.TaskFinders,
    setters.TaskSetters,
    updaters.TaskUpdaters,
):
    def __init__(self, **options):
        """
        :param options: A dictionary of MongoDB options for the
         database server URL and port, and the process database
         name, username and password.

        The following is a list of accepted options as keyword arguments:

        :param db_server: Mongodb server uri and optional port, e.g. 'localhost:27017'
        :type db_server: str
        :param db_name: Database name.
        :type db_name: str
        :param db_user: Database username.
        :type db_user: str
        :param db_passw: Database password.
        :type db_passw: str
        :param db_auth_source: Authentication database.
        :type db_auth_source: str

        Example usage:

        .. code-block:: python

            tos = TaskObjectStorage(
                    db_server="localhost:27017",
                    db_name="testing",
                    db_auth_source="admin",
                    db_user="robo-user",
                    db_passw="secret-word",
            )
            tos.initialize_tos()

        where ``db_auth_source`` is the same as ``db_name`` by default.

        """
        self.options = options

        self.client = self.connect()
        self._check_connection_established(self.client)
        self.tos = None  # TOS collection
        self.payloads_coll = None  # Optional separate payloads-collection
        atexit.register(self.disconnect)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self):
        """Connect to MongoDB.

        :returns: MongoDB client object.
        :rtype: pymongo.MongoClient
        """
        server = self.options.get("db_server") or DEFAULT_DB_ADDRESS
        # conn_string = (
        #     f"mongodb+srv://"
        #     f'{self.options["db_user"]}'
        #     f':{self.options["db_passw"]}'
        #     f'@{server}'
        # )
        if self.options.get("db_passw"):
            client = pymongo.MongoClient(
                host=server,
                authSource=self.options.get("db_auth_source")
                or self.options["db_name"],
                authMechanism="SCRAM-SHA-1",
                username=self.options["db_user"],
                password=self.options["db_passw"],
                serverSelectionTimeoutMS=self.options.get("timeout", 10000),
            )
        else:
            client = pymongo.MongoClient(
                host=server,
                serverSelectionTimeoutMS=self.options.get("timeout", 10000),
            )

        return client

    def disconnect(self):
        self.client.close()

    def _check_connection_established(self, client):
        """Get active nodes (DB servers).

        :raises ServerSelectionTimeoutError: if no
                 connections active.
        """
        try:
            return client.server_info()
        except pymongo.errors.ServerSelectionTimeoutError as err:
            raise Exception("Is MongoDB running?") from err

    def initialize_tos(
        self,
        collection_suffix="",
        separate_payloads=False,
        payloads_ttl_seconds=0,
        collection_prefix="",
    ):
        """Initialize Mongo database and collection objects.

        If ``payloads_ttl_seconds`` is given a positive non-zero value,
        payloads in separate collection will have the given lifetime
        in seconds. The existence of the index will be enforced on every initialisation.

        :param collection_suffix: Optional suffix to collection name
        :param separate_payloads: Optionally separate payloads to separate collection
        :param payloads_ttl_seconds: Optional lifetime for separate TTL payloads
        :param collection_prefix: Optional prefix to collection name

        :raises ValueError: If `separate_payloads` is not given but `payloads_ttl_seconds` is.
        :raises ValueError: if `payloads`-collection already exists but ``payloads_ttl_seconds``
                 is not given.
        """
        database = self.client[self.options["db_name"]]
        collection_base = "task_objects"
        collection = ".".join(
            filter(None, [collection_prefix, collection_base, collection_suffix])
        )
        if not _validate_collection_name(collection):
            raise NameError("Collection name must conform to [0-9a-z_.]")

        payloads_collection = ".".join(filter(None, [collection_prefix, "payloads"]))
        self.tos = database[collection]
        if separate_payloads:
            self.payloads_coll = database[payloads_collection]
            if payloads_ttl_seconds > 0:
                self._initialize_ttl_payloads(payloads_ttl_seconds)

        elif payloads_ttl_seconds > 0:
            raise ValueError(
                "Payload TTL-index cannot be automatically created without "
                "payloads being separated to their own collection."
            )
        else:
            try:
                collections = self.list_collections()
            except pymongo.errors.PyMongoError:
                # missing permission to listcollections
                collections = []
            if payloads_collection in collections:
                raise ValueError(
                    f"Found '{payloads_collection}'-collection, without argument indicating "
                    "the creation of separate payload collection.\n"
                    "'{payloads_collection}' is reserved collection name. "
                    "Please rename it or provide the flag 'separate_payloads'."
                )

    def list_collections(self):
        return self.client[self.options["db_name"]].list_collection_names()

    def _initialize_ttl_payloads(self, payloads_ttl_seconds):
        """Initializes TTL-index for the separate payloads-collection.

        Indexing is based on 'updatedAt'-field.

        :param payloads_ttl_seconds: TTL in seconds
        :type payloads_ttl_seconds: int

        :raises pymongo.errors.OperationFailure: if index already
                 exists with different value
        """
        self.payloads_coll.create_index(
            "updatedAt", name="ttl_index", expireAfterSeconds=payloads_ttl_seconds
        )

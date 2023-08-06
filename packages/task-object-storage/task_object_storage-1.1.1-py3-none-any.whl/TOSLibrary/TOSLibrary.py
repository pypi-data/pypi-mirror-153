# import os, sys
# DIRNAME = os.path.dirname(os.path.abspath(__file__))
# PACKAGE_ROOT = os.path.abspath(os.path.join(DIRNAME, os.pardir))
# sys.path.append(PACKAGE_ROOT)

from tos.task_object_storage import TaskObjectStorage
from .dynamic_library import DynamicLibrary
from robot.utils.robottime import timestr_to_secs


class TOSLibrary(DynamicLibrary):
    """Robot Framework layer for TOS."""

    def __init__(
        self,
        db_server,
        db_name,
        db_user="",
        db_passw="",
        db_auth_source="",
        collection_suffix="",
        separate_payloads=False,
        payloads_ttl=0,
        collection_prefix="",
    ):
        """
        Initialize the MongoDB client and collection.

        Register the methods inside ``tos.TaskObjectStorage`` as
        ``TOSLibrary`` keywords.

        :param db_server: Mongodb server uri and port, e.g. 'localhost:27017'
        :type db_server: str
        :param db_name: Database name.
        :type db_name: str
        :param db_user: Database username.
        :type db_user: str
        :param db_passw: Database password.
        :type db_passw: str
        :param db_auth_source: Authentication database.
        :type db_auth_source: str
        :param collection_suffix: Suffix for collection. (task_objects.suffix)
        :type collection_suffix: str
        :param collection_prefix: Prefix for collection. (prefix.task_objects, prefix.payloads)
        :type collection_prefix: str
        :param separate_payloads: Optionally separate payloads to separate collection
        :type separate_payloads: bool
        :param payloads_ttl: Optional lifetime for separate payloads.
            Either seconds or timestring (for example '30 days' or '1h 10s')
        :type payloads_ttl: Union[int, str]
        """
        super(TOSLibrary, self).__init__()
        self.tos = TaskObjectStorage(
            db_server=db_server,
            db_name=db_name,
            db_user=db_user,
            db_passw=db_passw,
            db_auth_source=db_auth_source,
        )
        self.tos.initialize_tos(
            collection_suffix=collection_suffix,
            collection_prefix=collection_prefix,
            separate_payloads=separate_payloads,
            payloads_ttl_seconds=int(timestr_to_secs(payloads_ttl, round_to=0)),
        )

        self.add_component(self.tos)

import warnings

import pymongo
from tos.settings import ErrorMessages
from tos.utils import accept_string_object_ids

from . import query_helpers as helper


class TaskFinders:

    @accept_string_object_ids
    def find_task_object_by_id(self, object_id):
        """
        Get a single task object.

        This doesn't change the status of the task object.

        With separated payload collection:
        Returns task object with BARE payload (just reference to separate payload).
        Use `find_task_object_by_id_and_merge_payload` to get already
        merged payload like in a normal task object.

        :param object_id: the object id
        :type object_id: ObjectId or str
        :returns: task object
        :raises ValueError: When no task object with given id is found
        :rtype: dict
        """
        to = self.tos.find_one({"_id": object_id})
        if to:
            return to
        raise ValueError(f"Could not find task object with given id: {str(object_id)}")

    def find_one_task_object_by_status(self, statuses):
        """Convenience method."""
        return self.find_one_task_object_by_status_and_stage(statuses=statuses)

    def find_one_task_object_by_stage(self, stages):
        """Convenience method."""
        return self.find_one_task_object_by_status_and_stage(stages=stages)

    def find_one_task_object_by_status_and_stage(self, statuses=None, stages=None, **kwargs):
        """
        Get one of the task objects by status and (optionally) by stage.

        The status of the task object is **always** set to processing when
        using this keyword.

        The filtered results are sorted by date (by default) in ascending
        order so an item with the hightest priority will be returned.

        Filters out task-objects which have `defer_until`-field set in the future.

        :param statuses: status(es)
        :type statuses: str or list of strs
        :param stages: stage number(s)
        :type stages: int or list of ints
        :param sort_condition: custom sort condition of the form
                               `[("_id", pymongo.ASCENDING)]`

        :raises TypeError: when invalid keyword arguments passed
        :returns: task object with the hightest priority.
        :rtype: dict
        """
        if statuses is stages is None:
            raise TypeError("Pass statuses or stages or both.")

        if not kwargs.get("sort_condition"):
            sort_condition = [("_id", pymongo.ASCENDING)]
        elif kwargs.get("sort_condition") == "priority":
            # TODO: is this ever really needed?
            sort_condition = [("priority", pymongo.DESCENDING)]
        else:
            sort_condition = kwargs["sort_condition"]

        amend = kwargs.get("amend", "")
        query = helper.create_query(statuses, stages, amend, filter_deferred=True)

        task_object = self.tos.find_one_and_update(
            query,
            {"$set": {"status": "processing"}},
            sort=sort_condition
        )
        if task_object and self.payloads_coll:
            task_object = self.find_task_object_by_id_and_merge_payload(task_object["_id"])

        if task_object:
            self.set_task_object_executor(task_object["_id"])
            self.set_task_object_build_number(task_object["_id"])
            self.set_task_object_job_name(task_object["_id"])

        return task_object

    def find_all_failed_task_objects(self):
        """Convenience method."""
        return self.find_all_task_objects_by_status("fail")

    def find_all_task_objects_by_status(self, statuses):
        """Convenience method."""
        return self.find_all_task_objects_by_status_and_stage(statuses=statuses)

    def find_all_task_objects_by_stage(self, stages):
        """Convenience method."""
        return self.find_all_task_objects_by_status_and_stage(stages=stages)

    def find_all_task_objects_by_status_and_stage(self, statuses=None, stages=None):
        """Get all task objects by status and stage.

        The returned list is sorted by priority in descending order so the
        hightest priority item is always the first.

        Filters out task-objects which have `defer_until`-field set in the future.

        With separated payload collection:
        Returns task objects with BARE payload (just reference to separate payload)
        Use ``find_all_task_objects_and_merge_them_with_payloads`` to get task objects
        with merged payloads.

        :param statuses: status(es)
        :type statuses: str or list of strs
        :param stages: stage number(s)
        :type stages: int or list of ints
        :raises TypeError: when invalid keyword arguments passed
        :returns: list of task objects
        :rtype: list

        Usage:

        >>> find_all_task_objects_by_status_and_stage("pass", 1)
        """
        # FIXME: might be stupid to support both list an str arguments. Maybe always use a list?
        if statuses is stages is None:
            raise TypeError("Pass statuses or stages or both.")

        query = helper.create_query(statuses, stages, filter_deferred=True)
        task_objects = self.tos.find(query).sort([("priority", -1), ])

        return list(task_objects)

    def find_one_task_object_marked_as_manual_and_not_passed(self):
        """
        Get one of the task objects marked as manual.

        The list returned by `find_all_task_objects_marked_as_manual_and_not_passed`
        is sorted by priority so the hightest priority item is
        always the first.

        :returns: manual task object with the hightest priority.
        :rtype: dict
        """
        # TODO: Deprecate this method
        warnings.warn("Use status instead of manual field", DeprecationWarning)
        if self.payloads_coll:
            raise TypeError(ErrorMessages.OPERATION_NOT_SUPPORTED_WITH_SEP_PAYLOADS)
        task_objects = self.find_all_task_objects_marked_as_manual_and_not_passed()
        if not task_objects:
            return None
        one_object = task_objects[0]

        return one_object

    def find_all_task_objects_marked_as_manual_and_not_passed(self):
        """
        Get all task objects marked to manual handling.

        :returns: list of task objects
        :rtype: list
        """
        # TODO: Deprecate this method
        warnings.warn("Use status instead of manual field", DeprecationWarning)
        if self.payloads_coll:
            raise TypeError(ErrorMessages.OPERATION_NOT_SUPPORTED_WITH_SEP_PAYLOADS)
        task_objects = self.tos.find(
            {"manual": {"$eq": True},
             "status": {"$ne": "pass"}}
        ).sort([("priority", -1), ])

        return list(task_objects)

    @accept_string_object_ids
    def find_task_object_by_id_and_merge_payload(self, object_id):
        """
        Finds given task object, then finds the referenced payload in separate collection,
        and merges it with the original task object. Resulting task object does not contain
        the "extra"-fields in the payload documents, such as `_id` or timestamps.

        :param object_id: The payload document object id
        :type object_id: ObjectId or str
        :raises TypeError: If separated payloads are not initialised
        :raises ValueError: When no task object or referenced payload with given id is found
        :returns: task object
        :rtype: dict
        """
        if not self.payloads_coll:
            raise TypeError(ErrorMessages.SEP_PAYLOADS_NOT_INITIALIZED)
        cursor = self._find_task_objects_and_merge_payloads([object_id])
        results = list(cursor)
        if results:
            return results[0]
        raise ValueError(
            f"Could not find either task object with given id: {str(object_id)},"
            " or its referenced payload. Has the payload document expired?"
        )

    def find_all_task_objects_and_merge_them_with_payloads(self, object_ids: list):
        """ Finds all given task objects, and merges them with their referenced payloads.

        Note: If task object contains reference to expired payload, this method will
        not return the task object!

        :param object_ids: Task objects' Object ID's
        :type object_id: List of ObjectIds
        :raises TypeError: If separated payloads are not initialised
        :returns: Cursor to iterate over query results
        :rtype: pymongo.cursor
        """
        if not self.payloads_coll:
            raise TypeError(ErrorMessages.SEP_PAYLOADS_NOT_INITIALIZED)
        cursor = self._find_task_objects_and_merge_payloads(object_ids)
        return list(cursor)

    @accept_string_object_ids
    def find_payload_document_by_to_id(self, object_id):
        """
        Finds the given whole (with ID and timestamps) payload
        from the separate 'payloads'-collection.

        :param object_id: The payload document object id
        :type object_id: ObjectId or str
        :returns: payload document
        :raises TypeError: If separated payloads are not initialised
        :raises ValueError: When no payload document with given id is found
        :rtype: dict
        """
        if not self.payloads_coll:
            raise TypeError(ErrorMessages.SEP_PAYLOADS_NOT_INITIALIZED)
        to = self.find_task_object_by_id(object_id)
        return self.find_payload_document_by_payload_id(to['payload']['_id'])

    @accept_string_object_ids
    def find_payload_document_by_payload_id(self, payload_id):
        """
        Finds the given whole payload (with ID and timestamps)
        from the separate 'payloads'-collection.

        :param object_id: The payload document object id
        :type object_id: ObjectId or str
        :returns: task object
        :raises TypeError: If separated payloads are not initialised
        :raises ValueError: When no payload document with given id is found
        :rtype: dict
        """
        if not self.payloads_coll:
            raise TypeError(ErrorMessages.SEP_PAYLOADS_NOT_INITIALIZED)
        payload = self.payloads_coll.find_one({"_id": payload_id})
        if payload:
            return payload
        raise ValueError(
            f"Could not find task object payload with given payload id: {str(payload_id)}. "
            "Has the payload document expired?"
        )

    def _find_task_objects_and_merge_payloads(self, object_ids: list):
        """
        Finds and merges task objects with their referenced payloads in separate collection.
        Leaves out "extra"-fields in the separate payload documents, such as `_id` or timestamps.
        E.g.
        Actual task object:
        {
            ...,
            "payload": {
                "_id": ObjectId("...")
            },
            ...
        }
        Returned (merged) object:
        {
            ...,
            "payload": {
                "key in payload doc": "value in payload doc",
                "key2 in payload doc": [
                    "values in payload doc"
                ]
                etc...
            },
            ...
        }
        Expects given id's to be Object IDs, returns cursor to the results.

        :param object_ids: Task objects' Object ID's
        :type object_id: List of ObjectIds
        :returns: Cursor to iterate over query results
        :rtype: pymongo.cursor
        """
        return self.tos.aggregate([
            {
                '$match': {
                    "_id": {
                        "$in": object_ids
                    }
                }
            }, {
                '$lookup': {
                    'from': self.payloads_coll.name,
                    'localField': 'payload._id',
                    'foreignField': '_id',
                    'as': 'payload'
                }
            }, {
                '$unwind': {
                    'path': '$payload'
                }
            }, {
                '$addFields': {
                    'payload': '$payload.payload'
                }
            }, {
                '$sort': {
                    "priority": -1
                }
            }
        ])

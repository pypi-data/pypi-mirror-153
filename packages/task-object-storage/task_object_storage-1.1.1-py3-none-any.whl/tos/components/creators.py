import copy
import warnings

from tos.templates import INITIAL_TASK_OBJECT

from tos.utils import (
    accept_string_object_ids,
    get_temporary_file,
)


class TaskCreators:

    def create_new_task_object(self, payload, process_name="", priority=0):
        """
        Create a new task object and insert into database.

        With separate payload collection:
        Returns merged to task object, identical as with regular usage.
        Use `find_task_object_by_id` to get the actual, bare task object
        if it is required.

        :param payload: The contents of the actual task object
        :type payload: dict
        :param priority: Priority of the task object, default=0.
        :type priority: int
        :param process_name: Name of the process.
        :type process_name: str
        :returns: The created task object.
        :rtype: dict

        Usage:

        >>> payload = {"customer_number": 583459089}
        >>> create_new_task_object(payload)
        {
            "_id": ObjectId("5c519c08cd9c9f140f95b427"),
            "status": "new",
            "stage": 0,
            "priority": 0,
            "executor": ""
            "payload": {
                "customer_number": 583459089
            }
            "analytics": {},
        }

        With separated payloads collection returns the same value.
        However the true created task object is::
            {
                "_id": ObjectId("5c519c08cd9c9f140f95b427"),
                ...
                "payload": {
                    "_id": ObjectId("60db0d52d30efa2804f80a8c")
                }
                ...
            }

        """
        # TODO: think of a better way to represent a task object template
        task_object = copy.deepcopy(INITIAL_TASK_OBJECT)
        task_object["priority"] = priority
        if self.payloads_coll:
            payload_id = self._insert_separate_payload(payload).inserted_id
            self._add_created_at_timestamp_field_to_separate_payload(payload_id)
            task_object["payload"] = {"_id": payload_id}
        else:
            task_object["payload"] = payload

        if process_name:
            warnings.warn("process_name should not be used anymore", DeprecationWarning)
            task_object["process_name"] = process_name  # deprecate this

        inserted = self._insert_task_object(task_object)
        task_object = self._add_created_at_timestamp_field(inserted.inserted_id)
        if self.payloads_coll:
            task_object['payload'] = payload
        return task_object

    def _add_created_at_timestamp_field(self, task_object_id):
        return self._set_task_object_item(
            task_object_id,
            "createdAt",
            task_object_id.generation_time
        )

    def _insert_task_object(self, task_object):
        return self.tos.insert_one(task_object)

    def _add_created_at_timestamp_field_to_separate_payload(self, payload_id):
        creation_time = payload_id.generation_time
        # Also sets updatedAt field
        self._set_payload_document_item_by_payload_id(payload_id, "createdAt", creation_time)

    def _insert_separate_payload(self, payload):
        return self.payloads_coll.insert_one({'payload': payload})

    def save_binary_payload_to_tmp(self, task_object, payload_item_name, prefix="", suffix=""):
        tmp_file = get_temporary_file(prefix, suffix)
        with open(tmp_file, "wb") as f:
            f.write(task_object["payload"][payload_item_name])

        return tmp_file

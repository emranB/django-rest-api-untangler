import query_objects
import enums
from django.db import transaction
import update_object_in_database
import api_client
from django.http import HttpResponse, JsonResponse
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from typing import Any, Dict, Optional

# Configuration variables
MAX_NAME_LENGTH = 5

"""
Logger Helper class
- Abstracts away low level logging methods and provides simple interface for caller
"""
class LoggerHelper:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def log_info(self, message: str) -> None:
        self.logger.info(message)
        print(message)

    def log_warning(self, message: str) -> None:
        self.logger.warning(message)
        print(message)

    def log_error(self, message: str) -> None:
        self.logger.error(message)
        print(message)

    def log_exception(self, message: str) -> None:
        self.logger.exception(message)
        print(message)

logger_helper = LoggerHelper()

"""
Status messages class
- Provides Interface for logging and printing messages based on their status types
"""
class StatusMsg:
    @staticmethod
    def success(msg: str, data: Optional[Dict[str, Any]] = None) -> HttpResponse:
        logger_helper.log_info(msg)
        return JsonResponse({"success": True, "message": msg, "data": data}, status=200)

    @staticmethod
    def warning(msg: str) -> HttpResponse:
        logger_helper.log_warning(msg)
        return JsonResponse({"success": False, "message": msg}, status=422)

    @staticmethod
    def not_found(msg: str) -> HttpResponse:
        logger_helper.log_warning(msg)
        return JsonResponse({"success": False, "message": msg}, status=404)

    @staticmethod
    def error(msg: str) -> HttpResponse:
        logger_helper.log_error(msg)
        return JsonResponse({"success": False, "message": msg}, status=500)

    @staticmethod
    def exception(msg: str) -> HttpResponse:
        logger_helper.log_exception(msg)
        return JsonResponse({"success": False, "message": msg}, status=500)

"""
API Manager class
- Handles rest API calls with input data
- Handles error catching
- Manages machine state
"""
class ApiManager:
    # High level public method to be used by caller
    def rest_endpoint(self, input_data: 'Input') -> HttpResponse:
        try:
            obj_response = self._fetch_object(input_data.id)
            if obj_response.status_code != 200:
                return obj_response

            obj = obj_response.json().get('data')

            validation_response = self._validate_input(input_data)
            if validation_response.status_code != 200:
                return validation_response

            update_response = self._update_object_attributes(obj, input_data)
            if update_response.status_code != 200:
                return update_response

            finalize_response = self._finalize_object(obj, input_data)
            if finalize_response.status_code != 200:
                return finalize_response

            return StatusMsg.success(f"Object {obj['id']} successfully processed", data=obj)
        except Exception as e:
            return StatusMsg.exception(f"Unexpected error: {str(e)}")

    # Fetch object from db
    def _fetch_object(self, obj_id: int) -> HttpResponse:
        try:
            with transaction.atomic():
                qs = query_objects(id=obj_id)
                if not qs.exists():
                    return StatusMsg.not_found(f"Object with id {obj_id} not found")
                obj = qs.get()
                return StatusMsg.success("Object fetched successfully", data=obj)
        except Exception as e:
            return StatusMsg.exception(f"Exception in _fetch_object: {str(e)}")

    # Validate input data
    # - Validates names length
    # - Validates input data type
    def _validate_input(self, input_data: 'Input') -> HttpResponse:
        try:
            if len(input_data.name) > MAX_NAME_LENGTH:
                return StatusMsg.warning(f"Input name '{input_data.name}' exceeds length limit")
            if input_data.type not in enums.Types._value2member_map_:
                return StatusMsg.warning(f"Invalid input type: {input_data.type}")
            return StatusMsg.success("Input validated successfully")
        except Exception as e:
            return StatusMsg.exception(f"Exception in _validate_input: {str(e)}")

    # Updates name and type of input
    def _update_object_attributes(self, obj: Dict[str, Any], input_data: 'Input') -> HttpResponse:
        try:
            obj['name'] = f"{input_data.name}_object"
            obj['type'] = enums.Types.BANK_ACCOUNT
            return StatusMsg.success("Object attributes updated successfully")
        except Exception as e:
            return StatusMsg.exception(f"Exception in _update_object_attributes: {str(e)}")

    # Performs final transaction and saves object
    def _finalize_object(self, obj: Dict[str, Any], input_data: 'Input') -> HttpResponse:
        try:
            with transaction.atomic():
                response = api_client.post(obj, input_data)
                if response.status != 200:
                    return StatusMsg.error(f"API client post failed with status: {response.status}")
                update_object_in_database.update_object_in_database(obj, input_data.details)
                obj.save()
                transaction.on_commit(lambda: logger_helper.log_info(f"Transaction committed for object {obj}"))
            return StatusMsg.success("Object finalized successfully")
        except Exception as e:
            return StatusMsg.exception(f"Exception in _finalize_object: {str(e)}")

    # Method called once django transaction has been successfully completed
    # - If this method is not called, transaction was not comitted
    @staticmethod
    @receiver(post_save, sender=query_objects.QuerySet)
    def post_save_handler(sender: Any, instance: Any, **kwargs: Any) -> None:
        logger_helper.log_info(f"Post save signal triggered for object {instance}")
        updated_obj = query_objects(id=instance['id']).get()
        logger_helper.log_info(f"Updated object data: {updated_obj}")

"""
Input data class
"""
class Input:
    def __init__(self, id: int, name: str, type: str, details: Dict[str, Any]) -> None:
        self.id = id
        self.name = name
        self.type = type
        self.details = details

"""
Main loop
"""
if __name__ == "__main__":
    input_data = Input(id=1, name="test", type="bank_account", details={})
    api_manager = ApiManager()
    response = api_manager.rest_endpoint(input_data)
    print(response)

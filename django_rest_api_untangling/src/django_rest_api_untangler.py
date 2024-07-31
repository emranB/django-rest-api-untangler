from django.db import transaction
from .LoggerHelper import LoggerHelper
from .StatusMsg import StatusMsg
from django.db.models.signals import post_save
from django.dispatch import receiver
import query_objects
import enums
import update_object_in_database
import api_client

logger_helper = LoggerHelper()

def rest_endpoint(input):
    obj_response = _fetch_object(input.id)
    if not obj_response["success"]:
        return obj_response

    obj = obj_response["data"]
    
    validation_response = _validate_input(input)
    if not validation_response["success"]:
        return validation_response

    update_response = _update_object_attributes(obj, input)
    if not update_response["success"]:
        return update_response

    finalize_response = _finalize_object(obj, input)
    if not finalize_response["success"]:
        return finalize_response

    logger_helper.log_info(f"Object {obj['id']} successfully processed")
    return StatusMsg.success("Operation completed successfully")

def _fetch_object(obj_id):
    try:
        with transaction.atomic():
            qs = query_objects.query_objects(id=obj_id).select_for_update().filter(id=obj_id)
            if not qs.exists():
                return StatusMsg.not_found(f"Object with id {obj_id} not found")
            obj = qs.get()
            return StatusMsg.success("Object fetched successfully", data=obj)
    except Exception as e:
        return StatusMsg.error(f"Exception in _fetch_object: {str(e)}")

def _validate_input(input):
    try:
        if len(input.name) > 5:
            return StatusMsg.unprocessable_entity(f"Input name '{input.name}' exceeds length limit")
        if input.type != enums.Types.BANK_ACCOUNT.value:
            return StatusMsg.unprocessable_entity(f"Invalid input type: {input.type}")
        return StatusMsg.success("Input validated successfully")
    except Exception as e:
        return StatusMsg.error(f"Exception in _validate_input: {str(e)}")

def _update_object_attributes(obj, input):
    try:
        obj['name'] = f"{input.name}_object"
        obj['type'] = enums.Types.BANK_ACCOUNT
        return StatusMsg.success("Object attributes updated successfully")
    except Exception as e:
        return StatusMsg.error(f"Exception in _update_object_attributes: {str(e)}")

def _finalize_object(obj, input):
    try:
        with transaction.atomic():
            logger_helper.log_info(f"Finalizing object: {obj}")
            response = api_client.post(obj, input)
            if response.status != 200:
                return StatusMsg.error(f"API client post failed with status: {response.status}")
            update_object_in_database.update_object_in_database(obj, input.details)
            obj.save()  # Single save call
            logger_helper.log_info(f"Saving object after update: {obj}")
            transaction.on_commit(lambda: logger_helper.log_info(f"Transaction committed for object {obj}"))
        return StatusMsg.success("Object finalized successfully")
    except Exception as e:
        return StatusMsg.error(f"Exception in _finalize_object: {str(e)}")

@receiver(post_save, sender=query_objects.QuerySet)
def post_save_handler(sender, instance, **kwargs):
    logger_helper.log_info(f"Post save signal triggered for object {instance}")
    updated_obj = query_objects.query_objects(id=instance['id']).get()
    logger_helper.log_info(f"Updated object data: {updated_obj}")

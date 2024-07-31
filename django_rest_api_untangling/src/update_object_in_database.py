from .LoggerHelper import LoggerHelper

logger_helper = LoggerHelper()

def update_object_in_database(obj, details):
    logger_helper.log_info("update_object_in_database() called")
    print("update_object_in_database() called")

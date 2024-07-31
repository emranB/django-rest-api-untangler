from .LoggerHelper import LoggerHelper

logger_helper = LoggerHelper()

class QuerySet:
    def __init__(self, exists=True):
        self.exists = exists

    def select_for_update(self):
        return self

    def filter(self, **kwargs):
        return self

    def exists(self):
        return self.exists

    def get(self):
        logger_helper.log_info("query_objects.get() called")
        return "dummy_object"

def query_objects(id):
    return QuerySet()

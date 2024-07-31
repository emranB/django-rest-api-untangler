from .LoggerHelper import LoggerHelper

logger_helper = LoggerHelper()

class Response:
    def __init__(self, status=200):
        self.status = status

def post(obj, input):
    logger_helper.log_info("api_client.post() called")
    print("api_client.post() called")
    return Response(status=200)

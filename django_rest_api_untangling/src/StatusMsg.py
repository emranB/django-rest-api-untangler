from django.http import JsonResponse
from .LoggerHelper import LoggerHelper

logger_helper = LoggerHelper()

class StatusMsg:
    logger = logger_helper.logger

    @staticmethod
    def error(msg):
        StatusMsg.logger.error(msg)
        return JsonResponse({"success": False, "message": msg}, status=500)

    @staticmethod
    def not_found(msg):
        StatusMsg.logger.warning(msg)
        return JsonResponse({"success": False, "message": msg}, status=404)

    @staticmethod
    def unprocessable_entity(msg):
        StatusMsg.logger.warning(msg)
        return JsonResponse({"success": False, "message": msg}, status=422)

    @staticmethod
    def success(msg, data=None):
        StatusMsg.logger.info(msg)
        return JsonResponse({"success": True, "message": msg, "data": data}, status=200)

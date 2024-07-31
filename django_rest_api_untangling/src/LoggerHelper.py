import logging

class LoggerHelper:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def log_info(self, message):
        self.logger.info(message)
        print(message)

    def log_warning(self, message):
        self.logger.warning(message)
        print(message)

    def log_error(self, message):
        self.logger.error(message)
        print(message)

    def log_exception(self, message):
        self.logger.exception(message)
        print(message)

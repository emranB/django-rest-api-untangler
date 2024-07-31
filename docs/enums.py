from enum import Enum

class Types(Enum):
    BANK_ACCOUNT = "bank_account"

class StatusCodes(Enum):
    SUCCESS = 200
    WARNING = 422
    NOT_FOUND = 404
    ERROR = 500
    EXCEPTION = 500
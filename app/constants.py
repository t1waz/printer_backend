from enum import Enum


class FileStatus(Enum):
    REGISTER = 0
    IMAGE_CREATED = 1
    SENDED_TO_PRINT = 2
    PRINTED = 3
    ERROR = 4

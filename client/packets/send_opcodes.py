from enum import Enum


class SendOps(Enum):
    USER_REQ_GAME_LOGIN = 1
    USER_MOVE = 2
    BLOB_EAT = 3

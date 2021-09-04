from enum import Enum


class RecvOps(Enum):
    USER_REQ_GAME_LOGIN = 1
    USER_MOVE = 2
    BLOB_EAT = 3

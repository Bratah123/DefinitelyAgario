from enum import Enum


class RecvOps(Enum):
    ON_USER_REQ_GAME_LOGIN = 1
    ON_USER_MOVE = 2
    ON_REMOVE_USER = 3
    ON_BLOB_INIT = 4
    ON_BLOB_EAT = 5

from enum import Enum


class SendOps(Enum):
    ON_USER_REQ_GAME_LOGIN = 1
    ON_USER_MOVE = 2
    ON_REMOVE_USER = 3

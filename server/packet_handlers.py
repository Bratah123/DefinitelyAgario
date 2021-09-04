from server_opcodes.recv_opcodes import RecvOps


class PacketHandler:
    def __init__(self, opcode, func):
        self.opcode = opcode
        self.func = func


def handler(opcode: RecvOps):
    def inner(func):
        return PacketHandler(opcode.value, func)

    return inner


class GamePackets:

    @staticmethod
    @handler(opcode=RecvOps.USER_REQ_GAME_LOGIN)
    def handle_user_request_game_login(client, in_packet):
        print("hello world")
        pass

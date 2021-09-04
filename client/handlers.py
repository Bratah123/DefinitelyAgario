from player import Player
from packets.packet import Packet
from packets.recv_opcodes import RecvOps


class PacketHandler:
    def __init__(self, opcode, func):
        self.opcode = opcode
        self.func = func


def handler(opcode):
    def inner(func):
        return PacketHandler(opcode.value, func)

    return inner


class ServerPackets:

    @staticmethod
    @handler(opcode=RecvOps.ON_USER_REQ_GAME_LOGIN)
    def handle_on_user_req_game_login(client, packet: Packet):
        client_id = packet.decode_int()
        client.client_id = client_id

        radius = packet.decode_int()
        x = packet.decode_int()
        y = packet.decode_int()
        color = (packet.decode_byte(), packet.decode_byte(), packet.decode_byte())
        player = Player(x, y, radius, color, client)
        client.player = player

    @staticmethod
    @handler(opcode=RecvOps.ON_USER_MOVE)
    def handle_on_user_move(client, packet: Packet):
        x = packet.decode_int()
        y = packet.decode_int()
        radius = packet.decode_int()
        r = packet.decode_byte()
        g = packet.decode_byte()
        b = packet.decode_byte()
        color = (r, g, b)
        pos = (x, y)
        client.player.draw_remote_player(color, pos, radius)

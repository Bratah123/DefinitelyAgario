import random

from packets.packet import Packet
from server_opcodes.send_opcodes import SendOps
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
        # Send the player some Player() info
        packet = Packet(opcode=SendOps.ON_USER_REQ_GAME_LOGIN.value)
        packet.encode_int(client.id)
        packet.encode_int(20)  # starting radius
        start_x, start_y = random.randint(0, 1280), random.randint(0, 720)
        packet.encode_int(start_x)
        packet.encode_int(start_y)
        red, green, blue = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        packet.encode_byte(red)  # R
        packet.encode_byte(green)  # G
        packet.encode_byte(blue)  # B
        client.send_packet(packet)

    @staticmethod
    @handler(opcode=RecvOps.USER_MOVE)
    def handle_user_move(client, in_packet):
        client_id = in_packet.decode_int()
        x, y = in_packet.decode_int(), in_packet.decode_int()
        radius = in_packet.decode_int()
        r, g, b = in_packet.decode_byte(), in_packet.decode_byte(), in_packet.decode_byte()

        packet = Packet(opcode=SendOps.ON_USER_MOVE.value)  # we send this to packet to the other players in the game
        packet.encode_int(client_id)
        packet.encode_int(x)
        packet.encode_int(y)
        packet.encode_int(radius)
        packet.encode_byte(r)
        packet.encode_byte(g)
        packet.encode_byte(b)
        client.broadcast_packet_except_self(packet)

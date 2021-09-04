import random

from packets.packet import Packet
from game_object import Blob
from server_constants import BLOBS, BLOB_AMOUNT
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
        packet.encode_int(10)  # starting radius
        start_x, start_y = random.randint(0, 1280), random.randint(0, 720)
        packet.encode_int(start_x)
        packet.encode_int(start_y)
        red, green, blue = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        packet.encode_byte(red)  # R
        packet.encode_byte(green)  # G
        packet.encode_byte(blue)  # B
        client.send_packet(packet)
        packet = Packet(opcode=SendOps.ON_BLOB_INIT.value)
        packet.encode_int(len(BLOBS))
        for blob in BLOBS:
            blob.encode(packet)
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

    @staticmethod
    @handler(opcode=RecvOps.BLOB_EAT)
    def handle_blob_eat(client, in_packet):
        blob_id = in_packet.decode_int()
        for blob in BLOBS:
            if blob.blob_id == blob_id:
                BLOBS.remove(blob)
                break
        packet = Packet(opcode=SendOps.ON_BLOB_EAT.value)
        packet.encode_int(blob_id)
        client.broadcast_packet(packet)
        if len(BLOBS) == 0:  # If no more blobs on the field we reset the game
            for i in range(BLOB_AMOUNT):
                BLOBS.append(Blob(i))
            packet = Packet(opcode=SendOps.ON_BLOB_INIT.value)
            packet.encode_int(len(BLOBS))
            for blob in BLOBS:
                blob.encode(packet)
            for cli in client.clients:
                modified_packet = Packet(opcode=SendOps.ON_PLAYER_MODIFIED.value)
                x, y = random.randint(0, 1280), random.randint(0, 720)
                radius = 10
                modified_packet.encode_int(x)
                modified_packet.encode_int(y)
                modified_packet.encode_int(radius)
                cli.send_packet(modified_packet)
            client.broadcast_packet(packet)

    @staticmethod
    @handler(opcode=RecvOps.PLAYER_EAT)
    def handle_player_eat(client, in_packet):
        player_id = in_packet.decode_int()
        packet = Packet(opcode=SendOps.ON_PLAYER_EAT.value)
        packet.encode_int(player_id)
        client.broadcast_packet_except_self(packet)

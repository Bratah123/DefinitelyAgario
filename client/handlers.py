from blob import Blob
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
        player.player_id = client_id
        client.player = player

    @staticmethod
    @handler(opcode=RecvOps.ON_USER_MOVE)
    def handle_on_user_move(client, packet: Packet):
        client_id = packet.decode_int()
        x = packet.decode_int()
        y = packet.decode_int()
        radius = packet.decode_int()
        r = packet.decode_byte()
        g = packet.decode_byte()
        b = packet.decode_byte()
        color = (r, g, b)
        for player in client.player.players:
            if player.player_id == client_id:
                player.x = x
                player.y = y
                player.radius = radius
                player.color = color
                break
        else:
            new_player = Player(x, y, radius, color, None)
            new_player.player_id = client_id
            client.player.players.append(new_player)

    @staticmethod
    @handler(opcode=RecvOps.ON_REMOVE_USER)
    def handle_on_remove_user(client, packet):
        client_id = packet.decode_int()
        for player in client.player.players:
            if player.player_id == client_id:
                client.player.players.remove(player)
                break

    @staticmethod
    @handler(opcode=RecvOps.ON_BLOB_INIT)
    def handle_on_blob_init(client, packet):
        blob_amt = packet.decode_int()
        for i in range(blob_amt):
            blob_id = packet.decode_int()
            x = packet.decode_int()
            y = packet.decode_int()
            radius = packet.decode_int()
            r = packet.decode_byte()
            g = packet.decode_byte()
            b = packet.decode_byte()
            blob = Blob(blob_id, x, y, radius, (r, g, b))
            client.player.blobs.append(blob)

    @staticmethod
    @handler(opcode=RecvOps.ON_BLOB_EAT)
    def handle_on_blob_eat(client, packet):
        blob_id = packet.decode_int()
        client.player.remove_blob_by_id(blob_id)

    @staticmethod
    @handler(opcode=RecvOps.ON_PLAYER_EAT)
    def handle_on_player_eat(client, packet):
        player_id = packet.decode_int()
        if player_id == client.player.player_id:
            client.player.is_dead = True
        client.player.make_player_dead_by_id(player_id)

    @staticmethod
    @handler(opcode=RecvOps.ON_PLAYER_MODIFIED)
    def handle_on_player_modified(client, packet):
        x = packet.decode_int()
        y = packet.decode_int()
        radius = packet.decode_int()
        client.player.x = x
        client.player.y = y
        client.player.radius = radius
        client.player.is_dead = False
        for player in client.player.players:
            player.is_dead = False

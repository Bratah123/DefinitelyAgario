"""
    @author brandon
    entry point for the connection
"""
import inspect
import pickle
import socket
import sys
import time
from threading import Thread

import pygame

from handlers import ServerPackets, PacketHandler
from packets.send_opcodes import SendOps
from packets.packet import Packet
from window import Window

SPAM_PACKETS = [
    2,  # User Move
]


class Client:
    def __init__(self, player=None, window=None):
        self._client_id = 0
        self._server_ip = "127.0.0.1"
        self._server_port = 4444
        self._window = window
        self._player = player
        self._is_online = True
        self._client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client_socket.connect((self._server_ip, self._server_port))

        self._handlers = {}
        members = inspect.getmembers(ServerPackets())
        for _, member in members:
            if isinstance(member, PacketHandler):
                self._handlers[member.opcode] = member.func

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, new_player):
        self._player = new_player

    @property
    def window(self):
        return self._window

    @property
    def client_id(self):
        return self._client_id

    @client_id.setter
    def client_id(self, new_id):
        self._client_id = new_id

    def send_packet(self, packet):
        try:
            if packet.opcode not in SPAM_PACKETS:
                print("[INFO] Sending packet to server")
            self._client_socket.sendall(pickle.dumps(packet))
        except Exception as e:
            print("[ERROR] Server is offline:", e)
            self.close()
            sys.exit()

    def receive(self):
        while self._is_online:
            buffer = self._client_socket.recv(4096)
            if not buffer:
                continue
            try:
                packet = pickle.loads(buffer)
            except Exception as e:
                print("[ERROR] Error loading pickle data:", e)
                continue
            if packet.opcode not in SPAM_PACKETS:
                print("[RECV] Packet Received opcode:", packet.opcode)
            self.dispatch_packet(packet)
        self._client_socket.close()

    def dispatch_packet(self, packet):
        packet.seek(0)
        self._handlers[packet.opcode](client=self, packet=packet)

    def close(self):
        self._client_socket.close()


def main():
    pygame.display.set_caption("Definitely Agario")
    win = Window()
    # Construct the socket connection and listeners
    client = Client(window=win)
    packet_listener = Thread(target=client.receive)
    packet_listener.start()
    # Send initial setup packet
    packet = Packet(opcode=SendOps.USER_REQ_GAME_LOGIN.value)
    client.send_packet(packet)
    # game loop
    clock = pygame.time.Clock()
    while True:
        if client.player is None:
            continue
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        try:
            client.player.listen_input_event()
            client.player.draw_game()
        except pygame.error:
            print("[INFO] no game found exiting connections")
            client.close()
            sys.exit()


if __name__ == '__main__':
    main()

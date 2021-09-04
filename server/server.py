"""
    @author brandon
    The entry point of the server
"""
import inspect
import socket
from threading import Thread

from connection.server_client import ServerClient
from packet_handlers import GamePackets, PacketHandler
from server_constants import SERVER_IP, SERVER_PORT, MAX_CONNECTIONS


class Server:
    def __init__(self):
        self._ip = SERVER_IP
        self._port = SERVER_PORT
        self._max_conn = MAX_CONNECTIONS
        self._clients = []
        self._id_gen = 0
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self._packet_handlers = {}
        members = inspect.getmembers(GamePackets())
        for _, member in members:
            if isinstance(member, PacketHandler):
                self._packet_handlers[member.opcode] = member.func
            # Values are the opcodes, key is the function() to be ran

    def start(self):
        try:
            print("[INFO] Starting server...")
            self._server_socket.bind((self._ip, self._port))
            self._server_socket.listen(self._max_conn)
            print("[INFO] Server successfully started up")
            print(f"[INFO] Listening for connections on port: {self._port}")
            self.on_connection()
        except Exception as e:
            print("[ERROR] Error trying to start server:", e)

    def on_connection(self):
        """
        The logic for when a player initially connects to the server.
        We create a new server connection object and initialize its packet listeners for the server
        to communicate to the connection
        :return:
        """
        while True:
            conn, addr = self._server_socket.accept()
            print(f"[INFO] Connection from {addr}")
            server_client = ServerClient(conn, addr, handlers=self._packet_handlers)
            self._id_gen += 1
            server_client.id = self._id_gen
            self._clients.append(server_client)
            accept_thread = Thread(target=server_client.init_listener)
            accept_thread.start()


SERVER = Server()  # Global instance to server object


def main():
    SERVER.start()


if __name__ == '__main__':
    main()

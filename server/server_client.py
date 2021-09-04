import pickle

from packets.packet import Packet
from server_opcodes.send_opcodes import SendOps

SPAM_PACKETS = [
    2,  # User Move
]


class ServerClient:
    def __init__(self, socket, addr=(), is_online=True, handlers=None):
        self._id = 0
        self._addr = addr
        self._socket = socket
        self._is_online = is_online
        self._handlers = handlers
        self._clients = []
        if handlers is None:
            self._handlers = {}

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, new_id):
        self._id = new_id

    @property
    def handlers(self):
        return self._handlers

    @handlers.setter
    def handlers(self, handler):
        self._handlers = handler

    @property
    def clients(self):
        return self._clients

    @clients.setter
    def clients(self, new_clients):
        self._clients = new_clients

    def send_packet(self, packet):
        try:
            if packet.opcode not in SPAM_PACKETS:
                print(f"[SEND] Sending Packet with opcode:", packet.opcode)
            packet.seek(0)
            self._socket.sendall(pickle.dumps(packet))
        except Exception as e:
            print(f"[ERROR] Connection to {self._addr} most likely lost:", e)
            packet = Packet(opcode=SendOps.ON_REMOVE_USER.value)
            packet.encode_int(self.id)
            for client in self._clients:
                if client.id != self.id:
                    client.send_packet(packet)
            self._is_online = False
            self._socket.shutdown(1)
            self._clients.remove(self)

    def init_listener(self):
        while self._is_online:
            # We are receiving the Packet class back by pickled data from the connection
            try:
                buffer = self._socket.recv(4096)
            except ConnectionResetError or ConnectionAbortedError:
                print(f"[ERROR] Lost connection to {self._addr}")
                self._is_online = False
                packet = Packet(opcode=SendOps.ON_REMOVE_USER.value)
                packet.encode_int(self.id)
                for client in self._clients:
                    if client.id != self.id:
                        client.send_packet(packet)
                break
            if not buffer:
                continue
            packet = pickle.loads(buffer)
            if packet.opcode not in SPAM_PACKETS:
                print("[RECV] Packet Received opcode:", packet.opcode)
            self.dispatch_packet(packet)
        self._clients.remove(self)
        self._socket.shutdown(1)

    def dispatch_packet(self, packet):
        packet.seek(0)
        func = self._handlers.get(packet.opcode)
        if func is None:
            print("[INFO] Unknown opcode:", packet.opcode)
        func(client=self, in_packet=packet)

    def broadcast_packet_except_self(self, packet):
        for client in self.clients:
            if client.id != self.id:
                client.send_packet(packet)

    def broadcast_packet(self, packet):
        for client in self.clients:
            client.send_packet(packet)

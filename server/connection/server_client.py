import pickle


class ServerClient:
    def __init__(self, socket, addr=(), is_online=True, handlers=None):
        self._id = 0
        self._addr = addr
        self._socket = socket
        self._is_online = is_online
        self._handlers = handlers
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

    def send_packet(self, packet):
        try:
            print(f"[SEND] Sending Packet with opcode:", packet.opcode)
            self._socket.sendall(pickle.dumps(packet))
        except Exception as e:
            print(f"[ERROR] Connection to connection {self._addr} most likely lost:", e)
            self._is_online = False

    def init_listener(self):
        while self._is_online:
            # We are receiving the Packet class back by pickled data from the connection
            buffer = self._socket.recv(2048)
            if not buffer:
                continue
            packet = pickle.loads(buffer)
            print("[RECV] Packet Received opcode:", packet.opcode)
            self.dispatch_packet(packet)
        self._socket.shutdown(1)

    def dispatch_packet(self, packet):
        self._handlers[packet.opcode](client=self, in_packet=packet)

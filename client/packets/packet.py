from io import BytesIO
from struct import pack, unpack


class Packet(BytesIO):
    """
    The class to send information from the server to the connection and vice versa
    """

    def __init__(self, initial_data=None, opcode=-1):
        if initial_data is None:
            initial_data = b''
        super().__init__(initial_data)
        self._opcode = opcode

    @property
    def opcode(self):
        return self._opcode

    @opcode.setter
    def opcode(self, op):
        self._opcode = op

    def encode_byte(self, val):
        self.write(pack('b', val))
        return self

    def encode_int(self, val):
        self.write(pack('i', val))
        return self

    def decode_byte(self):
        return self.read(1)[0]

    def decode_int(self):
        return unpack('I', self.read(4))[0]

    def encode_string(self, string):
        self.write(pack('H', len(string)))

        for ch in string:
            self.write(ch.encode())

        return self

    def decode_string(self) -> str:
        length = self.decode_short()
        string = ""

        for _ in range(length):
            string += self.read(1).decode()

        return string

    def encode_short(self, value):
        self.write(pack('H', value))
        return self

    def decode_short(self):
        return unpack('H', self.read(2))[0]

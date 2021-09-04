import random


class Blob:
    def __init__(self, blob_id):
        self.blob_id = blob_id
        self.x = random.randint(0, 1280)
        self.y = random.randint(0, 720)
        self.radius = 5
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def encode(self, packet):
        packet.encode_int(self.blob_id)
        packet.encode_int(self.x)
        packet.encode_int(self.y)
        packet.encode_int(self.radius)
        packet.encode_byte(self.color[0])
        packet.encode_byte(self.color[1])
        packet.encode_byte(self.color[2])

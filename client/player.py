from math import sqrt

import pygame.draw
from circle import Circle
from packets.packet import Packet
from packets.send_opcodes import SendOps


class Player(Circle):
    """
    Represents the player object in Agario
    """

    def __init__(self, x, y, radius, color, client, velocity=5):
        super().__init__(x, y, radius, color)
        self._player_id = 0
        self._client = client
        self._velocity = velocity
        self._players = []
        self._blobs = []
        self._is_dead = False

    @property
    def player_id(self):
        return self._player_id

    @player_id.setter
    def player_id(self, new_plr_id):
        self._player_id = new_plr_id

    @property
    def players(self):
        return self._players

    @property
    def blobs(self):
        return self._blobs

    @property
    def is_dead(self):
        return self._is_dead

    @is_dead.setter
    def is_dead(self, dead):
        self._is_dead = dead

    def velocity(self):
        vel = self._velocity - (self.radius // 50)
        return vel if vel > 0 else 1

    def window(self):
        return self._client.window.window

    def listen_input_event(self):
        keys_pressed = pygame.key.get_pressed()
        if self._is_dead:
            return
        if keys_pressed[pygame.K_UP]:
            if not self.y - self._velocity <= 0:
                self.y -= self.velocity()
        if keys_pressed[pygame.K_DOWN]:
            if not self.y + self._velocity >= self._client.window.height:
                self.y += self.velocity()
        if keys_pressed[pygame.K_LEFT]:
            if not self.x - self._velocity <= 0:
                self.x -= self.velocity()
        if keys_pressed[pygame.K_RIGHT]:
            if not self.x - self._velocity >= self._client.window.width:
                self.x += self.velocity()

    def send_packet(self, packet):
        self._client.send_packet(packet)

    def draw_game(self):
        self.window().fill((255, 255, 255))
        self.draw_self(self.window())
        for player in self._players:
            if player.is_dead:
                continue
            if self.contains(player):
                player.is_dead = True
                continue
            player.draw_self(self.window())
        for blob in self._blobs:
            blob.draw_self(self.window())
            if self.contains(blob):
                self.remove_blob_by_id(blob.blob_id)
                self.radius += blob.radius
                packet = Packet(opcode=SendOps.BLOB_EAT.value)
                packet.encode_int(blob.blob_id)
                self.send_packet(packet)
        pygame.display.update()
        packet = Packet(opcode=SendOps.USER_MOVE.value)
        self.encode(packet)
        self.send_packet(packet)

    def contains(self, circle):
        distance = sqrt((circle.x - self.x)**2 + (circle.y - self.y)**2)
        if self.radius > (distance + circle.radius):
            return True
        return False

    def remove_blob_by_id(self, blob_id):
        for blob in self.blobs:
            if blob.blob_id == blob_id:
                self.blobs.remove(blob)
                break

    def remove_player_by_id(self, player_id):
        for player in self.players:
            if player.player_id == player_id:
                self.blobs.remove(player)
                break

    def encode(self, packet):
        packet.encode_int(self._client.client_id)
        packet.encode_int(self._x)
        packet.encode_int(self._y)
        packet.encode_int(self._radius)
        packet.encode_byte(self._color[0])  # R
        packet.encode_byte(self._color[1])  # G
        packet.encode_byte(self._color[2])  # B

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

    @property
    def player_id(self):
        return self._player_id

    @player_id.setter
    def player_id(self, new_plr_id):
        self._player_id = new_plr_id

    @property
    def players(self):
        return self._players

    def velocity(self):
        # TODO: figure out an algo to make the player slower if they are bigger
        return abs(self._velocity)

    def window(self):
        return self._client.window.window

    def listen_input_event(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_UP]:
            self.y -= self._velocity
        if keys_pressed[pygame.K_DOWN]:
            self.y += self._velocity
        if keys_pressed[pygame.K_LEFT]:
            self.x -= self._velocity
        if keys_pressed[pygame.K_RIGHT]:
            self.x += self._velocity

    def send_packet(self, packet):
        self._client.send_packet(packet)

    def draw_game(self):
        self.window().fill((255, 255, 255))
        self.draw_self(self.window())
        for player in self._players:
            player.draw_self(self.window())
        pygame.display.update()
        packet = Packet(opcode=SendOps.USER_MOVE.value)
        self.encode(packet)
        self.send_packet(packet)

    def encode(self, packet):
        packet.encode_int(self._client.client_id)
        packet.encode_int(self._x)
        packet.encode_int(self._y)
        packet.encode_int(self._radius)
        packet.encode_byte(self._color[0])  # R
        packet.encode_byte(self._color[1])  # G
        packet.encode_byte(self._color[2])  # B

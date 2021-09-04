import pygame


class Window:
    def __init__(self, width=1280, height=720):
        self._width = width
        self._height = height
        self._window = pygame.display.set_mode((self._width, self._height))

    @property
    def window(self):
        return self._window

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

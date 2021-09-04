import pygame


class Circle:
    """
    Represents any circle object in Agario
    """

    def __init__(self, x, y, radius, color):
        self._x = x
        self._y = y
        self._radius = radius
        self._color = color

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, new_x):
        self._x = new_x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, new_y):
        self._y = new_y

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, new_radius):
        self._radius = new_radius

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, new_clr):
        self._color = new_clr

    def pos(self):
        return self._x, self._y

    def draw_self(self, display):
        self.draw_circle(display, self._color, self.pos(), self._radius)

    @staticmethod
    def draw_circle(display, color, pos, radius):
        pygame.draw.circle(display, color, pos, radius)

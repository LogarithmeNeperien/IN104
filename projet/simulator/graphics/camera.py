#04/05 Seta : codage de to_screen_coords et from_screen_cords
from ..utils.vector import Vector2


class Camera:
    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.position = Vector2(0, 0)
        self.scale = 1

    def to_screen_coords(self, position):
        """ Converts the world-coordinate position to a screen-coordinate. """
        return self.scale*(position-self.position)

    def from_screen_coords(self, position):
        """ Converts the screen-coordinate position to a world-coordinate. """
        return position/self.scale+self.position

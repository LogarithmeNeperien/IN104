from ..utils.vector import Vector2, Vector


class Camera:
    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.position = Vector2(0, 0)
        self.scale = 1
        self.offset = Vector2(screen_size[0]/100,screen_size[1]/100)

    def to_screen_coords(self, position):
        """ Converts the world-coordinate position to a screen-coordinate. """
        return (position+self.offset)*self.scale

        raise NotImplementedError

    def from_screen_coords(self, position):
        """ Converts the screen-coordinate position to a world-coordinate. """
        return (position/self.scale)-self.offset

        raise NotImplementedError

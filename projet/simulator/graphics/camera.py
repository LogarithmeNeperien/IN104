#04/05 Seta : codage de to_screen_coords et from_screen_cords
#; ajout de l'attribut follows qui vaut None si la camera ne suit aucun body, les coordonnées du body suivi sinon.
from ..utils.vector import Vector2


class Camera:
    def __init__(self, screen_size,follows=None):
        self.screen_size = screen_size
        self.position = Vector2(0, 0)
        self.scale = 1
        self.follows=follows

    def to_screen_coords(self, position):
        """ Converts the world-coordinate position to a screen-coordinate. """
        return self.scale*(position-self.position)

    def from_screen_coords(self, position):
        """ Converts the screen-coordinate position to a world-coordinate. """
        return position/self.scale+self.position

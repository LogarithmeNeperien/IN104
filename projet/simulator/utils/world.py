#04/05 Seta, on stocke l'ID d'un body dans un attribut qu'on appelle id_nb. Avant l'attribution on l'initialise à -1.

from .vector import Vector2
from ..utils.uid import UID


class Body:
    def __init__(self, position, velocity=Vector2(0, 0), mass=1, color=(255, 255, 255), draw_radius=50,id_nb=-1):
        self.position = position
        self.velocity = velocity
        self.mass = mass
        self.color = color
        self.draw_radius = draw_radius
        self.id_nb=id_nb

    def __str__(self):
        return "<pos:%s, vel:%s, mass:%.2f>" % (self.position, self.velocity, self.mass)


class World:
    def __init__(self):
        self._bodies = []

    def add(self, body):
        """ Add `body` to the world.
            Return a unique ID for `body`.
            enregistre l'ID dans body.id_nb
        """
        new_id = len(self._bodies)
        self._bodies.append(body)
        body.id_nb=new_id
        return new_id

    def get(self, id_):
        """ Return the body with ID `id`.
            If no such body exists, return None.
        """
        if (id_ >= 0 and id_ < len(self._bodies)):
            return self._bodies[id_]
        return None

    def bodies(self):
        """ Return a generator of all the bodies. """
        for body in self._bodies:
            yield body

    def __len__(self):
        """ Return the number of bodies """
        return len(self._bodies)

    def __str__(self):
        return "Bodies: %d\n\t%s" % \
            (len(self),
             '\n\t'.join([str(i) + ": " + str(self._bodies[i])
                          for i in range(len(self))]))

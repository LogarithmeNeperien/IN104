#04/05 Seta, on stocke l'ID d'un body dans un attribut qu'on appelle id_nb. Avant l'attribution on l'initialise à -1.

#11/05 Theophane : Ajout de la méthode merge_bodies qui réalise la fusion de deux corps, et d'un attribut real_radius dans la classe Body

from .vector import Vector2
from ..utils.uid import UID


class Body:
    def __init__(self, position, velocity=Vector2(0, 0), mass=1, color=(255, 255, 255), real_radius = 50, draw_radius=50,id_nb=-1):
        self.position = position
        self.velocity = velocity
        self.mass = mass
        self.color = color
        self.real_radius = real_radius
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

    def merge_bodies(self,id_winner,id_loser):
        """ Return the list of bodies where two of them were merged into one """
        if id_winner != id_loser :
            winner = self.get(id_winner)
            loser = self.get(id_loser)
            winner.position = (winner.position+loser.position)/2
            winner.velocity = (winner.position+loser.velocity)/2
            winner.mass += loser.mass
            winner.draw_radius = (winner.draw_radius+loser.draw_radius)/2
            winner.real_radius = (winner.real_radius+loser.real_radius)/2
            self._bodies.remove(loser)

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

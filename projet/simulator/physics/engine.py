from ..utils.vector import Vector, Vector2
from .constants import G
from ..utils.world import World


def gravitational_force(pos1, mass1, pos2, mass2):
    """ Return the force applied to a body in pos1 with mass1
        by a body in pos2 with mass2
    """

    # If the bodies occupy the same position
    # we suppose they're not applying any
    # force to one another
    if pos1 == pos2 :
        return Vector2(0,0)

    direction = pos2.__sub__(pos1)

    return direction.__rmul__(G*mass1*mass2).__truediv__((direction.norm())**3)

    raise NotImplementedError


class IEngine:
    def __init__(self, world):
        self.world = world

    def derivatives(self, t0, y0):
        """ This is the method that will be fed to the solver
            it does not use it's first argument t0,
            its second argument y0 is a vector containing the positions
            and velocities of the bodies, it is laid out as follow
                [x1, y1, x2, y2, ..., xn, yn, vx1, vy1, vx2, vy2, ..., vxn, vyn]
            where xi, yi are the positions and vxi, vyi are the velocities.

            Return the derivative of the state, it is laid out as follow
                [vx1, vy1, vx2, vy2, ..., vxn, vyn, ax1, ay1, ax2, ay2, ..., axn, ayn]
            where vxi, vyi are the velocities and axi, ayi are the accelerations.
        """
        raise NotImplementedError

    def make_solver_state(self):
        """ Returns the state given to the solver, it is the vector y in
                y' = f(t, y)
            In our case, it is the vector containing the
            positions and speeds of all our bodies:
                [x1, y1, x2, y2, ..., xn, yn, vx1, vy1, vx2, vy2, ..., vxn, vyn]
            where xi, yi are the positions and vxi, vyi are the velocities.
        """
        raise NotImplementedError


class DummyEngine(IEngine):
    def __init__(self, world):
        super().__init__(world)

    def derivatives(self, t0, y0):
        world = self.world
        vector = Vector(y0.dim)
        mid_range = int(y0.dim / 2)

        # First we fill the first nth speeds with the
        # last nth speeds from the previous
        # vector
        for i in range(int((y0.dim)/4)):
            vector.__setitem__(2*i,y0.__getitem__(2*i+mid_range))
            vector.__setitem__(2*i+1,y0.__getitem__(2*i+1+mid_range))

        #print("copie = " + str(vector))
        # Then we can compute the acceleration
        # via NewTon's second law

        for i in range(len(world._bodies)):
            pos = (world._bodies[i]).position
            mass = (world._bodies[i]).mass
            speed = (world._bodies[i]).velocity
            a = Vector2(0,0)
            for body in world._bodies :

                a = a.__add__(gravitational_force(pos,
                mass,body.position,body.mass))

            vector.__setitem__(2*i+mid_range,a.get_x()/mass)
            vector.__setitem__(2*i+1+mid_range,a.get_y()/mass)

        return vector


    def make_solver_state(self):
        world = self.world
        world_size = world.__len__()
        state = Vector(world_size*4)
        for i in range(world_size):
            state.__setitem__(2*i,world._bodies[i].position[0])
            state.__setitem__(2*i+1,world._bodies[i].position[1])
            state.__setitem__(2*i+2*world_size,world._bodies[i].velocity[0])
            state.__setitem__(2*i+1+2*world_size,world._bodies[i].velocity[1])
        return state




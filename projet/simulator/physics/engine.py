#11/05 Theophane: Ajout de la fonction detect_collision

from ..utils.vector import Vector, Vector2
from .constants import G

from ..utils.quadtree import Quadtree


def gravitational_force(pos1, mass1, pos2, mass2):
    """ Return the force applied to a body in pos1 with mass1
        by a body in pos2 with mass2
    """
    #SETA 2/05 : in 2D
    d=(pos2-pos1).sqrnorm()
    if d!=0:
    	return G*mass1*mass2*d**(-1.5)*(pos2-pos1)
    else:
    	return Vector2(0,0)

def detect_collision(b1,b2):
    return abs(b1.position-b2.position) <= max(b1.real_radius,b2.real_radius)


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
    def __init__(self,world):
        super().__init__(world)

    def make_solver_state(self):
        pos=[]
        vel=[]

        for b in self.world.bodies():

        	pos+=b.position
        	vel+=b.velocity

        values=pos+vel

        y0=Vector(len(values))
        for i in range(len(values)):
            y0[i]=values[i]

        return y0

    def derivatives(self,t0,y0):
        velocities=y0[2*len(self.world)::]

        masses=[b.mass for b in self.world.bodies()]

        accelerations=[0]*2*len(self.world)

        for i in range(len(self.world)):
            pos_b_i=Vector2(y0[2*i],y0[2*i+1])
            for j in range(i):
                pos_b_j=Vector2(y0[2*j],y0[2*j+1])
                force=gravitational_force(pos_b_i,masses[i],pos_b_j,masses[j])
                accelerations[2*i]+=force.get_x()/masses[i]
                accelerations[2*i+1]+=force.get_y()/masses[i]
                accelerations[2*j]-=force.get_x()/masses[j]
                accelerations[2*j+1]-=force.get_y()/masses[j]


        y0_prime=Vector(len(values))
        for i in range(len(values)):
            y0_prime[i]=values[i]

        return y0_prime


class BarnesHutEngine(IEngine):
    def __init__(self,world):
        super().__init__(world)

    def make_solver_state(self):
        pos=[]
        vel=[]

        for b in self.world.bodies():

            pos+=b.position
            vel+=b.velocity

        values=pos+vel

        y0=Vector(len(values))
        for i in range(len(values)):
            y0[i]=values[i]

        return y0




    def derivatives(self,t0,y0):
        velocities=y0[2*len(self.world)::]
        accelerations=[0]*2*len(self.world)

        #calcul de la coordonnées max
        coord_max=0
        for i in range(2*len(self.world)):
            coord_max=max(coord_max,abs(y0[i]))

        #création du quadtree
        quadtree=Quadtree(coord_max)
        for b in self.world.bodies():
            quadtree.add(b)

        i=0

        for b in self.world.bodies():

            quadtree.calculate_acceleration_on(b,gravitational_force)
            accelerations[2*i]=b.accelerations.get_x()
            accelerations[2*i]=b.accelerations.get_y()
            i+=1



        return velocities+accelerations



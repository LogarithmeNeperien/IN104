#11/05 Theophane : Nouvel intégrateur avec la méthode saute mouton, nécessitant de garder en mémoire les accélerations

from ..utils.vector import Vector

class SolverError(Exception):
    pass


class ISolver:

    # NOTE: our systems do not depend on time,
    # so the input t0 will never be used by the
    # the derivatives function f
    # However, removing it will not simplify
    # our functions so we might as well keep it
    # and build a more general library that
    # we will be able to reuse some day

    def __init__(self, f, t0, y0, max_step_size=0.01):
        self.f = f
        self.t0 = t0
        self.y0 = y0
        self.max_step_size = max_step_size

    def integrate(self, t):
        """ Compute the solution of the system at t
            The input `t` given to this method should be increasing
            throughout the execution of the program.
            Return the new state at time t.
        """
        raise NotImplementedError


class DummySolver(ISolver):
    def __init__(self,f,t0,y0,max_step_size=0.01):
        super().__init__(f,t0,y0,max_step_size)


    def integrate(self, t):
        derivative = (self.f)(t,self.y0)
        derivative = derivative*(self.max_step_size)
        #print("new value y = " + str(self.y0.__add__(derivative)))
        self.y0 = self.y0+derivative
        return self.y0



class LeapFrogSolver(ISolver):
    def __init__(self,f,t0,y0,a0,max_step_size=0.01):
        super().__init__(f,t0,y0,max_step_size)
        self.a0 = [0]*2*len(y0)/2

    def integrate(self,t):
        p_k = y0[0:len(y0)/2]
        v_k = y0[len(y0)/2+1:len(y0)]
        derivative = (self.f)(t,self.y0)
        a_k = derivative[len(y0)/2+1:len(y0)]

        p_k = p_k + max_step_size*v_k + 0.5*max_step_size**2*a_k
        v_k = v_k + 0.5*max_step_size*(a_k+a0)

        self.y0 = p_k + v_k














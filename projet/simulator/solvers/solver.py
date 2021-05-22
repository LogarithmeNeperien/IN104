#16/05 Theophane: Ajout du solveur saute mouton

from ..utils.vector import Vector, Vector2
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

    def integrate(self,t):

        self.y0=[self.y0[i]+(t-self.t0)*self.f(0,self.y0)[i] for i in range(len(self.y0))]

        return self.y0

        if (t-self.t0>self.max_step_size):
            h=self.max_step_size
        else:
            h=t-self.t0

        t_step=self.t0
        while(t_step+h<=t):
            f_result=self.f(t_step,self.y0)
            if isinstance(self.y0,float):

                self.y0=self.y0+h*f_result
            else:

                for i in range(len(self.y0)):
                    self.y0[i]=self.y0[i]+h*f_result[i]

            t_step+=self.max_step_size

        return self.y0

class LeapFrogSolver(ISolver):
    def __init__(self,f,t0,y0,a0,max_step_size=0.01):
        super().__init__(f,t0,y0,max_step_size)
        self.a0 = Vector(int(len(y0)/2))

    def integrate(self,t):
        y0=self.y0
        leng = int(len(y0)/2)
        p_k = Vector(leng)
        p_k[:] = y0[0:leng]
        v_k = Vector(leng)
        v_k[:] = y0[leng:2*leng]
        derivative = (self.f)(t,self.y0)
        a_k = Vector(leng)
        a_k[:] = derivative[leng:len(y0)]

        p_k = p_k + v_k*(self.max_step_size) + a_k*(0.5*self.max_step_size**2)
        v_k = v_k + (a_k+self.a0)*(0.5*self.max_step_size)

        self.y0[0:leng] = p_k
        self.y0[leng:2*leng] = v_k
        self.a0 = a_k
        return self.y0


#11/05 Seta: correction de la méthode step, erreur d'indexation dans y pour velocity 
class Simulator:
    def __init__(self, world, Engine, Solver):
        self.t = 0
        self.world = world

        self.engine = Engine(self.world)

        # Engine uses World to represent the state
        # of the world while Solver uses a
        # vector to represent the current state of
        # the ODE system.
        # The method Engine.make_solver_state computes
        # the vector of state variables (the positions
        # and velocities of the bodies) as a Vector

        y0 = self.engine.make_solver_state()

        self.solver = Solver(self.engine.derivatives, self.t, y0)

    def step(self, h):       
                        
        y = self.solver.integrate(self.t + h)      
            
            
        for i in range(len(self.world)):
            b_i = self.world.get(i)

            b_i.position.set_x(y[2 * i])
            b_i.position.set_y(y[2 * i + 1])
        
            b_i.velocity.set_x(y[2*len(self.world) + 2 * i])
            
            b_i.velocity.set_y(y[2*len(self.world) + 2 * i + 1])

        self.t += h

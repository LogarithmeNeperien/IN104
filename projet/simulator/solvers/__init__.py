# This exposes this module in the current namespace
# we can now write 'from simulator.solvers import DummySolver'
# instead of 'from simulator.solvers.solver import DummySolver'
from .solver import DummySolver
from .solver import LeapFrogSolver

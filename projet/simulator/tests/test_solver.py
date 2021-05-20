import unittest
from math import cos, sin, sqrt, exp, pi
from ..solvers import DummySolver
from ..solvers import LeapFrogSolver

# region ODE Systems

# -------- Simple system
#                 ODE: dx/dt = 9.8 - 0.196 * x
#       Initial value: x(0) = c
# Analytical solution: x(t) = 50 + (c - 50) * exp(-0.196 * t)


def linear_f(t, x):
    return 9.8 - 0.196 * x


def linear_solution(t, c):
    return 50 + (c - 50) * exp(-0.196 * t)

# -------- Periodic system
#                 ODE: dx/dt = (2 * cos^3(t)*sin(t) - sin(t)*x - 1) / cos(t)
#       Initial value: x(pi/4) = c
#              Domain: 0 <= t < pi / 2
# Analytical solution: x(t) = -0.5 * cos(t)*cos(2 * t) - sin(t) + (c / sqrt(2) + 1) * cos(t)


def trigo_f(t, x):
    return (2 * pow(cos(t), 3) * sin(t) - sin(t)*x - 1) / cos(t)


def trigo_solution(t, c):
    return -0.5 * cos(t) * cos(2 * t) - sin(t) + (c / sqrt(2) + 1) * cos(t)

# -------- Non linear system
#                 ODE: dx/dt = (t² - t - 2 * x + 1) / t
#       Initial value: x(1) = c
#              Domain: t > 0
# Analytical solution: x(t) = 0.25 * t² - 1/3 * t + 0.5 + (c - 5/12) / t²


def nonlinear_f(t, x):
    return ((t * t) - t - 2 * x + 1) / t


def nonlinear_solution(t, c):
    return 0.25 * (t * t) - 1/3 * t + 0.5 + (c - 5/12) / (t * t)


# This arry stores all the test cases that will be used for unittesting
ODE_SYSTEMS = [
    ("Linear", linear_f, linear_solution),
    ("Trigo", trigo_f, trigo_solution),
    ("Non Linear", nonlinear_f, nonlinear_solution),
]

# endregion

# region Solvers
# This arry stores all the solvers that will be tested against all the systems
SOLVERS = [DummySolver,LeapFrogSolver]
# endregion


class SolverTestCase(unittest.TestCase):

    def test_integrate(self):
        x0 = 0.600686
        t0 = 0.1243
        h = 1

        for (name, f, solution) in ODE_SYSTEMS:
            with self.subTest(name=name):
                exact_y0 = solution(t0, x0)
                exact = solution(t0 + h, x0)

                for solver in SOLVERS:
                    with self.subTest(solver=solver):
                        solver_instance = solver(
                            f, t0, exact_y0, max_step_size=0.0001)
                        approx = solver_instance.integrate(t0 + h)

                        self.assertAlmostEqual(approx, exact, places=3)

import unittest
from .. import Body, World
from ..utils.vector import Vector2, Vector
from ..physics.engine import DummyEngine,BarnesHutEngine,gravitational_force
from ..physics.constants import G

# region Solvers
# This arry stores all the engines that will be tested by EngineTestCase
ENGINES = [DummyEngine]
# endregion


class EngineTestCase(unittest.TestCase):

    def test_gravitational_forces(self):
        pos1 = Vector2(0, 0)
        mass1 = 10
        pos2 = Vector2(10, 10)
        mass2 = 1

        force = gravitational_force(pos1, mass1, pos2, mass2)

        # two floats computed with two equivalent but different formulas
        # can be different due to rounding errors.
        # self.assertAlmostEqual does not check exact equality
        # but checks that the absolute value of the difference is close enough to 0
        # this requires the implementation of Vector2.__abs__()
        self.assertAlmostEqual(force[0], G * 0.03535533905932737)
        self.assertAlmostEqual(force[1], G * 0.03535533905932737)

    def test_gravitational_forces_antisymmetry(self):
        pos1 = Vector2(0, 0)
        mass1 = 10
        pos2 = Vector2(10, 10)
        mass2 = 1

        force1 = gravitational_force(pos1, mass1, pos2, mass2)
        force2 = gravitational_force(pos2, mass2, pos1, mass1)

        # two floats computed with two equivalent but different formulas
        # can be different due to rounding errors.
        # self.assertAlmostEqual does not check exact equality
        # but checks that the absolute value of the difference is close enough to 0
        # this requires the implementation of Vector2.__abs__()
        self.assertAlmostEqual(force1[0], -force2[0])
        self.assertAlmostEqual(force1[1], -force2[1])

    def test_make_engine_state_one_body(self):
        world = World()
        world.add(Body(Vector2(15, 18), velocity=Vector2(42, 36)))

        for Engine in ENGINES:
            with self.subTest(engine=Engine):
                engine_instance = Engine(world)
                solver_state = engine_instance.make_solver_state()

                self.assertEqual(len(solver_state), 4)
                self.assertAlmostEqual(solver_state[0], 15)
                self.assertAlmostEqual(solver_state[1], 18)
                self.assertAlmostEqual(solver_state[2], 42)
                self.assertAlmostEqual(solver_state[3], 36)

    def test_make_engine_state_two_bodies(self):
        world = World()
        world.add(Body(Vector2(15, 18), velocity=Vector2(42, 36)))
        world.add(Body(Vector2(25, 28), velocity=Vector2(52, 46)))

        for Engine in ENGINES:
            with self.subTest(engine=Engine):
                engine_instance = Engine(world)
                solver_state = engine_instance.make_solver_state()

                self.assertEqual(len(solver_state), 8)
                self.assertAlmostEqual(solver_state[0], 15)
                self.assertAlmostEqual(solver_state[1], 18)
                self.assertAlmostEqual(solver_state[2], 25)
                self.assertAlmostEqual(solver_state[3], 28)
                self.assertAlmostEqual(solver_state[4], 42)
                self.assertAlmostEqual(solver_state[5], 36)
                self.assertAlmostEqual(solver_state[6], 52)
                self.assertAlmostEqual(solver_state[7], 46)

    def test_derviatives_one_body(self):
        world = World()
        world.add(Body(Vector2(15, 18), velocity=Vector2(42, 36)))

        y0 = Vector(4)
        y0[0] = 15
        y0[1] = 18
        y0[2] = 42
        y0[3] = 36

        for Engine in ENGINES:
            with self.subTest(engine=Engine):
                engine_instance = Engine(world)
                derivative = engine_instance.derivatives(0, y0)

                self.assertAlmostEqual(len(derivative), 4)
                self.assertAlmostEqual(derivative[0], 42)
                self.assertAlmostEqual(derivative[1], 36)
                self.assertAlmostEqual(derivative[2], 0)
                self.assertAlmostEqual(derivative[3], 0)

    def test_derviatives_two_bodies(self):
        world = World()
        world.add(Body(Vector2(15, 18), velocity=Vector2(42, 36)))
        world.add(Body(Vector2(10, 28), velocity=Vector2(52, 46)))

        y0 = Vector(8)
        y0[0] = 15
        y0[1] = 18
        y0[2] = 10
        y0[3] = 28
        y0[4] = 42
        y0[5] = 36
        y0[6] = 52
        y0[7] = 46

        for Engine in ENGINES:
            with self.subTest(engine=Engine):
                engine_instance = Engine(world)
                derivative = engine_instance.derivatives(0, y0)

                self.assertAlmostEqual(len(derivative), 8)
                self.assertAlmostEqual(derivative[0], 42)
                self.assertAlmostEqual(derivative[1], 36)
                self.assertAlmostEqual(derivative[2], 52)
                self.assertAlmostEqual(derivative[3], 46)
                self.assertAlmostEqual(derivative[4], -1.538740340017379e-05)
                self.assertAlmostEqual(derivative[5], 3.077480680034758e-05)
                self.assertAlmostEqual(derivative[6], 1.538740340017379e-05)
                self.assertAlmostEqual(derivative[7], -3.077480680034758e-05)

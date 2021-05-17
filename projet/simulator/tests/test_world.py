from .. import World, Body
from ..utils.vector import Vector2
import unittest


class WorldTestCase(unittest.TestCase):
    def setUp(self):
        self.world = World()

    def test_add(self):
        body = Body(Vector2(0, 0))
        id_ = self.world.add(body)

        body_ = self.world.get(id_)
        self.assertEqual(body, body_)

    def test_add_multiple(self):
        body1 = Body(Vector2(0, 0))
        body2 = Body(Vector2(0, 0))
        body3 = Body(Vector2(0, 0))

        id1 = self.world.add(body1)
        id2 = self.world.add(body2)
        id3 = self.world.add(body3)

        body1_ = self.world.get(id1)
        self.assertEqual(body1, body1_)

        body2_ = self.world.get(id2)
        self.assertEqual(body2, body2_)

        body3_ = self.world.get(id3)
        self.assertEqual(body3, body3_)

    def test_get_none(self):
        body = self.world.get(3714)
        self.assertIsNone(body)

    
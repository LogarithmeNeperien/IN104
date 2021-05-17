import unittest
from ..utils.quadtree import Quadtree
from ..utils.vector import Vector2
from ..utils.world import Body



class QuadtreeTestCase(unittest.TestCase):
	def setUp(self):
		#side_lentgh=10
		self.quadtree=Quadtree(10)

	def test_mass(self):
		b1=Body(Vector2(0,0))
		b2=Body(Vector2(3,3))
		b3=Body(Vector2(-5,4))
		b4=Body(Vector2(-1,-1))

		self.quadtree.add(b1)
		self.quadtree.add(b2)
		self.quadtree.add(b3)
		self.quadtree.add(b4)

		self.assertEqual(4,self.quadtree.mean_body.mass)
		
	def test_add(self):
		b1=Body(Vector2(1,1))
		b2=Body(Vector2(1,4))
		b3=Body(Vector2(3,4))
		b4=Body(Vector2(4,3))

		self.quadtree.add(b1)
		self.quadtree.add(b2)
		self.quadtree.add(b3)
		self.quadtree.add(b4)

		
		
		self.assertIsNone(self.quadtree.nodes[0].mean_body)
		self.assertIsNone(self.quadtree.nodes[0].nodes)
		self.assertIsNone(self.quadtree.nodes[1].mean_body)
		self.assertIsNone(self.quadtree.nodes[1].nodes)
		self.assertIsNone(self.quadtree.nodes[3].mean_body)
		self.assertIsNone(self.quadtree.nodes[3].nodes)
		
		
		

		node=self.quadtree.nodes[2]

		for i in range(1):
			self.assertIsNotNone(node.nodes[(3+i)%4].mean_body)
			self.assertIsNone(node.nodes[(3+i)%4].nodes)

		self.assertIsNotNone(node.nodes[1].mean_body)
		self.assertIsNone(node.nodes[1].nodes)


		node=node.nodes[2]

		for i in range(4):
			self.assertIsNone(node.nodes[i].nodes)
			if (i%2==1):
				self.assertIsNotNone(node.nodes[i].mean_body)
			else:
				self.assertIsNone(node.nodes[i].mean_body)
			

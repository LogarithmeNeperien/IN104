#semaine du 17/05 seta ajout de test pour quadtree
import unittest
from ..utils.quadtree import Quadtree
from ..utils.vector import Vector2
from ..utils.world import Body
from random import seed,random


#sert au test_mass. remplit la liste concordance de bool.
#s'il n'y a que des True, la somme des masses de fils est égale à la somme de masses des pères
concordances=[]
def concordance_masse_pere_fils(father,list_concordances):
	sons_total_mass=0
	if father.nodes is not None:
		for son in father.nodes:
			if son.mean_body is not None:

				sons_total_mass+=son.mean_body.mass


	
	list_concordances.append((sons_total_mass==father.mean_body.mass)
							or (father.nodes is None))



class QuadtreeTestCase(unittest.TestCase):
	def setUp(self):
		#side_lentgh=10
		self.quadtree=Quadtree(10)

	def test_mass(self):
		b1=Body(Vector2(0,0))
		b2=Body(Vector2(3,3))
		b2.mass=5
		b3=Body(Vector2(1,-3))
		b3.mass=2
		b4=Body(Vector2(-5,-3.99))
		b4.mass=10
		b5=Body(Vector2(-5,-4))
		b5.mass=3
		

		self.quadtree.add(b1)
		self.quadtree.add(b2)
		self.quadtree.add(b3)
		self.quadtree.add(b4)
		self.quadtree.add(b5)

		self.quadtree.calculate_position_of_mean_bodies()

	
		self.quadtree.rec_visit(lambda father: concordance_masse_pere_fils(father,concordances))
		
		for concord in concordances:
			self.assertTrue(concord)

		
		
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
		self.assertIsNone(self.quadtree.nodes[1].mean_body)
		self.assertIsNone(self.quadtree.nodes[3].mean_body)

		##test quart nord-est
		self.assertIsNotNone(self.quadtree.nodes[2].nodes[0].mean_body)
		self.assertIsNotNone(self.quadtree.nodes[2].nodes[3].mean_body)

		self.assertIsNone(self.quadtree.nodes[2].nodes[1].mean_body)


		##à l'intérieur du nord-est, on prend encore une fois le nord est
		node=self.quadtree.nodes[2].nodes[2]

		self.assertIsNone(node.nodes[0].mean_body)
		self.assertIsNone(node.nodes[2].mean_body)

		self.assertIsNotNone(node.nodes[1].mean_body)
		self.assertIsNotNone(node.nodes[3].mean_body)



	def test_many_bodies(self):
		seed()
		bodies=[Body(Vector2(10*random()-5,10*random()-5)) for i in range(100)]

		for b in bodies:
			self.quadtree.add(b)
		
		self.assertTrue(True)
		
		
			

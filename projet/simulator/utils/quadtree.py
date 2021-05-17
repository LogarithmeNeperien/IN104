from .vector import Vector2
from .world import Body
from ..physics.engine import gravitational_force

#Une feuille est un quadtree. Un noeud qui a 4 fils exactement qui sont des quadtrees est un quadtree
#Un quadtree représente un carré de centre "center"et de longuer de côté "side_length"
#Les fils d'un noeud représentent chaque quart du carré représenté par le père

class Quadtree:
	def __init__(self,side_length,center=Vector2(0,0),mean_body=None,nodes=None):
		self.side_length=side_length
		self.center=center
		self.mean_body=mean_body
		self.nodes=nodes

	def add(self,body):
		if self.mean_body is None:
			self.mean_body=body
		else:
			#si il y a déjà un corps dans le noeud (corps fictif ou non) on doit ajouter le corps récursivement dans le bon noeud fils.
			# (il faut les créer s'ils n'existent pas )
			#Les fils créés représentent les 4 quarts du carré que représentent le noeud père (leur side_length est donc deux fois plus petite)
			if self.nodes is None:
				self.nodes=[Quadtree(self.side_length,
					self.center+Vector2(i*self.side_length/4,j*self.side_length/4)) for j in range(-1,2,2) for i in range(-1,2,2)]

			b_position=body.position
			indice_ajout=-1
			if b_position.get_y()-self.center.get_y()<=0:
				if b_position.get_x()-self.center.get_x()<=0:
					self.nodes[0].add(body)
					indice_ajout=0
				else:
					self.nodes[1].add(body)
					indice_ajout=1
			else:
				if b_position.get_x()-self.center.get_x()<=0:
					self.nodes[2].add(body)
					indice_ajout=2
				else:
					self.nodes[3].add(body)
					indice_ajout=3

			#quand on ajoute un body dans un fils on met à jour le mean_body du parent (on fait la moyenne pondérées par les masses des fils)
			added_body=self.nodes[indice_ajout].mean_body
			self.mean_body.position*=self.mean_body.mass
			self.mean_body.position+=added_body.position*added_body.mass
			self.mean_body.mass+=added_body.mass
			self.mean_body.position/=self.mean_body.mass

	#Le principe de l'algorithme de Barnes-Hut est de considérer qu'on peut réduire l'influence gravitationnelle de corps assez éloignés
	#peut être réduit à l'influence gravitationnel de leur moyenne.
	#Chaque corps est stocké dans une feuille du quadtree et la moyenne des corps des noeuds frères est stocké dans le noeud père.
	#On estime le caractère "assez loin" par la formule s/d<theta == True
	#où d estla distance entre le corps ou le corps moyen et le corps dont on calcule la somme des forces
	#s est le side_length du noeud qui contient le corps ou le corps moyen
	#theta est un paramètre dans [0,1] qui contrôle la précision (on le prend à 0.5 généralement) (à 0 on a la précision maximale et on revient à l'algo brute force)

	#body est le corps dont on calcule la somme des forces extérieures
	
	def calculate_force_on(self,body,theta=0.5):
		n_body=self.mean_body
		if n_body is not None:
			#s/d<theta <=> theta*d>s ; on note aussi que si le noeud n'a pas de fils on calcule la force inconditionnellement
			if theta*(body.position-n_body.position).norm()>node.side_length or node.nodes is None:
				body.acceleration+=gravitational_force(body.position,body.mass,n_body.position,n_body.mass)/body.mass

			else:
				for i in range(4):
					if node.nodes[i].mean_body.id_nb != body.id_nb:
						node.nodes[i].calculate_force_on(body,theta)

		

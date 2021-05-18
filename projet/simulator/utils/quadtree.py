#17/05 seta création du fichier
#18/05 correction lors de l'ajout d'un coprs dans l'arbre. Le mean_body d'une feuille n'était pas réinséré lorsque la-dite feuille devenait un noeud
#on sépare en deux add : add qui ajoute simplement les corps et crée les corps fictifs
#						calculate_position_of_mean_bodies qui met à jour les masses et positions des mean_body qui ne sont pas à des feuilles
from .vector import Vector2
from .world import Body
from ..physics.engine import gravitational_force

#Une feuille est un quadtree. Un noeud qui a 4 fils exactement qui sont des quadtrees est un quadtree
#Un quadtree représente un carré de centre "center"et de longuer de côté "side_length"
#Les fils d'un noeud représentent chaque quart du carré représenté par le père
#Ajout d'un affichage textuel du quadtree

class Quadtree:
	appel_add=0#####################""
	def __init__(self,side_length,center=Vector2(0,0),mean_body=None,nodes=None):
		self.side_length=side_length
		self.center=center
		self.mean_body=mean_body
		self.nodes=nodes

	#écriture récursive de l'arbre en une liste. J'utilise un dessin pour m'y retrouver. nodes[0] est le sud ouest et on tourne dans le sens trigo jusqu'à nodes[3]
	def __str__(self):
		string_nodes="["
		if self.nodes is not None:
			for i in range(4):
				string_nodes+="%s,"%self.nodes[i]

		string_nodes+="]"

		return "<mean_body:%s center: %s nodes:%s"% (self.mean_body,self.center,string_nodes)

	def add(self,body):
		Quadtree.appel_add+=1##############""
		if self.mean_body is None:
			self.mean_body=body
		else:
			#si il y a déjà un corps dans le noeud (corps fictif ou non) on doit ajouter le corps récursivement dans le bon noeud fils.
			# (il faut les créer s'ils n'existent pas )
			#Les fils créés représentent les 4 quarts du carré que représentent le noeud père (leur side_length est donc deux fois plus petite)
			if self.nodes is None:

				self.nodes=[Quadtree(self.side_length/2,
							self.center+Vector2(i[0]*self.side_length/4,i[1]*self.side_length/4)) for i in [(-1,-1),(1,-1),(1,1),(-1,1)] ]
							#self.center+Vector2(i[0]*self.side_length/4,i[1]*self.side_length/4)) for i in[(-1,-1),(1,-1),(1,1),(-1,1)]]			

				#notre feuille devient un noeud, donc le mean_body qu'elle contenait doit être insérer dans une feuille
				true_body=self.mean_body
				self.mean_body=Body(Vector2(0,0))#on crée simplement une instance, sa position sera calculer par calculate_position_of_mean_bodies
				self.mean_body.mass=0#on corps fictif a une masse nulle avant tout ajout
				self.mean_body.id_nb=-1#on fixe à -1 les corps fictifs
				self.add(true_body)
				


			b_position=body.position
			
			if b_position.get_y()-self.center.get_y()<=0:
				if b_position.get_x()-self.center.get_x()<=0:
					self.nodes[0].add(body)
				else:
					self.nodes[1].add(body)
			else:
				if b_position.get_x()-self.center.get_x()<=0:
					self.nodes[3].add(body)					
				else:
					self.nodes[2].add(body)

			self.calculate_position_of_mean_bodies()


	def calculate_position_of_mean_bodies(self):
		if self.nodes is not None:
			#on réinitialise la masse et la position du corps fictif à 0. On n'a normalement pas besoin,
			# mais apparemment ça ne fonctionne pas sans (on ne passait pas les tests)
			self.mean_body.mass=0
			self.mean_body.position=Vector2(0,0)
			for i in range(4):
				
				mass_and_pos=self.nodes[i].calculate_position_of_mean_bodies()
				self.mean_body.mass+=mass_and_pos[0]
				self.mean_body.position+=mass_and_pos[1]*mass_and_pos[0]

			self.mean_body.position/=self.mean_body.mass


		if self.mean_body is not None:
			return (self.mean_body.mass,self.mean_body.position)
		else:
			return (0,0)


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

	
	def rec_visit(self,f):
		
		
		if self.mean_body is not None:
			f(self)

		if self.nodes is not None:
			for i in range(4):
				self.nodes[i].rec_visit(f)



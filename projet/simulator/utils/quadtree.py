#17/05 seta création du fichier
#18/05 correction lors de l'ajout d'un coprs dans l'arbre. Le mean_body d'une feuille n'était pas réinséré lorsque la-dite feuille devenait un noeud
#on sépare en deux add : add qui ajoute simplement les corps et crée les corps fictifs
#						calculate_position_of_mean_bodies qui met à jour les masses et positions des mean_body qui ne sont pas à des feuilles
from .vector import Vector2
from .world import Body
#Une feuille est un quadtree. Un noeud qui a 4 fils exactement qui sont des quadtrees est un quadtree
#Un quadtree représente un carré de centre "center"et de longuer de côté "side_length"
#Les fils d'un noeud représentent chaque quart du carré représenté par le père
#Ajout d'un affichage textuel du quadtree

class Quadtree:
	
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
		#self.nodes=[Quadtree(self.side_length/2,
							#self.center+Vector2(i[0]*self.side_length/4,i[1]*self.side_length/4)) for i in [(-1,-1),(1,-1),(1,1),(-1,1)] ] BACKUP

		if self.mean_body is None:
			self.mean_body=body
		else:
			lifo=[[body,self]]
			while(not(not(lifo))): #tant que lifo n'est pas vide. A noter que lifo==[] <=> not(lifo)
				

				[body_to_place,node_of_placement]=lifo[-1]		
				if node_of_placement.nodes is None:	#création de quatre fils à partir d'un noeud externe plein dans lequel on veut insérer un corps		
					node_of_placement.nodes=[Quadtree(node_of_placement.side_length/2,
											node_of_placement.center+Vector2(i[0]*node_of_placement.side_length/4,i[1]*node_of_placement.side_length/4)) 
											for i in [(-1,-1),(1,-1),(1,1),(-1,1)] ]

					lifo.append((node_of_placement.mean_body,node_of_placement))
					lifo[-1][1].mean_body=Body(Vector2()) #création du corps moyen fictif stocké dans le noeud interne
					[body_to_place,node_of_placement]=lifo[-1]#mise à jour du corps à ajouter en premier	

				

						
				index_of_placement=0
				if body_to_place.position.get_y()-node_of_placement.center.get_y()<=0:
					if body_to_place.position.get_x()-node_of_placement.center.get_x()<=0:
						index_of_placement=0
					else:
						index_of_placement=1
				else:
					if body_to_place.position.get_x()-node_of_placement.center.get_x()<=0:
						index_of_placement=3
					else:
						index_of_placement=2



				if node_of_placement.nodes[index_of_placement].mean_body is None:
					lifo.pop()
					node_of_placement.nodes[index_of_placement].mean_body=body_to_place
				else:
					lifo[-1][1]=node_of_placement.nodes[index_of_placement]
				

			


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
	
	

	
	def rec_visit(self,f):
		
		
		if self.mean_body is not None:
			f(self)

		if self.nodes is not None:
			for i in range(4):
				self.nodes[i].rec_visit(f)



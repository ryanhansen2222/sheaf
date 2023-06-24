import numpy as np




class Stalk():

	#Sheaf object. Has ID,
	# May have a stalk, data value, outgoing restriction morphs,
	#incoming restriction morphisms


	def __init__(self, name, basis):
		#Name of current object (abcd set for example) 
		self.name = name
		self.dimension = len(name)/basis

		#List of incoming objects 
		self.incomingstalks = []
		#List of restricted to objects 
		self.outgoingstalks = []

		#Should be a dict of numpy matricies. Key is name of out
		self.outgoingmats = {}#name: np.identity(len(name))
		

		#Assignment
		self.section = np.ones((1,1))
		
		#Subsection Label
		self.label = -1

		self.visited = False
		

	def add_incoming(self, stalk):
		self.incomingstalks.append(stalk)

	def add_outgoing(self, stalk):
		self.outgoingstalks.append(stalk)
	
	def addrestriction(self, codomain, mapping):
		self.outgoingmats[codomain] = mapping

	def set_section(self, value):
		self.section = value





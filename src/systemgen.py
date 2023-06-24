import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
import copy
from datagen import DataGen



class SystemGen():

	#Randomly generates linear system via a network graph

	#Generates everything for truthful system/data
	def __init__(self, nodes):
		print('Generating equations')
		
		#Make network with networkx
		network = nx.gnp_random_graph(nodes, .5)
		self.network = network
		self.savenetwork('TruthNetwork', network)

		#Generate equations in form of eqtn matrix from cliques
		self.equations = self.generate_eqtns(network)
		self.fake_equations = copy.deepcopy(self.equations)


		#Now we are trying to generate measurement values
		print('Generating Measurement Values')
		#Generate data based on shape of eqtns matrix (maybe we want to change this)
		numreqmeas = len(self.equations) 
		numunmeas = len(self.equations[0]) - numreqmeas
		self.unmeasurable = self.make_unmeasurables(numunmeas)

		


	def savenetwork(self, name, network):
		nx.draw(network, with_labels = True)
		plt.savefig(name)
		plt.clf()

		
		#Randomly choose values for the unmeasurables. This is ground truth
	def make_unmeasurables(self, numunmeas):
		lowbound = 0
		highbound = 10
		#print('Picking unmeasurables values from uniform distribution bounded by: (', lowbound, ',', highbound, ')')
		unmeas = []

		for x in range(numunmeas):
			unmeas.append(random.uniform(lowbound, highbound))
		print('Unmeasurable values vector: ', unmeas)
		final = np.transpose(np.matrix(unmeas))
		return final
		
	 

		
	#Generate the equations from our cliques
	def generate_eqtns(self,network):
		#Start making variables from network
		values = list(network.nodes)
		edges = network.edges
		cliques = list(nx.find_cliques(network))
		print(cliques)

		nodes = len(values)

		#Cliques generate the relationships. Now we form coefficients
		#to generate the linear equation matrix
		equations = []
		for clique in cliques:
			eqtn = [0 for i in range(nodes)]
			for varidx in clique:
				pos = random.randint(0,1)
				negative = 1
				if(pos):
					negative = -1
				coeff = random.randint(1,10)
				eqtn[varidx] = negative*coeff
			equations.append(eqtn)

		print('Generated Equation Matrix:', equations)
		return equations
		
	#Runner for making fake data values
	def makefalsevals(self):
		#Just graph object

		print('Generating ground truth data for permuted network')
		fakenetwork = self.network.copy()

		print('Making False Values')
		name = 'FalseNetwork'
		self.permutation(fakenetwork)
		
		self.savenetwork(name, fakenetwork)
	



		numreq = len(self.fake_equations[0])-len(self.unmeasurable)
		numunmeas = len(self.unmeasurable)
		fakedata = DataGen(self.fake_equations, self.unmeasurable, numreq, numunmeas)
		
		fakemeasurements = fakedata.synthesize()
		return fakemeasurements

		
		

	#Permutation on network
	def permutation(self,network):
		print('Permuting original network')
		
		possiblepermutations = [1]#[1, 2, 3]
		'''
		for i in range(int(len(list(network.nodes))/5)):
			possiblepermutations.append(i)
		'''
		
		numpermutations = random.choice(possiblepermutations)
		print('Permuting ', numpermutations, 'times')

		options = [1,1]
		for x in range(numpermutations):
			selected = random.choice(options)
			#Pathways for each option
			if(selected == 1):
				#Add a clique
				self.addunmeas(network)
			if(selected == 2):
				self.deleteclique(network)


	
	def addunmeas(self, network):
		#We know we need to add new node (rate) for each new eqtn, so we do that here
 
		newunmeas = self.make_unmeasurables(1)
		self.unmeasurable = np.concatenate((self.unmeasurable,newunmeas), 0)

		permutedeqtn = random.randint(0,len(self.fake_equations)-1)

		print("****addunmeas method(1)****", self.equations)
		#e make equations coeff account for new unmeas
		for idx, e in enumerate(self.fake_equations):
			if(permutedeqtn == idx):
				pos = random.choice([-1,1])

				coeff = random.randint(1,10)
				self.fake_equations[idx].append(pos*coeff)
			else:
				self.fake_equations[idx].append(0)

		print("****addunmeas method****", self.equations)



					
	'''    
	def addclique(self,network):
		#What nodes are in the clique? 
		#Expected nodes in eqtn is 3
		nodes = []
		expected = 3
		for node in range(len(list(network.nodes))):
			fail = random.randint(1,len(list(network.nodes)))
			if(fail <= expected):
				nodes.append(node)
		
		#We know we need to add new node (rate) for each new eqtn, so we do that here
		nodes.append(len(list(network.nodes)))
		
		neweqtnvars = []

		#Make clique
		for idx1 in range(len(nodes)):
			for idx2 in range(idx1, len(nodes)):
				if(not network.has_edge(nodes[idx1], nodes[idx2])):

					#Add all participant variables to new eqtn we boutta add
					#Add it to the network for visual purposes as well
					network.add_edge(nodes[idx1], nodes[idx2])


		#Make coeff for new eqtn
		values = list(network.nodes)
		numnodes = len(values)

		#Cliques generate the relationships. Now we form coefficients
		#to generate the linear equation matrix
		eqtn = [0 for i in range(numnodes)]
		for varidx in nodes:
			pos = random.choice([-1,1])

			coeff = random.randint(1,10)
			eqtn[varidx] = pos*coeff
		eqtn = eqtn[-1:] + eqtn[:-1]
		print('Generated New Equation: ', eqtn)


		#print('Now we do maintainence on eqtns - make sure we account for new msrd')
		for e in self.fake_equations:
			e.insert(0,0)
		self.fake_equations.append(eqtn) 

		#Last we update new unmeasured val for the one we just added in
		newunmeas = self.make_unmeasurables(1)
		self.unmeasurable = np.concatenate((self.unmeasurable,newunmeas), 0)
		print('AFTER WE TRY TO PERMUTE VARS', self.unmeasurable)

		#print('The last ', len(self.unmeasurable), ' entries in the EQTN matrix represent unmeasurable values')
	'''


	#Removes an entire clique
	def deleteclique(self,network):
		#Find nodes in clique to remove
		cliques = list(nx.find_cliques(network))
		
		nodes = random.choice(cliques)

		for idx1 in range(len(nodes)):
			for idx2 in range(idx1+1, len(nodes)):
				network.remove_edge(nodes[idx1], nodes[idx2])
		print('Clique Removed: ', nodes)



	#Find the values for measured quantities Least Squares suggests
	def extractsuggested(self, m, a, ls, constantmtx):
		mprime = a*ls[0]
		inverse = np.linalg.inv(constantmtx)
		suggested = -1*inverse*mprime
		return suggested

	#Do Least squares on our target stalk
	def doleastsquares(self, measured, equations):
		print('-------- ANALYSIS --------')
		print('Assuming equations: ', equations, 'And measured values: ', measured)
	
		#Splitting into measure/unmeasured
		chunk = len(measured)
		constant = []
		variables = []
		for eqtn in equations:
			consteqtn = []
			vareqtn = []
			for x in range(len(eqtn)):
				if(x < chunk):
					consteqtn.append(eqtn[x])
				else:
					vareqtn.append(eqtn[x])
	 
			constant.append(consteqtn)
			variables.append(vareqtn)
	 
		constantmtx = np.matrix(constant)
		measuredvect = np.transpose(np.matrix(measured))

		#m = solution side (rhs of eqtn, Ax = m) - for Least Squares
		m = -1 * constantmtx * measuredvect

	 
		#Adding extra rows for underdefined matrix to make least sq
		print('Adding dummy rows in matrix to make least squares work')
		while(len(variables) < len(variables[0])):
			variables.append([0 for x in range(len(variables[0]))])

		#A is lhs of Least Squares Ax=m
		a=np.matrix(variables)


		#Do least squares
		ls = np.linalg.lstsq(a,m,rcond=None)
		
		return m,a,ls, constantmtx


	def maketruthvals(self):
		print('Generating Ground Truth Data from nonpermuted network')
		numreqmeas = len(self.equations) 
		numunmeas = len(self.equations[0]) - numreqmeas
		truthfulobject = DataGen(self.equations, self.unmeasurable, numreqmeas, numunmeas)
		truthfuldata = truthfulobject.synthesize()
		return truthfuldata



		
		

if __name__== "__main__":
	print('Running network test')

	print('----------------GROUND TRUTH DATA--------------')

	test = SystemGen(5)

	print('----------------OUR MODEL IS RIGHT (EXPERIMENT 1)--------------')

	truthfuldata = test.maketruthvals()
	m, a, ls, constantmtx = test.doleastsquares(truthfuldata, test.equations)
	suggested = test.extractsuggested(m, a, ls, constantmtx)


	print('The last ', len(test.unmeasurable), ' entries in the EQTN matrix represent unmeasurable values')
	print('Least squares proposed values for unmeasurable data: ', ls[0])
	print('Least squares suggested values for measured data: ', suggested)
	resid = (truthfuldata)-np.transpose(suggested)
	print('magnitude of least squares measured values residual: ', np.sqrt(resid.dot(np.transpose(resid))))
	
	print('----------------OUR MODEL IS WRONG (EXPERIMENT 2)--------------')
	permuteddata = test.makefalsevals()
	m, a, ls, constantmtx = test.doleastsquares(permuteddata, test.equations)
	suggested = test.extractsuggested(m,a,ls,constantmtx)

	print('The last ', len(test.unmeasurable), ' entries in the EQTN matrix represent unmeasurable values')
	print('Least squares proposed values for unmeasurable data: ', ls[0])
	print('Least squares suggested values for measured data: ', suggested)
	resid = (permuteddata)-np.transpose(suggested)
	print('magnitude of least squares measured values residual: ', np.sqrt(resid.dot(np.transpose(resid))))
	

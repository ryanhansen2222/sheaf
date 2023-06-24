#Test sheaf skeleton. 
'''
------IDEA------
Build the sheaf codomain. The top should be a stalk representing the 
solution space of the entire set of linear equations. Nothing is specified.
Each layer down assigns one of the measured values 'assignment' to the
'assignment' variable in the 'stalk' class. At the bottom, we should 
have all possible routes for solving for the desired variable, and we 
can then measure consistency.
'''


from mcs import MCS 
from stalk import Stalk
import Powerset as pw
import numpy as np
import matplotlib.pyplot as plt
from smartAssignment import SmartAssignment
from systemgen import SystemGen

def containsAll(small, big):
	for c in small.split('('):
		if c not in big.split('('): return 0
	return 1



#Input the stalknae and the array of measured values. Returns the measured
#values for the given assignment. Obsolete??? Feels bad to write code that
#is instantly obsolete
def findvarmeasured(stalkname, measured):
	variables = stalkname.split('(')
	measuredstalk = []
	#print(variables)
	for idx, variable in enumerate(variables):
		if(idx != 0):
			variables[idx] = '(' + variable
			#print(variables[idx])
			measuredstalk.append(measured[findvarnum(variables[idx])-1])
	#print(measuredstalk)
		
		
	
	return measuredstalk


	

#Find missing variable ---- not in small but in big
def findmissing(small, big):
	smalltrans = small.split('(')
	bigtrans = big.split('(')
	for idx, x in enumerate(bigtrans):
		#print(x)
		if x not in small: 
			#print('(' + x)
			return '(' + x, idx
	return bigtrans[0], 0

#Find the idx of the '1' in a given variable
def findvarnum(variable):
	for x in range(len(variable)):
		if variable[x] == '1':
			return x
	return 0

def makestalks(powerset):
	stalklist = []
	basis = len(powerset[0][0])
	print(basis)

	for x in powerset:
		order = len(x)
		name = ""
		for y in x:
			name += y
			
		stalklist.append(Stalk(name, basis))
	return stalklist
	

#Assigns vector of all 1s to all stalks
def dummyassignment(stalklist):
	basis = len(stalklist[0].name)
	for x in stalklist:
		numvariables = len(x.name)/basis
		section = []
		for y in range(int(numvariables)):
			section.append(1)
		x.section = np.transpose(np.matrix(section))

	print('Dummy Assignment Complete')
	
#Dank assignment makes a stupid assignment
def dankassignment(stalklist):
	basis = len(stalklist[0].name)
	count = 0
	for x in stalklist:
		numvariables = len(x.name)/basis
		section = []
		for y in range(int(numvariables)):
			count = count + .2
			section.append(count)
		x.section = np.transpose(np.matrix(section))

	print('Dank Assignment Complete')
	

#Generates the least squares assignment
def lsassignment(stalklist, measured, equations):

	#Creates the bottom level assignment
	for idx, stalk in enumerate(stalklist):
		if(stalk.dimension == 1):
			stalk.section = measured[idx]

	#Making the two parts - constant vect M (b) and variables mtx (A)
	#for least squares analysis
	print('Messing around with matricies')
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
	#varmtx = np.matrix(variables)
	print(measured)
	measuredvect = np.transpose(np.matrix(measured))
	print(constantmtx)
	m = -1 * constantmtx * measuredvect



	#Creates the top ---- 
	print('Generating least squares assignment on Big Daddy')
	print('Equations: ', equations)

	#Adding extra rows for underdefined matrix to make least sq
	print('Adding dummy rows in matrix to make least squares work')
	while(len(variables) < len(variables[0])):
		variables.append([0 for x in range(len(variables[0]))])
	

	a = np.matrix(variables)

	print('Modified eqtns', a)
	print('Measured values vector', m)
	ls = np.linalg.lstsq(a,m, rcond=None)


	print('Least Squares Soltn', ls[0])
	mprime = a*ls[0]
	print("M' Vector", mprime)
	inverse = np.linalg.inv(constantmtx)
	suggested = -1*inverse*mprime
	print('Least Squares Suggested Value', suggested)


	order = len(measured)
	queue = []
	
	#Find big daddy and make its section
	for x in stalklist:
		if(x.dimension == order):
			x.section =suggested 
			queue.append(x)	
	
	#Extend big daddy section to rest of sheaf stalks
	while(len(queue) > 0):
		current = queue.pop(0)
		for x in current.outgoingstalks:
			if(x.dimension > 1):
				queue.append(x)
				x.section = current.outgoingmats[x]*current.section
	print('Done with Least Squares Assignment')
		
	

	print('Least Squares Assignment Complete')
	

	
		


#Generates projection matrix 
def findmapping(height, width, missing):
	matrix = np.zeros((int(height),int(width)))

	#print(matrix)

	missing = missing -1
	d = -1
	for x in range(int(width)):
		d = d+1

		for y in range(int(height)):

			if(x == y):
				if(x == missing):
					d = x+1
				if(d != missing):
					matrix[y,d] = 1
	
	#print(matrix)
	return matrix

#make restrictions for given stalklist
def makerestrictions(stalklist):
	for x in range(len(stalklist)):
		for y in range(x,len(stalklist)):
			low = stalklist[x]
			high = stalklist[y]
			if(low.dimension + 1 == high.dimension):
			
				if(containsAll(low.name,high.name)):
					othr, position = findmissing(low.name,high.name)
					#print('Adding restriction ', high.name, ' --> ', low.name)
					low.add_incoming(high)
					high.add_outgoing(low)
					#newvar = findvarnum(othr)
					mapping = findmapping(low.dimension, high.dimension, position)
					
					high.addrestriction(low,mapping)
	#return stalklist
					

#Input measurements, makes the variable names as we have 
#EXAMPLE
#[1, 2, 3] ---> ['(100)', '(010)', '(001)']
def makevarnames(measurement):
	length = len(measurement)
	variables = [] 
	for varidx in range(length):
		name = ''
		name += '('
		for charidx in range(length):
			if(varidx == charidx):
				name += '1'
			else:
				name += '0'
		name += ')'
		variables.append(name)

	print(variables)
	return (variables)
				
			
def run_simulation(measurement, equations, assignment_type):
	variables = makevarnames(measurement)
	print('From starter variable set: ', variables)

	calcmtx = np.matrix(equations)
	
	

	powerset = pw.powerset(variables) 
	powerset.pop(0)

	print('Powerset: ', powerset)

	print('Generating Stalks from Powerset...')


	#Making Stalks	
	stalklist = makestalks(powerset)
	for x in stalklist:
		print(x.name, x.dimension)

	makerestrictions(stalklist)
	figname = ''

	print('Generated stalks:')
	if(assignment_type == 1):
			dummyassignment(stalklist)
			figname = 'DummyPie'
	if(assignment_type == 2):	
			dankassignment(stalklist)
			figname = 'DankPie'
	if(assignment_type == 3):
			lsassignment(stalklist, measurement, equations)
			figname = 'LeastSquaresPie'
	
	
	for x in stalklist:
		print(x.name, ': Section: ', x.section)

	print('---FINDING MAXIMAL CONSISTENT SUBSECTIONS---')
	print('xxx                                      xxx')
	print('xx                                        xx')
	print('x                                          x')
	
	
	algo = MCS(stalklist)

	for x in range(len(variables)):
		algo.iteration(x)
	
	print('')
	print('*****************************************')
	print('*****************************************')
	print('*****************************************')
	print('************** RESULTS ******************')
	print('')


	for x in stalklist:
		print('Stalk:', x.name, ' Subsection:', x.label)

	

	#Make results count 
	counts = []
	for x in range(len(algo.subsections)):
		counts.append(0)

	for x in stalklist:
		if(x.label > -1):
			counts[x.label] = counts[x.label] + 1

	#Make pie chart
	# Pie chart, where the slices will be ordered and plotted counter-clockwise:
	labels = []
	for x in range (len(algo.subsections)):
		labels.append(x)
	
	sizes = counts
	#explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

	fig1, ax1 = plt.subplots(1)
	ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
		shadow=True, startangle=90)
	ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
	figname = figname + '.png'
	plt.savefig(figname)

	

#Input: Equations E, variables V, measured values M in the form
#EV = M where E
if __name__ == "__main__":
	print('Generating sheaf skeleton...\n')

	
	'''
	#RUN 1
	measurement = [1, 2, 3, 4]

	equations = {"E1": [1, -1, 0, 4],
		"E2": [0, 1, -1, 3]
	} 
	'''
	
	'''
	print('Messing with Random Graph')
	lobbies = nx.random_lobster(5, .55, .3)
	#plt.draw(lobbies)
	#G = PrintGraph()
	#nx.add_path(G, range(10))
	#nx.add_star(G, range(9, 13))
	nx.draw(lobbies)
	plt.show()

	print(lobbies)

	'''

	#RUN 2
	'''
	measurement = [1, 2, 3, 4, 5]
	#measurement = [1, 3, 5, 7, 4, -3]
	equations = {'E1': [1, 0, -4, 0, 2, 0],
			'E2': [0, 1, 0, -3, 0, 0],
			'E3': [3, 0, 1, -2, 0, 0], 
			'E4': [0, 0, 2, 1, -5, 0],
			'E5': [-2, -1, 0, 0, 1, 2]
	}
	'''
	
	system = SystemGen(7)
	measurement = system.truthfuldata
	equations = system.equations

	print('Measurement', measurement)


	#run_simulation(measurement, equations, 1)
	#run_simulation(measurement, equations, 2)
	#run_simulation(measurement, equations, 3)


#MAKING STALKLIST
	variables = makevarnames(measurement)
	print('From starter variable set: ', variables)
	calcmtx = np.matrix(equations)
	powerset = pw.powerset(variables) 
	powerset.pop(0)
	print('Powerset: ', powerset)
	print('Generating Stalks from Powerset...')
	#Making Stalks	
	stalklist = makestalks(powerset)
	for x in stalklist:
		print(x.name, x.dimension)
	makerestrictions(stalklist)
#DONE MAKING STALKLIST

	SmartAssignment(stalklist, measurement, equations)
	
	



		


				


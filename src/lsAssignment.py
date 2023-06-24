import numpy as np


'''
Class responsible for generating the canonical least squares assignment.
The input is a stalklist, measured variables vector, and equations. The
output is a stalklist with appropriate vector sections on each stalk,
starting from the origin and working down through all morphism paths

'''



class LSAssignment():


	#Runner method
	def __init__(self, measured, equations, stalklist):
		#stalklist = self.getstalklist(originstalk)
		self.bottom(stalklist, measured)
		m, a, ls, constantmtx = self.doleastsquares(measured,equations)
		suggested = self.extractsuggested(m,a,ls,constantmtx)
		self.makeassignment(stalklist, suggested)
		#return stalklist
		print('Done with Sub-Least Squares Assignment')
		
		
	#Assign suggested to all stalks	with dim>1
	def makeassignment(self, stalklist, suggested):
		originstalk = stalklist[len(stalklist)-1]
		queue = [originstalk]
		originstalk.section = suggested
		while(len(queue)>0):
			current = queue.pop(0)
			for stalk in current.outgoingstalks:
				if(stalk.dimension > 1):
					queue.append(stalk)
					#Do morphism
					stalk.section = current.outgoingmats[stalk]*current.section
		

		
	
	
	#Makes the assignment for the bottom
	def bottom(self, stalklist, measured):
		for idx, stalk in enumerate(stalklist):
			if(stalk.dimension == 1):
				stalk.section = measured[idx]


	#Find the values for measured quantities Least Squares suggests
	def extractsuggested(self, m, a, ls, constantmtx):
		mprime = a*ls[0]
		inverse = np.linalg.inv(constantmtx)
		suggested = -1*inverse*mprime
		return suggested

	#Do Least squares on our target stalk
	def doleastsquares(self, measured, equations):
	
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



	#Generates the tree made by following restrictions from the origin
	#Returns a stalklist
	def getstalklist(self, originstalk):
		stalklist = []
		queue = [originstalk]
		originstalk.visited = True


		while(len(queue) > 0):
			currentstalk = stack.pop()
			stalklist.append(currentstalk)
			for restrictedstalk in currentstalk.outgoingstalks:
				if(not(restrictedstalk.visited)):
					restrictedstalk.visited = True
					queue.append(restrictedstalk)
					#stalklist.append(restrictedstalk)
		return stalklist




	

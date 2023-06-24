import numpy as np
from stalk import Stalk


class MCS():
	#Algorithm to calculate maximal consistent subsections of sheaf
	#assignment. Should be given a complete stalklist (with assignment
	#and complete set of restriction morphisms
	
	def __init__(self, stalklist):
		print('Algorithm confirm launch')
		self.stalklist = stalklist

		#This is the important variable for the class --- each index
		#corresponds to a label. Within the label (idx) is a set
		#of stalks that are self consistent
		self.subsections = self.initsubsections()
		print('Starter subsections generated')
		for label, x in enumerate(self.subsections):
			print('Label: ', label, 'Stalk: ', x[0].name)


	def initsubsections(self):
		startersections = []
		count = 0
		for stalk in self.stalklist:
			if(stalk.dimension == 1):
				subsection = [stalk]
				startersections.append(subsection)
				stalk.label = count
				count = count + 1

		return startersections
		

	def iteration(self, dimension):
		print('')
		print('***********************************************')
		print('Performing iteration ', dimension)
		print('***********************************************')
		print('')

		
		stalklistd = []

		for stalk in self.stalklist:
			if(stalk.dimension == dimension):
				stalklistd.append(stalk)

		for x in stalklistd:
			restrictionvalues = []
			for y in x.incomingstalks:
				#print(y.outgoingmats[x])
				#print(y.section)
				restriction = y.outgoingmats[x]*(y.section)
				restrictionvalues.append(restriction)

			#print(restrictionvalues)

			

			#print('Evaluating query stalks:')
			#for y in x.incomingstalks:
				#print(y.name)

			addtolabel = self.consistencyfunctions(restrictionvalues, x.section)

			if(addtolabel):
				#print('Adding query stalks to MCS with variable: ', x.name, 'and Label: ', x.label)
				for y in x.incomingstalks: 
					if(y.label == -1):
						y.label = x.label

				#print('Checking if we need to merge')
				#Check if we need to merge. If so, merge
				stufftomerge = []
				for y in x.incomingstalks: 
					if(y.label != -1):
						stufftomerge.append(y.label)
						
				
				#print(stufftomerge)
	
				#filter out redundant labels
				mergeitems = np.unique(list(filter((x.label).__ne__, stufftomerge)))				
				#print(mergeitems)
				if(len(mergeitems) > 0):
					for section in mergeitems:
						#print('Merging subsection ', x.label, ' to subsection: ', section)
						for stalk in self.stalklist:
							if(stalk.label == x.label):
								stalk.label = section
						

				else:
					#X has a label, we want to make all the y
					#have that label
				

					#print('Did not need to merge')
					'''
			else:
				print('Query stalks not self-consistent')
					'''
			print('----------')
															

	def consistencyfunctions(self, restrictionvalues, expected):
		for x in restrictionvalues:
			#for y in restrictionvalues:
			# If the error between our section and morphism is 
			#larger that 5% error, we fail consistency
			if(np.linalg.norm(x-expected) > np.linalg.norm(expected)*.05):
				print('Failed consistency function-')
				print('Detrimental values: ', x,expected)
				print('Not consistent')
				return False
		print('Consistent')
		return True
	

	#Used for SmartAssignment. Tells us if everything is consistent
	def totallyconsistent(self):
		uniformlabel = stalklist[0].label
		for stalk in self.stalklist:
			if(stalk.label != uniformlabel):
				return False
			
		return True
		
		
				

	

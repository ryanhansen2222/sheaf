import random
import numpy as np


class DataGen():
	
	'''
	Statistically generates data for first n elements a given set of 
	linear equations. Does so by asuming starter values for 
	unmeasurable data elements, and using linear algebra to work
	backwards. At the end, adds noise (scaled with what? --> initial 
	extracted value. This makes sense because if our change was super
	small, we should expect the noise to be pretty small too)
	''' 


	def __init__(self, equations, unmeasvals, numreqmeas, numunmeas):
	
	#From our theory, we need msr matrix to be invtble, so we  
		#must have len(equations) measurements. Because of noise, 
		#there is a 0 probability matrix det is 0 therefore  
		# 0 probability msr matrix is not invtble 
		self.equations = equations
		self.numreqmeas = numreqmeas
		self.numunmeas = numunmeas
		self.truth = unmeasvals

   
	#Add gaussian noise to measurement, scaled by its own magnitude
	def noise(self, rawmeasurements):
			noisy = []
			for  measurement in rawmeasurements:
				#print(measurement[0,0])
				noisy.append(measurement[0,0]*(1+.05*random.gauss(0, 1)))
			return noisy 
	   
		
	def make_half_matricies(self):
			#HERE
			#Making the two parts - constant vect M (b) and variables mtx (A)
			chunk = self.numreqmeas 
			constant = []
			variables = []
			for eqtn in self.equations:
				consteqtn = []
				vareqtn = []
				for x in range(len(eqtn)):
						if(x < chunk):
							consteqtn.append(eqtn[x])
						else: 
							vareqtn.append(eqtn[x])
						 
				constant.append(consteqtn)
				variables.append(vareqtn)
			
			return np.matrix(constant), np.matrix(variables)

	
	def findrawmeas(self, meas, unmeas):
			#EQTN
			#original : [MU]mu = 0 

			#modified : m = [M]^(-1)[-U]u
			inversemeas = np.linalg.inv(meas)
			right = -unmeas * self.truth 

			rawmeasvals = inversemeas*right
			return rawmeasvals
		 
 
	  
	#Generate full set of synthetic data
	def synthesize(self):
			#Generate ground truth unmeasurable values
			#unmeasvect = self.make_unmeasurables()


			#Generate two matricies so we can synthesize values for meas
			meas, unmeas=self.make_half_matricies()

			#Generate synthetic measured values (RAW)
			rawmeasurements = self.findrawmeas(meas, unmeas)

			#Add noise to raw measurements
			noisy = self.noise(rawmeasurements)

			print('From equations: ', self.equations, 'And unmeasurables :', self.truth)
			print('Generated noisy data values: ', noisy)
			return noisy
			



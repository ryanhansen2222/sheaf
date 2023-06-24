import pysheaf as ps
import numpy as np
import copy

#Takes input reactions of form A + 2B --> C as
#-1 -2 1
def read_eqtn(filename) :
    fh = open(filename)
    result = []
    for l in fh.readlines():
        t = [(c) for (i,c) in enumerate(l.split())]#left i in in case we want for later
        #print(t)
        result.append(t)
    matrix = np.matrix(result)
    return np.transpose(matrix)
#return as the transpose (each column associated with a particular rate, as desired
#-1
#-2
#1


#For time being, input data is in form of
#1
#2
#3
#Name Measurement
def read_data(filename):
    fh = open(filename)
    result = []
    for l in fh.readlines():
        t = float(l)
        result.append(t)
    vector = np.matrix(result)
    return np.transpose(vector)
#return, column vector of assignments - row refers to metabolite -
#| 1 |
#| 2 |
#| 3 |
        
#Add structure and assignmens to sheaf
def make_sheaf(shf, data,eqtn,rates):
	#Adds metabolites to sheaf
	for i in range(data.size):
		shf.AddCell("M" + str(i),ps.Cell("Real Number",DistanceMeasurements,dataDimension=1))
		shf.GetCell("M" + str(i)).SetDataAssignment(ps.Assignment("Real Number",data[i]))
	# add reactions to sheaf
	for i in range(rates.size):
		shf.AddCell("R" + str(i),ps.Cell("Real Number",DistanceMeasurements,dataDimension=1))
		shf.GetCell("R" + str(i)).SetDataAssignment(ps.Assignment("Real Number",rates[i]))
	#Eqtns to sheaf : eqtns := 1 row per metabolite
	# 1 equation per metabolite, metabolite = sum of nonzero rates
	# equation in the form -1 + rates = 0
	for i in range(eqtn.shape[0]):
		support = [ (j, float(c_j)) for j, c_j in enumerate(eqtn[i,:].flat) \
			     if float(c_j) != 0 ]
		name = "E" + str(i)
		# data assignment = single metabolite measurement + rates
		assignment = \
		np.matrix( [float(data[i])] + \
		           [float(rates[j]) for (j,c_j) in support]).transpose()
		dataType = str(assignment.size) + "-Dimensional Vector"

		shf.AddCell(name,ps.Cell(dataType, DistanceMeasurements, \
		            dataDimension=assignment.size))
		shf.GetCell(name).SetDataAssignment(ps.Assignment(dataType,assignment))
	
		#AddMorphisms
		#Iterate through equation to determine metabolite in morphism
		# equation M = sum of rates, -M + sum of rates = 0
		cellNames = ["M" + str(i)] + ["R" + str(j) for j,c_j in support ]
		equation = [ -1 ] + [ c_j for j, c_j in support ]
		for (j,coefficient) in enumerate(equation):
			# turn -M + 2r1 + r2 into r1 = 1/2 M  + -1/2 r2
			projectionMorph = np.matrix(\
			[ float(c)/coefficient*(-1.0) if index != j else 0 \
			  for (index,c) in enumerate(equation) ])
			shf.AddCoface(name,cellNames[j],\
			ps.Coface(dataType,"Real Number",LinearMorphism(projectionMorph)))

def DistanceMeasurements(m1, m2):
    """Compute distance between two data measurements"""
    #im not sure which is which, but we should have some convention for m1 or m2 being first
    return np.linalg.norm(m2-m1)


class SetMorphism():
  """A morphism in a subcategory of Set, described by a function object"""
  def __init__(self,fcn):
      self.fcn=fcn

  def __mul__(self,other): # Composition of morphisms
      return SetMorphism(lambda x : self.fcn(other.fcn(x)))

  def __call__(self,arg): # Calling the morphism on an element of the set
      return self.fcn(arg)


class LinearMorphism(SetMorphism):
  """A morphism in a category that has a matrix representation"""
  def __init__(self,matrix):
      SetMorphism.__init__(self,lambda x: np.dot(matrix,x))

  def __mul__(self,other): # Composition of morphisms
      try: # Try to multiply matrices.  This might fail if the other morphism isn't a LinearMorphism
         return LinearMorphism(np.dot(other.matrix, self.matrix))
      except AttributeError:
         return SetMorphism.__mul__(self,other)
        

if __name__ == '__main__':

   print("+-+-+-+-+-+-+-+-+-+-+")
   print("+-Metabolites!-+")
   print("+-+-+-+-+-+-+-+-+-+-+")

   sheaf = ps.Sheaf()
   eqtn = read_eqtn("input.txt")
   dat = read_data("data.txt")
   rates = np.matrix([10,10]).transpose()
   make_sheaf(sheaf, dat, eqtn, rates)
   sheaf.MaximallyExtendCell("M0")
   sheaf.MaximallyExtendCell("M1")
   sheaf.MaximallyExtendCell("M2")
   sheaf.MaximallyExtendCell("M3")
   sheaf.MaximallyExtendCell("R0")
   sheaf.MaximallyExtendCell("E0")
   sheaf.MaximallyExtendCell("E1")
   sheaf.MaximallyExtendCell("E2")
   sheaf.MaximallyExtendCell("E3")
   print("for data: ")
   print(dat)
   print("for rates: ")
   print(rates)
   print("Consistency Radius! " + str(sheaf.ComputeConsistencyRadius()))

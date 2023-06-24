import numpy as np
from numpy import linalg as la

# dA = -r1 - r3
# dB =  r1 - r2
# dC =  r4 + r3
# dX =  r2 - r4

# Make stoichiometric matrix
A = [[-1, 0,-1, 0],
     [ 1,-1, 0, 0],
     [ 0, 0, 3, 1],
     [ 0, 1, 0,-1]]
A = np.array(A)

# u : unmeasured values (rates)
# m : measured values (metabolites)
u = np.array([7,3,67,4])
m =  np.dot(A , u.transpose())
print("true rates (u):",u)
print("true chngs (m):",m)

def pickSubsystem(rows,columns,rDim,cDim,measuredValues):
	R = A[rows,columns]
	R = R.reshape(rDim,cDim)
	print(R)
	print(measuredValues)
	u = la.lstsq(R,measuredValues,rcond=None)[0]
	consistentMeasured = np.dot(R,u)
	print("computed rates(u[1])",u)
	print("computed chngs(m[1,3])",m)

# make a susbsystem for each rate
rate = 1
def generateCoordinates(A,rate):
	rows = tuple([r for r in np.nonzero(A[:,rate])[0] ])
	col = tuple([ rate for index in rows ])
	return rows,col
r,c = generateCoordinates(A,1)

pickSubsystem(r,c,2,1,m[[1,3]])

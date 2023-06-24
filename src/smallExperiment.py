import numpy as np
from numpy import linalg as la

# dA = -r1 - r3
# dB =  r1 - r2
# dC =  r2 + r3

A = [[-1, 0,-1],
     [1 ,-1, 0],
     [0 , 1, 3]]
A = np.array(A)

Areduced = [[-1, 0],
            [1 ,-1],
            [0 , 1]]
Areduced = np.array(Areduced)

u = np.array([7,3,67])
m =  np.dot(A , u.transpose())

print("correct")
print("unmeasured: ",u)
print("measured: ",m)

print("reduced values")
# a @ x = b
ureduced =  la.lstsq(Areduced,m,rcond=None)
mconsistent = np.dot(Areduced , ureduced[0])
print("unmeasured: ",ureduced[0])
print("measured consistent: ",mconsistent)

firstPart = Areduced[0:2,:]
firstMeasured = m[0:2]
firstUnmeasured = la.lstsq(firstPart,firstMeasured,rcond=None)[0]
firstConsistent = np.dot(firstPart,firstUnmeasured)
print("A --> B")
print("first unmeasured (r1,r2)",firstUnmeasured)
print("first consistent (dA,dB)",firstConsistent)
print("first measured true (dA and dB)",firstMeasured)

secondPart = Areduced[1:,:]
secondMeasured = m[1:]
secondUnmeasured = la.lstsq(secondPart,secondMeasured,rcond=None)[0]
secondConsistent = np.dot(secondPart,secondUnmeasured)
print("B --> C")
print("second unmeasured (r1,r2)",secondUnmeasured)
print("second consistent (dB,dC)",secondConsistent)
print("second measured true (dB and dC)",secondMeasured)



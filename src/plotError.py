

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
#Plots Error
N = 15#data points per bar
numBars = 4
names = np.arange(numBars)
y = []
for l in open("genConRad.txt").readlines():
    y.append(float(l))
 
x = []
colors = np.random.rand(N)
graphcolors = []
for i in range(0,numBars):
    
    for j in range(0,N):
        x.append(i)
        graphcolors.append(colors[j])
    
print(x)

plt.scatter(x,y,s=10,c=graphcolors)
plt.xticks(names, ('Same', 'Add ConCom', 'Add Cycle', 'Remove ConCom'))
plt.ylabel('Consistency Radius')#Relative Error may be more useful here
plt.xlabel('Topology of Simulated Data')
plt.show()

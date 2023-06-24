import pysheaf
import numpy as np
from collections import defaultdict

"""
this version became obsolete with the newest version of pysheaf (20 march 2019)
"""
def main(simplices):
	k = pysheaf.AbstractSimplicialComplex(simplices)
	s = make_sheaf(k)
	print(len(s.cells))

def make_simplex(filename) :
	fh = open(filename)
	result = []
	for l in fh.readlines():
		t = [(i) for (i,c) in enumerate(l.split()) if int(c) != 0]
		result.append(tuple(t))
	return result

def make_sheaf(komplex):
	sheaf_cells = []
	for i, c in enumerate(komplex.cells) :
		cf = [pysheaf.SheafCoface(i,f.index,morph(i,f.index,komplex)) \
		for f in c.cofaces ]
		sc = pysheaf.SheafCell(dimension=1,\
		                       id=i,\
				       stalkDim=1,\
				       name=c.name,\
				       cofaces=cf)
		sheaf_cells.append(sc)
	return pysheaf.Sheaf(sheaf_cells)

# restriction from i into j
def morph(i,j,k):
	return np.matrix([1])

if __name__ == "__main__" :
	simplices = make_simplex("input.txt")
	main(simplices)

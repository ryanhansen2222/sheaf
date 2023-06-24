import random


class rxn :
        """
        This class represents a reaction.
        It has a metabolite list. [ (metabolite index, coefficient) ]
        It has a  method called run, that takes as input a list of metabolite
        concentrations and produces their new concentrations after one
        iteration of the reaction
        """
        metabolites = []
        def run(self,concentrations):
                for (i,c) in self.metabolites :
                        concentrations[i] += c+(c/50)*random.randint(-25,25)

def runCycle(reactions,concentrations,iterations) :
        n = 0
        while(n <  iterations):
                for r in reactions :
                        r.run(concentrations)
                n += 1
        return concentrations

if __name__ == "__main__" :
#       from sys import argv
        argv = ["ok","input.txt","data.txt"]

        reactions = []
        for l in open(argv[1]).readlines() :
                r = rxn()
                r.metabolites = [(i,int(c))for i,c in enumerate(l.split()) if c != 0]
                reactions.append(r)
        concentrations = [ float(m) for m in open(argv[2]).readlines() ]
        runCycle(reactions,concentrations,10)
        for c in concentrations :
                print(c)


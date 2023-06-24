import numpy as np


'''
This is the class responsible for generating the assignment we describe
in our paper. If we just calculate least squares for the entire system,
we can get bad fitting. This algorithm remedies that by calculating least
squares values for every stalk (either bottom up or top down) and finding 
the partition of the least number of maximally consistent subsections.
It accomplishes this by assuming smaller stalks are 'bigdaddy', and running
the least squares algorithm on them to create assignments. If the assignment
is consistent, as described by our MCS algorithm, we know at worst, the 
stalk we selected is part of a maximally consistent subsection - so we keep
moving up until we can't
'''

#Comment - Bottom up clearly eliminates solutions that are way off? 




class SmartAssignment():


    def __init__(self,stalklist, measured, equations):
        #Creates bottom level assignment
        self.equations = equations
        self.measured = measured
        for idx, stalk in enumerate(stalklist):
            if(stalk.dimension == 1):
                stalk.section = measured[idx]

    #Make bigdaddy stalklist
    def temp_stalklist(self, bigdaddy, shortmeasurement):
        variables = self.makevarnames(shortmeasurement)
        powerset = pw.powerset(variables)
        powerset.pop(0)
        stalklist = self.makestalks(powerset)
        self.makerestrictions(stalklist)

    #Helper for temp_stalklist - generates identity morphisms
    def makerestrictions(self, stalklist):
        for x in range(len(stalklist)):
            for y in range(x,len(stalklist)):
                low = stalklist[x]
                high = stalklist[y]
                if(low.dimension + 1 == high.dimension):

                    if(containsAll(low.name,high.name)):
                        othr, position = findmissing(low.name,high.name)
                        #print('Adding restriction ', high.n    ame, ' --> ', low.name)
                        low.add_incoming(high)
                        high.add_outgoing(low)
                        #newvar = findvarnum(othr)
                        mapping = findmapping(low.dimension,     high.dimension, position)

                        high.addrestriction(low,mapping)
        #return stalklist

        
    #Helper for temp_stalklist
    def makestalks(self, powerset):
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

        


    #Rename stalks for bigdaddy audition 
    def makevarnames(self, shortmeasurement):
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

        #print(variables)
        return (variables)


    #Helper function for getmeasuredidxs
    def findvarnum(variable):
        for x in range(len(variable)):
            if variable[x] == '1':
                return x
        return 0


    #Return list of indecies of the varibles we select for the given stalk
    #Pictorally, should just be the cols of variables/eqtns we use
    def getmeasuredidxs(self, stalk):
        variables = stalkname.split('(')
        idxstalk = []
        #print(variables)
        for idx, variable in enumerate(variables):
            if(idx != 0):
                variables[idx] = '(' + variable
                idxstalk.append(findvarnum(variables[idx])-1)
        return idxstalk
     

    #Find measured variables and equations from given stalk name
    def getparams(self, stalk):
        idxs = self.getmeasuredidxs(stalk)


        selectedvars = []
        for idx in idxs:
            selectedvars.append(self.measured[idx])



        #Find eqtns where there exist no nonzero values in spots
        #other than the idxs
        matrix = []
        for eqtn in self.equations:
            fail = False
            for queryidx in range(len(eqtn)):
                if(eqtn[queryidx] != 0 and (not(queryidx in idxs))):
                    fail = True 
            if(not fail):
                matrix.append(eqtn)

        #Delete extra cols:
        shrunkmatrix = []
        for eqtn in matrix:
            shrunkeqtn = []
            for idx in range(len(eqtn)):
                if(idx in idxs):
                    shrunkeqtn.append(eqtn[idx])
            shrunkmatrix.append(shrunkeqtn)

        '''
        shrunkmatrix = []
        for eqtn in matrix:
            shrunkmatrix.append(shrunkeqtn)

                
        return selectedvars, shrunkmatrix
        '''
                

            
        
        

    #Assume given stalk is big daddy. Do least squares and MCS on it
    def consistent_stalk(self, stalk):
        shrunkvars, shrunkmatrix = self.getparams(stalk)
        ministalklist = self.temp_stalklist(stalk, shrunkvars)
        LSAssignment(shrunkvars, shrunkmatrix, ministalklist)
        algo = MCS(ministalklist)

        for iteration in range(len(shrunkvars)):
            algo.iteration(iteration)
        return algo.totallyconsistent()

    #Runner function - tests all candidate stalks
    def test_sheaf(self, stalklist):
        candidate_cover_elements = []
        for stalk in stalklist:
            valid = self.consistent_stalk(stalk)    
            if(valid):
                candidate_cover_elements.append(stalk)

        #Now all we need to do is find the min cover
        mincover = []
        for element in candidate_cover_elements:
            :q

                
            
        
        
        
        
    #Input corresponding measurements and equations. 
    #Return a,m for least squares
    def gethalfmatricies(self,measured, equations):

        #Splitting eqtns matrix to measured + variables
        #Note: All measured vals must come first
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
        #print(measured)
        measuredvect = np.transpose(np.matrix(measured))
        m = -1 * constantmtx * measuredvect

        #Adding extra rows for underdefined matrix to make least sq
        #print('Adding dummy rows in matrix to make least squares work')
        while(len(variables) < len(variables[0])):
            variables.append([0 for x in range(len(variables[0]))])


        a = np.matrix(variables)

        return a,m

 

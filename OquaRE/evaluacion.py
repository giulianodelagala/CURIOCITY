#Evaluacion OQuaRE

from metricas import Metricas
import numpy as np
import pandas as pd

class Evaluacion:
    def __init__(self, onto):
        self.M = Metricas(onto)
        self.LCOMOnto = []
        self.WMCOnto2 = []
        self.DITOnto = []
        self.NACOnto = []
        self.NOCOnto = []
        self.CBOOnto = []
        self.RFCOnto = []
        self.NOMOnto = []
        self.RROnto = []
        self.PROnto = []
        self.AROnto = []
        self.INROnto = []
        self.ANOnto = []
        self.TMOnto2 = []

        self.setValues() #Set metrics
        self.setScore() #Set score
        self.EvalStructural()
        self.EvalFunctionalAdequacy()
        self.EvalARRO()
        self.EvalMaintainability()
        self.EvalCharacteristics()

    def setValues(self):
        #set values to metrics
        self.LCOMOnto.append(self.M.LCOMOnto())
        self.WMCOnto2.append(self.M.WMCOnto2())
        self.DITOnto.append(self.M.DITOnto())
        self.NACOnto.append(self.M.NACOnto())
        
        self.NOCOnto.append(self.M.NOCOnto())
        self.CBOOnto.append(self.M.CBOOnto())
        self.RFCOnto.append(self.M.RFCOnto())
        self.NOMOnto.append(self.M.NOMOnto())

        self.RROnto.append(self.M.RROnto())
        self.PROnto.append(self.M.PROnto())
        self.AROnto.append(self.M.AROnto())

        self.INROnto.append(self.M.INROnto())
        self.ANOnto.append(self.M.ANOnto())
        self.TMOnto2.append(self.M.TMOnto2())

    def setScore(self):
        if (self.LCOMOnto[0] <= 2):
            self.LCOMOnto.append(5)
        elif (self.LCOMOnto[0] > 2 and self.LCOMOnto[0] <=4):
            self.LCOMOnto.append(4)
        elif (self.LCOMOnto[0] > 4 and self.LCOMOnto[0] <=6):
            self.LCOMOnto.append(3)
        elif (self.LCOMOnto[0] > 6 and self.LCOMOnto[0] <=8):
            self.LCOMOnto.append(2)
        else:
            self.LCOMOnto.append(1)
        ##########################
        if (self.WMCOnto2[0] <= 5):
            self.WMCOnto2.append(5)
        elif (self.WMCOnto2[0] > 5 and self.WMCOnto2[0] <=8):
            self.WMCOnto2.append(4)
        elif (self.WMCOnto2[0] > 8 and self.WMCOnto2[0] <=11):
            self.WMCOnto2.append(3)
        elif (self.WMCOnto2[0] > 11 and self.WMCOnto2[0] <=15):
            self.WMCOnto2.append(2)
        else:
            self.WMCOnto2.append(1)
        ##########################
        if (self.DITOnto[0] >= 1 and self.DITOnto[0] <= 2):
            self.DITOnto.append(5)
        elif (self.DITOnto[0] > 2 and self.DITOnto[0] <=4):
            self.DITOnto.append(4)
        elif (self.DITOnto[0] > 4 and self.DITOnto[0] <=6):
            self.DITOnto.append(3)
        elif (self.DITOnto[0] > 6 and self.DITOnto[0] <=8):
            self.DITOnto.append(2)
        else: #>8
            self.DITOnto.append(1)
        ################################################
        if (self.NACOnto[0] >= 1 and self.NACOnto[0] <= 2):
            self.NACOnto.append(5)
        elif (self.NACOnto[0] > 2 and self.NACOnto[0] <=4):
            self.NACOnto.append(4)
        elif (self.NACOnto[0] > 4 and self.NACOnto[0] <=6):
            self.NACOnto.append(3)
        elif (self.NACOnto[0] > 6 and self.NACOnto[0] <=8):
            self.NACOnto.append(2)
        else: #>8
            self.NACOnto.append(1)
        ###############################################
        if (self.NOCOnto[0] >= 1 and self.NOCOnto[0] <= 3):
            self.NOCOnto.append(5)
        elif (self.NOCOnto[0] > 3 and self.NOCOnto[0] <=6):
            self.NOCOnto.append(4)
        elif (self.NOCOnto[0] > 6 and self.NOCOnto[0] <=8):
            self.NOCOnto.append(3)
        elif (self.NOCOnto[0] > 8 and self.NOCOnto[0] <=12):
            self.NOCOnto.append(2)
        else: #>12
            self.NOCOnto.append(1)
        ###############################################
        if (self.CBOOnto[0] >= 1 and self.CBOOnto[0] <= 2):
            self.CBOOnto.append(5)
        elif (self.CBOOnto[0] > 2 and self.CBOOnto[0] <=4):
            self.CBOOnto.append(4)
        elif (self.CBOOnto[0] > 4 and self.CBOOnto[0] <=6):
            self.CBOOnto.append(3)
        elif (self.CBOOnto[0] > 6 and self.CBOOnto[0] <=8):
            self.CBOOnto.append(2)
        else: #>8
            self.CBOOnto.append(1)
        ###############################################
        if (self.RFCOnto[0] >= 1 and self.RFCOnto[0] <= 3):
            self.RFCOnto.append(5)
        elif (self.RFCOnto[0] > 3 and self.RFCOnto[0] <=6):
            self.RFCOnto.append(4)
        elif (self.RFCOnto[0] > 6 and self.RFCOnto[0] <=8):
            self.RFCOnto.append(3)
        elif (self.RFCOnto[0] > 8 and self.RFCOnto[0] <=12):
            self.RFCOnto.append(2)
        else: #>12
            self.RFCOnto.append(1)
        ###############################################
        if (self.NOMOnto[0] <= 2):
            self.NOMOnto.append(5)
        elif (self.NOMOnto[0] > 2 and self.NOMOnto[0] <=4):
            self.NOMOnto.append(4)
        elif (self.NOMOnto[0] > 4 and self.NOMOnto[0] <=6):
            self.NOMOnto.append(3)
        elif (self.NOMOnto[0] > 6 and self.NOMOnto[0] <=8):
            self.NOMOnto.append(2)
        else: #>8
            self.NOMOnto.append(1)
        ###############################################
        if (self.RROnto[0] > 0.8):
            self.RROnto.append(5)
        elif (self.RROnto[0] > 0.6 and self.RROnto[0] <=0.8):
            self.RROnto.append(4)
        elif (self.RROnto[0] > 0.4 and self.RROnto[0] <=0.6):
            self.RROnto.append(3)
        elif (self.RROnto[0] > 0.2 and self.RROnto[0] <=0.4):
            self.RROnto.append(2)
        else: #>=0 <=0.2
            self.RROnto.append(1)
        ###############################################
        if (self.PROnto[0] > 0.8):
            self.PROnto.append(5)
        elif (self.PROnto[0] > 0.6 and self.PROnto[0] <=0.8):
            self.PROnto.append(4)
        elif (self.PROnto[0] > 0.4 and self.PROnto[0] <=0.6):
            self.PROnto.append(3)
        elif (self.PROnto[0] > 0.2 and self.PROnto[0] <=0.4):
            self.PROnto.append(2)
        else: #>=0 <=0.2
            self.PROnto.append(1)
        ###############################################
        if (self.AROnto[0] > 0.8):
            self.AROnto.append(5)
        elif (self.AROnto[0] > 0.6 and self.AROnto[0] <=0.8):
            self.AROnto.append(4)
        elif (self.AROnto[0] > 0.4 and self.AROnto[0] <=0.6):
            self.AROnto.append(3)
        elif (self.AROnto[0] > 0.2 and self.AROnto[0] <=0.4):
            self.AROnto.append(2)
        else: #>=0 <=0.2
            self.AROnto.append(1)
        ###############################################
        if (self.INROnto[0] > 0.8):
            self.INROnto.append(5)
        elif (self.INROnto[0] > 0.6 and self.INROnto[0] <=0.8):
            self.INROnto.append(4)
        elif (self.INROnto[0] > 0.4 and self.INROnto[0] <=0.6):
            self.INROnto.append(3)
        elif (self.INROnto[0] > 0.2 and self.INROnto[0] <=0.4):
            self.INROnto.append(2)
        else: #>=0 <=0.2
            self.INROnto.append(1)
        ###############################################
        if (self.ANOnto[0] > 0.8):
            self.ANOnto.append(5)
        elif (self.ANOnto[0] > 0.6 and self.ANOnto[0] <=0.8):
            self.ANOnto.append(4)
        elif (self.ANOnto[0] > 0.4 and self.ANOnto[0] <=0.6):
            self.ANOnto.append(3)
        elif (self.ANOnto[0] > 0.2 and self.ANOnto[0] <=0.4):
            self.ANOnto.append(2)
        else: #>=0 <=0.2
            self.ANOnto.append(1)
        ###############################################
        if (self.TMOnto2[0] >= 1 and self.TMOnto2[0] <= 2):
            self.TMOnto2.append(5)
        elif (self.TMOnto2[0] > 2 and self.TMOnto2[0] <=4):
            self.TMOnto2.append(4)
        elif (self.TMOnto2[0] > 4 and self.TMOnto2[0] <=6):
            self.TMOnto2.append(3)
        elif (self.TMOnto2[0] > 6 and self.TMOnto2[0] <=8):
            self.TMOnto2.append(2)
        else: #>8
            self.TMOnto2.append(1)
        ###############################################

    def ShowScore(self):
        metric = ['LCOMOnto', 'WMCOnto2', 'DITOnto', 'NACOnto', 
            'NOCOnto', 'CBOOnto', 'RFCOnto', 'NOMOnto',
            'RROnto', 'PROnto', 'AROnto',
            'INROnto', 'ANOnto', 'TMOnto2']
        value = [self.LCOMOnto[0], self.WMCOnto2[0], self.DITOnto[0], self.NACOnto[0],
            self.NOCOnto[0], self.CBOOnto[0], self.RFCOnto[0], self.NOMOnto[0],
            self.RROnto[0], self.PROnto[0], self.AROnto[0],
            self.INROnto[0], self.ANOnto[0], self.TMOnto2[0] ]
        score = [self.LCOMOnto[1], self.WMCOnto2[1], self.DITOnto[1], self.NACOnto[1],
            self.NOCOnto[1], self.CBOOnto[1], self.RFCOnto[1], self.NOMOnto[1],
            self.RROnto[1], self.PROnto[1], self.AROnto[1],
            self.INROnto[1], self.ANOnto[1], self.TMOnto2[1] ]

        return pd.DataFrame(zip(value, score) , index = metric, columns=['Value','Score'])
        '''
        print("LCOMOnto" , self.LCOMOnto[0], "sc: ", self.LCOMOnto[1])
        print("WMCOnto2" , self.WMCOnto2[0], "sc: ", self.WMCOnto2[1])
        print("DITOnto", self.DITOnto[0], "sc: ", self.DITOnto[1])
        print("NACOnto", self.NACOnto[0], "sc: ", self.NACOnto[1])

        print("NOCOnto", self.NOCOnto[0], "sc: ", self.NOCOnto[1])      
        print("CBOOnto", self.CBOOnto[0], "sc: ", self.CBOOnto[1])
        print("RFCOnto", self.RFCOnto[0], "sc: ", self.RFCOnto[1])
        print("NOMOnto", self.NOMOnto[0], "sc: ", self.NOMOnto[1])

        print("RROnto", self.RROnto[0], "sc: ", self.RROnto[1])
        print("PROnto", self.PROnto[0], "sc: ", self.PROnto[1])
        print ("AROnto", self.AROnto[0], "sc: ", self.AROnto[1])

        print ("INROnto", self.INROnto[0], "sc: ", self.INROnto[1])
        print("ANOnto", self.ANOnto[0], "sc: ", self.ANOnto[1])
        print("TMOnto2", self.TMOnto2[0], "sc: ", self.TMOnto2[1])
        '''

    def EvalStructural(self):

        frs = self.RROnto[1] #Formal relations support
        cohesion = self.LCOMOnto[1]
        tangledness = self.TMOnto2[1]
        redundancy = self.ANOnto[1]
        self.formalization = 5 #Change according to evaluation
        self.consistency = 5 #Change according to evaluation

        self.sub_struct = ['Formal relations', 'Cohesion', 'Tangledness', 'Redundancy', 'Formalization', 'Consistency']
        self.score_struct = [frs,cohesion,tangledness,redundancy, self.formalization, self.consistency, frs] #Repeat first for graphics

    def EvalFunctionalAdequacy(self):
        #Functional adequacy
        cv = self.ANOnto[1] #Controlled vocabulary
        scv = (self.RROnto[1] + self.AROnto[1] + self.formalization + self.consistency)/4.0 #Schema and value reconciliation 
        csq = (self.ANOnto[1] + self.RROnto[1] + self.AROnto[1] + self.INROnto[1] + self.formalization)/5.0 #Consistent search and query
        ka = (self.ANOnto[1] + self.RROnto[1] + self.NOMOnto[1])/3.0 #Knowledge acquisition
        cs = (self.RROnto[1] + self.AROnto[1])/2.0 #Clustering and similiraty
        il = (self.RROnto[1] + self.AROnto[1] + self.INROnto[1])/3.0 #Indexing and linking
        rr = (self.AROnto[1] + 0)/2.0 #Results representation
        ta = (self.formalization) #Text analysis
        gdt = (self.INROnto[1] + self.AROnto[1])/2.0 #Guidance and decision trees
        kr = (self.ANOnto[1] + self.AROnto[1] + self.INROnto[1] + self.formalization + self.NOMOnto[1] + self.LCOMOnto[1] + self.consistency)/7.0 #Knowledge reuse

        self.sub_fa = ['Controlled\n vocabulary', 'Schema &\n value reconciliation', 'Consistent\n Search & Query',
         'Knowledge\n acquisition', 'Clustering &\n similiraty', 'Indexing &\n linking', 'Results\n representation',
          'Text analysis', 'Guidance &\n decision trees', 'Knowledge\n reuse']
        self.score_fa = [cv, scv, csq, ka, cs, il, rr, ta, gdt, kr, cv]

    def EvalARRO(self):
        #Adaptability
        self.adaptability = (self.WMCOnto2[1] + self.DITOnto[1] + self.RFCOnto[1] + self.CBOOnto[1])/4.0
        #Reliability
        self.recoverability = (self.WMCOnto2[1] + self.DITOnto[1] + self.NOMOnto[1] + self.LCOMOnto[1])/4.0
        self.availability = self.LCOMOnto[1]
        #  Replaceability
        self.replaceability = (self.WMCOnto2[1] + self.DITOnto[1] + self.NOCOnto[1] + self.NOMOnto[1])/4.0
        #  Operability
        learnability = (self.WMCOnto2[1] + self.LCOMOnto[1] + self.RFCOnto[1] + self.NOMOnto[1] + self.CBOOnto[1] + self.NOCOnto[1])/6.0

        self.sub_arro = ['Adaptability', 'Recoverability', 'Availability', 'Replaceability', 'Learnability']
        self.score_arro = [self.adaptability, self.recoverability, self.availability, self.replaceability, learnability, self.adaptability]

    def EvalMaintainability(self):
        modularity = (self.WMCOnto2[1] + self.CBOOnto[1])/2.0
        reusability = (self.WMCOnto2[1] + self.DITOnto[1] + self.NOCOnto[1] + self.RFCOnto[1] + self.NOMOnto[1] + self.CBOOnto[1])/6.0
        analysability = (self.WMCOnto2[1] + self.DITOnto[1] + self.LCOMOnto[1] + self.RFCOnto[1] + self.NOMOnto[1] + self.CBOOnto[1])/6.0
        changeability = (self.WMCOnto2[1] + self.DITOnto[1] + self.LCOMOnto[1] + self.RFCOnto[1] + self.NOMOnto[1] + self.CBOOnto[1] + self.NOCOnto[1])/7.0
        mo_stability = (self.WMCOnto2[1] + self.CBOOnto[1] + self.LCOMOnto[1] + self.RFCOnto[1] + self.NOCOnto[1])/5.0 #modification stability
        testability = (self.WMCOnto2[1] + self.DITOnto[1] + self.LCOMOnto[1] + self.RFCOnto[1] + self.NOMOnto[1] + self.CBOOnto[1])/6.0

        self.sub_maintain = ['Modularity', 'Reusability', 'Analysability', 'Changeability', 'Modification\nStability', 'Testability']
        self.score_maintain = [modularity, reusability, analysability, changeability, mo_stability, testability, modularity]

    def EvalCharacteristics(self):
        #Characteristic
        structural = np.mean(self.score_struct[:-1])
        func_adequacy = np.mean(self.score_fa[:-1]) #Functional adequacy
        #adaptability 
        reliability = (self.recoverability + self.availability)/2.0
        #replaceability
        maintainability = np.mean(self.score_maintain[:-1])

        self.sub_char = ['Structural', 'Functional\nadequacy', 'Adaptability', 'Reliability', 'Replaceability', 'Maintainability']
        self.score_char = [structural, func_adequacy, self.adaptability, reliability, self.replaceability, maintainability, structural]

if __name__ == "__main__":

    E = Evaluacion("../Curiocity_Turtle.owl")
    print(E.ShowScore())
import regulator

#===============================================================================
#===============================================================================
#Gene simulation
#===============================================================================
#Run the simulation of one gene transcription 
#Setup with the integration method for this transcription
#The integrator object sets the size of x_sim which is the number 
#  of previous points needed for the integration method
#===============================================================================
class simulateGene:
    def __init__(self,integrator):
        self.regulators = []
        self.integrator = integrator
        self.x_sim = self.integrator.get_X_history
        self.plot_x = []
        self.plot_t = []
    def addRegulator(self,regulator):
        regulators.append(regulator)
    def timeStep(x):
        self.integrator(self,x,self.regulators)
#    def plot(window)
#===============================================================================
#Gene simulation
#===============================================================================
#===============================================================================

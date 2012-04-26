import math

#===============================================================================
#Repressor/activator computation
#===============================================================================
#All are unitless so we can handle units at a higher level
#===============================================================================
def reg_Activator(x,k,n,reg):
    return 1/(1+math.pow(k/x,n))
def reg_Repressor(x,k,n):
    return 1/(1+math.pow(x/k,n))
def reg_Decay(x,k,n,reg):
    return x
def reg_None(x,k,n):
    return 0

#===============================================================================
#===============================================================================
#Regulation functor
#===============================================================================
#The return value of the functor has units
#===============================================================================
class regulation:
    #====================
    #constructor
    #====================
    def __init__(self):
        self.set_Interaction_Index()
        self.set_Interaction_Type()
        self.set_K()
        self.set_N()
        self.set_RateConstant()
    #====================
    #Set internals
    #====================
    #sets internal values
    #default index is -1 for maximal explosions
    #====================        
    def set_InteractionIndex(self,i = -1):
        self.interactionIndex = i
    def set_K(self,k = 1):
        self.k = k
    def set_N(self,n = 1):
        self.n = n
    def set_InteractionType(interaction_Type = reg_None):
        self.interaction_Type = interaction_Type
    def set_RateConstant(self,rate_Constant = 0):
        self.rate_Constant = rate_Constant
    
    def set(self,interaction_Index,k,n,interaction_Type,rate_Constant):
        self.set_InteractionIndex(interaction_Index)
        self.set_K(k)
        self.set_N(n)        
        self.set_Interaction_Type(interaction_Type)

    #====================
    #functor operator()  
    #====================      
    #returns production rate
    #====================      
    def __call__(self,x):
        return (self.rate_Constant * 
                self.interaction(x[self.interactionIndex],
                                 self.k,
                                 self.n))
#===============================================================================
#Regulation functor
#===============================================================================
#===============================================================================

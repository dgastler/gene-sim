import math

#===============================================================================
#Repressor/activator computation
#===============================================================================
#All are unitless so we can handle units at a higher level
#===========================================================o====================
def regfunc_None(x,k,n):
    return 0
def regfunc_Activator(x,k,n,reg):
    return 1/(1+math.pow(k/x,n))
def regfunc_Repressor(x,k,n):
    return 1/(1+math.pow(x/k,n))
def regfunc_Decay(x,k,n,reg):
    return x

regtypes = ["reg_None","reg_Activator","reg_Repressor","reg_Decay"]
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
        self.set_Name()
        self.set_Interaction_Index()
        self.set_Interaction_Type()
        self.set_K()
        self.set_N()
        self.set_Rate_Constant()
    #====================
    #Set internals
    #====================
    #sets internal values
    #default index is -1 for maximal explosions
    #====================        
    def set_Name(self,name = "X"):
        self.name = name
    def set_Interaction_Index(self,i = -1):
        self.interactionIndex = i
    def set_K(self,k = 1):
        self.k = k
    def set_N(self,n = 1):
        self.n = n
    def set_Interaction_Type(self,interaction_Type = "reg_None"):
        #set the internal interaction type (defaults to reg_None on error)
        self.interaction_Type = interaction_Type  

        #set the actual interaction function "pointer"
        if(self.interaction_Type == "reg_Activator"):    
            self.interaction_Function = regfunc_Activator
        elif(self.interaction_Type == "reg_Repressor"):   
            self.interaction_Function = regfunc_Repressor  
        elif(self.interaction_Type == "reg_Decay"): 
            self.interaction_Function = regfunc_Decay  
        else:
            #if the user gave us something dumb, set interaction
            #to reg_None
            self.interaction_Type = "reg_None"
            self.interaction_Function = regfunc_None

    def set_Rate_Constant(self,rate_Constant = 0):
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

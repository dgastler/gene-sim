import string

#gobject to give class signals
import gobject

#graphica elements of genes
from gene_element import *

#===============================================================================
#===============================================================================
#Gene Collection
#===============================================================================
class Gene_Collection(gobject.GObject):
    #====================
    #Custom signals
    #====================
    __gsignals__ = {
        "element-update-signal": (gobject.SIGNAL_RUN_FIRST, 
                                  gobject.TYPE_NONE, 
                                  (str,str )),
        }
    
    #====================
    #constructor
    #====================
    def __init__(self,design_Area):
        #initialize gObject and connect up signals
        gobject.GObject.__init__(self)
        self.connect("element-update-signal",self.Process_Update)
        
        self.design_Area = design_Area

        #list of gene_elements (graphical)
        self.element_list = []

        #list of genes (simulation)
        self.sim_list = []

    def Add_New(self,event):
        #Add a new blank gene element
        self.element_list.append(Gene_Element(self,
                                              event.x,event.y))

    def Process_Update(self,widget,update_Type,data):
        print update_Type,data
        if(update_Type == "name-change"):
            #break up name change
            names = string.split(data,":")
            #update all the gene_elements
            for element in self.element_list:
                element.update_Interaction(names[0],names[1])
    
#    def Build_Simulation(self):
#        
#        for element in self.element_list:
#            self.sim_list.append(element.name)
#        for i in range(len(self.element_list)):
            

#    def Redraw_Network(self):
#        style = self.design_Area.get_style()
#        gc = style.style.fg_gc[gtk.STATE_NORMAL]
#        for element in self.element_list:
#            self.design_Area.draw_line(element
                    
        

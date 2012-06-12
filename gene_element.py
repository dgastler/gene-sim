import pygtk
pygtk.require('2.0')
import gtk

#for gene regulator class
from regulator import *
from gene_settings import *

#===============================================================================
#===============================================================================
#gene element container
#===============================================================================
#This class deals with the visuals for a gene.
class Gene_Element_GUI:
    def __init__(self,gene_collection,screen_pos_x=0,screen_pos_y=0):                
        #Properties
        self.name = "X"
        self.regulation_Interactions = []

        #Graphics
        self.selected = False
        self.moving = 0
        self.x = screen_pos_x
        self.y = screen_pos_y
        
        #Fixed container this is in
        self.gene_collection = gene_collection
        
        #event box for the frame
        self.ebox = gtk.EventBox()        
        self.gene_collection.design_Area.put(self.ebox,
                                             int(self.x),
                                             int(self.y))
        self.frame = gtk.Frame("")
        self.update_Frame_Name()

        
        #connect signal handlers
        self.ebox.connect("button-press-event", self.press_button,"")
        self.ebox.connect("button-release-event",self.release_button,"")
        self.ebox.connect("motion-notify-event",self.mouse_movement,"")
        #look up _2BUTTON_PRESS event

        #add frame to ebox and show everything
        self.ebox.add(self.frame)
        self.frame.show()
        self.ebox.show()
        
    #====================
    #Mouse interactions
    #====================
    def press_button(self, widget,event,data=None):
        print 'test %d\n' % event.button
        if(event.button == 1):            
            self.toggle_Select()
        elif(event.button == 3):
            #adding a new interaction to the Gene_object
            gene_settings = Gene_Settings(self.gene_collection,self)


    def mouse_movement(self,widget, event,data=None):
        #move widget with the mouse
            #moving the gene_object
        if(self.moving != 1): 
            #since we are moving, we want to undo, the toggle select we just did
            #from press_button
            self.toggle_Select()      
            self.moving = 1        
        if(self.moving == 1):
            self.x += event.x
            self.y += event.y
            self.gene_collection.design_Area.move(widget,
                                             int(self.x),int(self.y))
            
    def release_button(self,widget,event,data=None):
        if(event.button == 1):
            if(self.moving == 1):
                #handle repositioning the moving gene
                self.moving = 0
                self.x += event.x
                self.y += event.y
                self.gene_collection.design_Area.move(widget,
                                                 int(self.x),int(self.y))


    #====================
    #Visual element manipulation
    #====================
    def update_Frame_Name(self):
        label_text = ""
        for interaction in self.regulation_Interactions:            
            if(interaction.interaction_Type == "reg_Activator"):
                label_text += "[" + interaction.name + "]   "
            elif(interaction.interaction_Type == "reg_Repressor"):
                label_text += "]" + interaction.name + "[   "
        label_text += "Gene:" + self.name
        self.frame.set_label(label_text)                   


    def toggle_Select(self):
        self.selected = not self.selected
        if(self.selected):
            self.frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        else:
            self.frame.set_shadow_type(gtk.SHADOW_ETCHED_IN)

    


    def set_Name(self,name):
        self.name = name

    #====================
    #External calls
    #====================

    def update_Interaction(self,old,new):
        for i in range(len(self.regulation_Interactions)):
            if(self.regulation_Interactions[i].name == old):
                self.regulation_Interactions[i].se_Name(new)
        self.update_Frame_Name()
            

#===============================================================================
#gene element container
#===============================================================================
#===============================================================================

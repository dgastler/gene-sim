import pygtk
pygtk.require('2.0')
import gtk

#for gene regulator class
from regulator import *

#===============================================================================
#===============================================================================
#gene element container
#===============================================================================
class Gene_Element:
    def __init__(self,collection,x=0,y=0):                
        #Properties
        self.name = "X"
        self.regulation_Interactions = []

        #Graphics
        self.selected = False
        self.moving = 0
        self.x = x
        self.y = y
        
        #Fixed container this is in
        self.collection = collection
        
        #event box for the frame
        self.ebox = gtk.EventBox()        
        self.collection.design_Area.put(self.ebox,
                                        int(self.x),int(self.y))

        self.frame = gtk.Frame("")
        self.update_Frame_Name()

        
        #connect signal handlers
        self.ebox.connect("button-press-event", self.press_button,"")
        self.ebox.connect("button-release-event",self.release_button,"")
        self.ebox.connect("motion-notify-event",self.mouse_movement,"")

        #add frame to ebox and show everything
        self.ebox.add(self.frame)
        self.frame.show()
        self.ebox.show()

        #add menu for right click
        self.menu = gtk.Menu()
        add_Interaction_Item = gtk.MenuItem("Add Interaction")
        self.menu.append(add_Interaction_Item)
        add_Interaction_Item.connect("activate",                                     
                                     self.add_Interaction)
        add_Interaction_Item.show()

        set_Name_Item = gtk.MenuItem("Set Name")
        self.menu.append(set_Name_Item)
        set_Name_Item.connect("activate",
                              self.set_Name)
        set_Name_Item.show()


    #====================
    #Mouse interactions
    #====================
    def press_button(self, widget,event,data=None):
        if(event.button == 1):            
            self.toggle_Select()
        elif(event.button == 2):
            #adding a new interaction to the Gene_object
            self.menu.popup(None, None, None, event.button, event.time)


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
            self.collection.design_Area.move(widget,
                                             int(self.x),int(self.y))
            
    def release_button(self,widget,event,data=None):
        if(event.button == 1):
            if(self.moving == 1):
                #handle repositioning the moving gene
                self.moving = 0
                self.x += event.x
                self.y += event.y
                self.collection.design_Area.move(widget,
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

    
    #====================
    #Visual element manipulation
    #====================

    def add_Menu_Item(self,menu,name,callback):
        menu_item = gtk.MenuItem(name)
        menu.append(menu_item)
        menu_item.connect("activate",callback)
        menu_item.show()
        
    def make_Text_Entry(self,signal_name,text,callback):
        text_entry = gtk.Entry()
        text_entry.set_max_length(25)
        if(callback != None):
            text_entry.connect(signal_name,callback,text_entry)
        text_entry.set_text(text)
        text_entry.select_region(0,len(text_entry.get_text()))
        text_entry.set_editable(True)
        text_entry.show()        
        return text_entry

    #====================
    #Menu: add interaction
    #====================
    def add_Interaction(self,entry):
        #create a new interaction
        new_Interaction = regulation()
        #create window for user input
        new_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        new_window.set_size_request(80,80)
        new_window.set_title("Add Interaction")
        #primary vbox
        window_VBox = gtk.VBox()        
        #create text box (it gets a row to itself
        name = self.make_Text_Entry("changed",
                                    "X",
                                    None
                                    )
        window_VBox.pack_start(name)
        #hboxs for the rest of the options
        window_HBox1 = gtk.HBox()
        rate = self.make_Text_Entry("changed",
                                    "0",                                    
                                    None
                                    )
        rate.show()
        regK = self.make_Text_Entry("changed",
                                    "0",                                    
                                    None
                                    )
        regK.show()
        window_HBox1.pack_start(rate)
        window_HBox1.pack_start(regK)
        window_HBox1.show()
        window_VBox.pack_start(window_HBox1)

        window_HBox2 = gtk.HBox()
        regType = self.make_Text_Entry("changed",
                                       "reg_Activator",                                       
                                       None
                                       )
        regType.show()
        regN = self.make_Text_Entry("changed",
                                    "1",                                    
                                    None
                                    )
        regN.show()
        window_HBox2.pack_start(regType)
        window_HBox2.pack_start(regN)
        window_HBox2.show()
        window_VBox.pack_start(window_HBox2)
        #add add button
        add_button = gtk.Button("Add")
        add_button.connect("clicked",
                           self.add_Interaction_Callback,
                           new_Interaction,
                           name,rate,regK,regType,regN)
        add_button.connect("clicked",
                           lambda w:new_window.destroy())    
        add_button.show();
        window_VBox.pack_start(add_button)
        window_VBox.show()
        new_window.add(window_VBox)
        new_window.show()   
      
    def add_Interaction_Callback(self,widget,new_interaction,name,rate,regK,regType,regN):
        new_interaction.set_Name(name.get_text())
        new_interaction.set_Rate_Constant(rate.get_text())
        new_interaction.set_K(regK.get_text())
        new_interaction.set_Interaction_Type(regType.get_text())
        new_interaction.set_N(regN.get_text())
        self.collection.emit("element-update-signal",
                             "interaction-change",
                             "+"+new_interaction.name)
        self.regulation_Interactions.append(new_interaction)
        self.update_Frame_Name()

    #====================
    #Menu: change name
    #====================

    def set_Name(self,widget):        
        #create window for user input
        new_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        new_window.set_size_request(80,50)
        new_window.set_title("Change Name")
        #create text box
        text = self.make_Text_Entry("activate",
                                    self.name,                                    
                                    self.set_Name_Callback)
        text.connect("activate", lambda w: new_window.destroy())       
        new_window.add(text)

                             
        new_window.show()         
    def set_Name_Callback(self,widget,entry):        
        self.collection.emit("element-update-signal",
                             "name-change",
                             self.name + ":" + entry.get_text())
        self.name = entry.get_text()
        self.update_Frame_Name()                


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

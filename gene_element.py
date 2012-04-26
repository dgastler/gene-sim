import pygtk
pygtk.require('2.0')
import gtk


#===============================================================================
#===============================================================================
#gene element container
#===============================================================================
class Gene_Element:
#    def __init__(self,fixed,gene_object_list,x=0,y=0):
    def __init__(self,fixed,x=0,y=0):
        
        #Properties
        self.name = "X"
        self.interactions = []

        #Graphics
        self.selected = False
        self.moving = 0
        self.x = x
        self.y = y
        
        #Fixed container this is in
        self.fixed = fixed
        
        #event box for the frame
        self.ebox = gtk.EventBox()        
        self.fixed.put(self.ebox,
                       int(self.x),int(self.y))

        self.frame = gtk.Frame("")
        self.set_Frame_Name()

        
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
        self.add_Menu_Item(self.menu,"Add Interaction",self.add_Interaction)
        self.add_Menu_Item(self.menu,"Set Name",self.set_Name)


    def set_Frame_Name(self):
        label_text = ""
        for i in range(len(self.interactions)):
            label_text += "[" + self.interactions[i] + "]   "
        label_text += "Gene:" + self.name
        self.frame.set_label(label_text)                   

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
#            self.x += event.x
#            self.y += event.y                
        if(self.moving == 1):
            self.x += event.x
            self.y += event.y
            self.fixed.move(widget,
                            int(self.x),int(self.y))
                    
    def release_button(self,widget,event,data=None):
        if(event.button == 1):
            if(self.moving == 1):
                #handle repositioning the moving gene
                self.moving = 0
                self.x += event.x
                self.y += event.y
                self.fixed.move(widget,
                                int(self.x),int(self.y))
    def toggle_Select(self):
        self.selected = not self.selected
        if(self.selected):
            self.frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        else:
            self.frame.set_shadow_type(gtk.SHADOW_ETCHED_IN)


    def add_Menu_Item(self,menu,name,callback):
        menu_item = gtk.MenuItem(name)
        menu.append(menu_item)
        menu_item.connect("activate",callback)
        menu_item.show()
        
    def add_Interaction(self,widget):                        
        self.interactions.append("Y")
        self.set_Frame_Name()

    def set_Name(self,widget):
        text_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        text_window.set_size_request(80,50)
        text_window.set_title("Set Name")
        text_entry = gtk.Entry()
        text_entry.set_max_length(25)
        text_entry.connect("activate",self.set_Name_Callback,text_entry)
        text_entry.connect("activate", lambda w: text_window.destroy())
        text_entry.set_text(self.name)
        text_entry.select_region(0,len(text_entry.get_text()))
        text_entry.set_editable(True)

        text_window.add(text_entry)
        text_entry.show()
        text_window.show()
    def set_Name_Callback(self,widget,entry):
        self.name = entry.get_text()
        self.set_Frame_Name()        


#===============================================================================
#gene element container
#===============================================================================
#===============================================================================

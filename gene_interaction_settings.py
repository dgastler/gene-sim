import pygtk
pygtk.require('2.0')
import gtk

from regulator import *
#This class is used in gene_settings and creates a frame
#to configure the settngs for a gene interaction
class Gene_Interaction_Settings:
    def calling_callback(self, widget,funct,value):
        funct(value)
    def call_popup(self,menu,event):
        if event.type == gtk.gdk.BUTTON_PRESS:
            menu.popup(None, None, None, event.button, event.time)
    def __init__(self,gene_collection,this_gene,gene_interaction):
        #properties in gene_interaction 
        
        #graphical values
        self.frame = gtk.Frame("")
        self.frame.set_size_request(100,25)
        self.box = gtk.HBox()
        self.frame.add(self.box)        
                
        #add pulldown for interaction source 
        self.source_Menu_Button = gtk.Button("Source")
        self.source_Menu = gtk.Menu()
        self.Add_Sources_To_Menu(gene_collection,
                                 this_gene,
                                 gene_interaction)
        self.source_Menu_Button.connect_object("event",
                                               self.call_popup,
                                               self.source_Menu)        
        self.source_Menu.show()
        self.source_Menu_Button.show()
        self.box.pack_start(self.source_Menu_Button)
        #add pop up

        #add interaction type pulldown
        self.type_Menu_Button = gtk.Button("Type")
        self.type_Menu = gtk.Menu()
        self.Add_Types_To_Menu(gene_interaction)
        self.type_Menu_Button.connect_object("event",
                                             self.call_popup,
                                             self.type_Menu)        
        self.type_Menu.show()
        self.type_Menu_Button.show()
        self.box.pack_start(self.type_Menu_Button)
        #add pop up

        #add rate text input
        self.rate_Entry = gtk.Entry()
        self.rate_Entry.set_max_length(25)
        self.rate_Entry.connect("changed",
                                self.calling_callback,
                                gene_interaction.set_Rate_Constant,
                                self.rate_Entry.get_text())
        self.rate_Entry.set_text(str(gene_interaction.rate_Constant))
        self.rate_Entry.select_region(0,len(self.rate_Entry.get_text()))
        self.rate_Entry.set_editable(True)
        self.rate_Entry.set_size_request(20,20)
        self.box.pack_start(self.rate_Entry)

        #add K input
        self.K_Entry = gtk.Entry()
        self.K_Entry.set_max_length(25)
        self.K_Entry.connect("changed",
                             self.calling_callback,
                             gene_interaction.set_K,
                             self.K_Entry.get_text())
        self.K_Entry.set_text(gene_interaction.rate_Constant)
        self.K_Entry.select_region(0,len(gene_interaction.rate_Constant))
        self.K_Entry.set_editable(True)
        self.K_Entry.set_size_request(20,20)
        self.box.pack_start(self.K_Entry)

        #add N value
        self.N_Adjust = gtk.Adjustment(1, 1, 10, 1, 1, 0)
        self.N_Entry = gtk.SpinButton(self.N_Adjust)
        self.N_Entry.connect("changed",
                             self.calling_callback,
                             gene_interaction.set_N,
                             self.N_Entry.get_value())
        self.N_Entry.set_size_request(20,20)
        self.box.pack_start(self.N_Entry)

        self.box.show()
        self.frame.show()

    def Add_Sources_To_Menu(self,
                            gene_collection,
                            this_gene,
                            gene_interaction):
        #manually add this element because it isn't on the list yet
        #this way it is always first
        print "name:", this_gene.name, "\n"

        this_Name_Item = gtk.MenuItem(this_gene.name)
        this_Name_Item.connect("activate",
                               self.Select_Source,
                               gene_interaction,
                               this_gene.name)
        self.source_Menu.append(this_Name_Item)
        this_Name_Item.show()

        #add all the other elements
        for element in gene_collection.element_list:
            #rely on the manual add for the this_gene, so don't add it here
            if(element.name != this_gene.name):
                name_Item = gtk.MenuItem(element.name)
                name_Item.connect("activate",
                                  self.Select_Source,
                                  gene_interaction,
                                  element.name)
                self.source_Menu.append(name_Item)
                name_Item.show()

    def Select_Source(self,widget,gene_interaction,source):
        gene_interaction.set_Name(source)
        self.source_Menu_Button.set_label(source)
        

    def Add_Types_To_Menu(self,gene_interaction):
        for regtype in regtypes:
            type_Item = gtk.MenuItem(regtype)
            type_Item.connect("activate",
                             self.Select_Type,
                             gene_interaction,
                             regtype)
            self.type_Menu.append(type_Item)
            type_Item.show()

    def Select_Type(self,widget,gene_interaction,regtype):
        gene_interaction.set_Interaction_Type(regtype)
        self.type_Menu_Button.set_label(regtype)
        if(regtype == "reg_None"):
            self.show_Rate = False
            self.show_K = False
            self.show_N = False
        elif(regtype == "reg_Decay"):    
            #only source for decay is self
            self.source_Menu.set_active(0)
            self.show_Rate = True
            self.show_K = False
            self.show_N = False
        elif(regtype == "reg_Activator"):
            self.show_Rate = True
            self.show_K = True
            self.show_N = True
        elif(regtype == "reg_Repressor"):
            self.show_Rate = True
            self.show_K = True
            self.show_N = True
        else:
            self.show_Rate = False
            self.show_K = False
            self.show_N = False
        self.Update_Visible()

    def Update_Visible(self):
        if(self.show_Rate):
            self.rate_Entry.show()
        else:
            self.rate_Entry.hide()
        
        if(self.show_K):
            self.K_Entry.show()
        else:
            self.K_Entry.hide()
            
        if(self.show_N):
            self.N_Entry.show()
        else:
            self.N_Entry.hide()

    def destroy(self):
        self.source_Menu_Button.destroy()
        self.type_Menu_Button.destroy()
        self.rate_Entry.destroy()
        self.K_Entry.destroy()
        self.N_Adjust.destroy()
        self.box.destroy()
        self.frame.destroy()

        

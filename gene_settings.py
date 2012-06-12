import pygtk
pygtk.require('2.0')
import gtk

from gene_interaction_settings import *
from regulator import *

#This class pops open a window to show and configure the settings for a gene_element
class Gene_Settings:
    def calling_callback(self, widget,funct,value):
        funct(value)
    def __init__(self,gene_collection,this_gene):
        #create window for configuring this gene eleent
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_size_request(300,300)
        window.set_title("Configure Gene Element");
        window.connect("delete_event",self.Close_Window)

        print "gene_settings ", this_gene.name, "\n"

        #Main division
        window_Main_VBox = gtk.VBox()
        window.add(window_Main_VBox)
        
        #add name entry linked to the this_gene's name
        name_Entry = gtk.Entry()
        name_Entry.set_size_request(100,25)
        name_Entry.set_max_length(25)
        name_Entry.connect("changed",
                           self.calling_callback,
                           this_gene.set_Name,
                           name_Entry.get_text())
        name_Entry.set_text(this_gene.name)
        name_Entry.select_region(0,len(this_gene.name))
        name_Entry.set_editable(True)
        name_Entry.show()
        window_Main_VBox.pack_start(name_Entry)


        #make a button to make new entries
        new_button = gtk.Button("New interaction");
        new_button.set_size_request(100,25)
        new_button.connect("clicked",
                           self.Add_Interaction,
                           gene_collection,
                           this_gene);
        new_button.show()
        window_Main_VBox.pack_start(new_button)

        #add a list of gene_interactions in a frame
        interactions_frame = gtk.Frame("Interactions")
        self.interactions_box = gtk.VBox()
        interactions_frame.add(self.interactions_box)
        interactions_frame.show()
        window_Main_VBox.pack_start(interactions_frame)

        #add all existing interactions
        self.interaction_List = []
        for interaction in this_gene.regulation_Interactions:
            current_interaction = Gene_Interaction_Settings(gene_collection,this_gene,interaction)
            self.interaction_List.append(current_interaction)
            self.interactions_box.pack_start(current_interaction.frame)

        self.interactions_box.show()
        window_Main_VBox.show()
        window.show()
        
    def Close_Window(self, widget, event, data=None):
        print "should emit signal"

    def Add_Interaction(self, widget,
                        gene_collection,
                        this_gene):
        blank_interaction = regulation()
        this_gene.regulation_Interactions.append(blank_interaction)
        current_interaction = Gene_Interaction_Settings(gene_collection,
                                                        this_gene,
                                                        blank_interaction)
        self.interaction_List.append(current_interaction)
        self.interactions_box.pack_start(current_interaction.frame)
        self.interaction_List.append(blank_interaction)
        
        

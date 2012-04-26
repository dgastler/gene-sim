#!/sw/bin/python2.6

#GTK for GUI
import pygtk
pygtk.require('2.0')
import gtk

#matplotlib for plots
import matplotlib
matplotlib.use('GTK')
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas

from gene_element import *

#===============================================================================
#===============================================================================
#main GUI
#===============================================================================
class mainGUI:
    #====================
    #constructor
    #====================
    def __init__(self):
        # Create main window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Dan's crazy gene regulation simulator")
        self.window.set_border_width(2)
        self.window.connect("delete_event",self.close)
        
        #window size values
        self.x_size = 800
        self.y_size = 600
        self.design_Window_Fraction_x = 1.0
        self.design_Window_Fraction_y = 0.5
        self.button_Window_Fraction_x = 0.1
        self.button_Window_Fraction_y = 0.5
        self.plot_Window_Fraction_x = 0.9
        self.plot_Window_Fraction_y = 0.5

                
        #divide up the window
        self.main_Box = gtk.VBox(False,0)
        self.window.add(self.main_Box)

        #Setup circuit design area
        self.setup_Design_Area(self.main_Box)
        
        self.sub_Box = gtk.HBox(False,0)
        self.main_Box.pack_start(self.sub_Box,True,True,0)
        #Setup buttons
        self.setup_Buttons(self.sub_Box)
        self.setup_Plots(self.sub_Box)
       
        self.sub_Box.show_all()
        self.main_Box.show_all()
        self.window.show_all()

        self.objects = []


    #====================
    #Init helpers
    #====================
    def setup_Design_Area(self,box):
        self.design_Area = gtk.Fixed()
        self.design_Area.set_size_request(int(self.design_Window_Fraction_x*self.x_size),
                                          int(self.design_Window_Fraction_y*self.y_size))


        self.design_Area.set_has_window(True)
        box.pack_start(self.design_Area,True,True,0)
        self.design_Area.show()
        self.elementList = []
        self.design_Area.connect("button-press-event",self.create_Object,"")

    def setup_Buttons(self,box):
        self.button_Box = gtk.VBox(False,0)

        self.button_Clear = gtk.Button("Clear")
        self.button_Clear.connect("clicked",self.clear,"")
        self.button_Clear.show()
        self.button_Box.pack_start(self.button_Clear,True,True,0)


        self.button_Go = gtk.Button("Go")
        self.button_Go.connect("clicked",self.runSim,"")
        self.button_Box.pack_start(self.button_Go,True,True,0)
        self.button_Go.show()

        self.button_Quit = gtk.Button("Quit")
        self.button_Quit.connect("clicked",self.close,"")
        self.button_Box.pack_start(self.button_Quit,True,True,0)
        self.button_Quit.show()
        
        self.button_Box.show()
        box.add(self.button_Box)

    def setup_Plots(self,box):
        self.plot_Figure = Figure(figsize=(5,4), dpi=72)
        self.plot = self.plot_Figure.add_subplot(111) 
        self.plot.plot(0,0,'-')
        self.plot_Canvas = FigureCanvas(self.plot_Figure)
        self.plot_Canvas.set_size_request(int(self.plot_Window_Fraction_x*self.x_size),
                                          int(self.plot_Window_Fraction_y*self.y_size))
        self.plot_Canvas.show()
        box.add(self.plot_Canvas)    
        
    #====================
    #Call backs
    #====================
    def close(self, widget, event, data=None):
        gtk.main_quit()
        return False
    def clear(self, widget, event, data=None):
        print "clear"
    def runSim(self, widget, event, data=None):
        print "sim"
    def create_Object(self, widget, event, data=None):
        if(event.button == 1):
            if(event.type == gtk.gdk._2BUTTON_PRESS):           
                self.objects.append(Gene_Element(widget,event.x,event.y))        


        
#===============================================================================
#main GUI
#===============================================================================
#===============================================================================


def main():
    gtk.main()

if __name__ == "__main__":
    mUI= mainGUI()
    main()

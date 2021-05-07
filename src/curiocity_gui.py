#from tkinter import *
from logging import disable, root
from re import S
import tkinter as tk
from tkinter import Canvas, ttk, PhotoImage
#from tkinter import simpledialog
#import tkinter

from tkinter.constants import E, HORIZONTAL, LEFT, N, TOP, Y
from tkinter.filedialog import askopenfilename
from tkinter import messagebox

import tkinter.font as tkFont

from query_gui import QueryGUI
from populate_gui import PopulateGUI


root = tk.Tk()

#root.geometry("700x500")
default_font = tkFont.nametofont("TkDefaultFont")
default_font.configure(family="Segoe Script", size = 12)
root.option_add("*Font", default_font)


root.title("CURIOCITY FRAMEWORK v0.3")
img = PhotoImage(file='img/curiocity.png')
root.tk.call('wm', 'iconphoto', root._w, img)

s = ttk.Style()
s.configure('Cyan.TNotebook', background="#00C3AF")
s.configure('Blue.TNotebook', background="#2494CC")
s.configure('Dark.TNotebook', background="#1F3D51")

s.configure("TEntry",background="black", disabledbackground="lightgray")

root.tk_setPalette(background='#F5F5F5', foreground='black',
               activeBackground='white', activeForeground='#1F3D51')
        
class MainApplication(tk.Frame):
    def __init__(self, parent : tk.Tk):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        self.tabControl = TabControl(self.parent)
        self.tabControl.pack(expand= True, fill="both")
        
    def __del__(self):
        self.parent.quit()
    
class TabControl(ttk.Notebook):
    def __init__(self, parent):
        ttk.Notebook.__init__(self, parent, style='Dark.TNotebook')
        self.parent = parent

        self.canvas = Canvas(parent)
        # self.canvas.pack()   
        self.populateTab = PopulateGUI(self)
        self.add(self.populateTab, text="Populate")
        self.populateTab = QueryGUI(self)
        self.add(self.populateTab, text="Query") 
   
    def chooseFileButtonClick(self, widget):
        filename = askopenfilename()
        if (filename != None):
            widget.delete(0, tk.END)
            widget.insert(0, filename)

    def setStateFrame(self, frame, state_):
        try:
            for child in frame.winfo_children():
                child.configure(state=state_)
        except Exception as E:
            print(E)
            pass


MainApplication(parent=root)#.pack(expand= True, fill="both")
root.mainloop()



# # data_columns_default = {
# #     'ID' : 'Código único en la database',
# #     'Alternative ID' : 'Número/código asignado por el museo desde ingreso a ser expuesto',
# #     'Title' : 'Título principal del objeto u obra de arte',
# #     'Description' : 'Descripción o nota asociada al objeto',
# #     'Author' : 'Creador del objeto',
# #     'Utility' : 'Uso que se le dio al objeto',
# #     'Owner' : 'Dueño actual',
# #     'Condition State' : 'Estado actual del objeto',
# #     'Material' : 'Material del objeto (TECNICA USADA)',
# #     'Period ID' : 'Código del Período o evento',
# #     'Period' : 'Periodo, evento',
# #     'Creation date' : 'Fecha de creación del objeto/obra de arte',
# #     'Acquisition' : 'Forma como fue adquirido el objeto',
# #     'Donor' : 'Identifica y da crédito a la persona, fundación o método por el cual el objeto fue adquirido  (del/a cual fue adquirido el objeto)',
# #     'Donor description' : 'Descripción de donación',
# #     'Location in Museum' : 'Localización del objeto dentro del museo',
# #     'Museum Department' : 'Departamento dentro del museo responsable por el objeto',
# #     'Artifact height' : 'Dimensión: Alto',
# #     'Artifact width' : 'Dimensión: Ancho',
# #     'Artifact length' : 'Dimensión: Largo',
# #     'Artifact diameter' : 'Dimensión: Diámetro',
# #     'Artifact depth' : 'Profundidad',
# #     'Artifact weight' : 'Peso'   
# # }

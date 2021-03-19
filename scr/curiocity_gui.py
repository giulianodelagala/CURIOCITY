#from tkinter import *
from logging import disable
import tkinter as tk
from tkinter import StringVar, ttk
from tkinter import simpledialog
import tkinter

from tkinter.constants import E, HORIZONTAL, LEFT, TOP
from tkinter.filedialog import askopenfilename
from tkinter import messagebox

import tkinter.font as tkFont

from query_process import QueryProcess

import json

from period_process import PeriodProcess
from data_process import DataProcess

root = tk.Tk()
#root.title("CURIOCITY Framework v0.2")
#root.geometry("700x500")
default_font = tkFont.nametofont("TkDefaultFont")
default_font.configure(size = 12)
root.option_add("*Font", default_font)

root.withdraw()


class MainApplication(tk.Frame):
    def __init__(self, parent : tk.Tk):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.tabControl = TabControl(self.parent)
        self.tabControl.pack(expand= True, fill="both")
        self.parent.title("CURIOCITY FRAMEWORK v0.2")

        
            
        # self.default_font = font.nametofont("TkDefaultFont")
        # self.default_font.configure(family="Segoe Script",
        #     weight=font.BOLD, size=50)
        # self.parent.option_add("Font", self.default_font)
        
    def __del__(self):
        self.parent.quit()
    
class TabControl(ttk.Notebook):
    def __init__(self, parent):
        ttk.Notebook.__init__(self, parent)
        self.parent = parent
        
        self.populateTab = PopulateTab(self)
        self.add(self.populateTab, text="Populate")
        self.periodTab = PeriodTab(self)
        self.add(self.periodTab, text="Periods")
        self.configureTab = ConfigureTab(self)
        self.add(self.configureTab, text="Configure")
        self.queryTab = QueryTab(self)
        self.add(self.queryTab, text="Query")

        self.sparqlTab = SparqlTab(self)
        self.add(self.sparqlTab, text="Sparql")  
   
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

class PopulateTab(tk.Frame):   
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        
        # Widgets
        self.wrapperPopulate = tk.LabelFrame(self, text = "Populate Ontology", bd=3)
        self.wrapperPopulate.pack(fill="both", expand="yes", padx=20, pady=10)
        self.wrapperPopulate.columnconfigure(1, weight=1) #entry
        self.wrapperPopulate.columnconfigure(2, weight=1) #buttons
        self.wrapperPopulate.rowconfigure(4, weight=1)
        

        self.csvLabel = tk.Label(self.wrapperPopulate, text="Database CSV filename:", anchor="w")
        self.periodLabel = tk.Label(self.wrapperPopulate, text="Time Period Ontology filename:", anchor="w")
        self.ontoLabel = tk.Label(self.wrapperPopulate, text="Output Ontology filename:", anchor="w")
        self.logLabel = tk.Label(self.wrapperPopulate, text="Log filename:")

        self.csvEntry = tk.Entry(self.wrapperPopulate, width= 50) #bg, border
        self.csvEntry.insert(0, "museum_data.csv")
        self.periodEntry = tk.Entry(self.wrapperPopulate, width= 50)
        self.periodEntry.insert(0, "period_onto.ttl")
        self.ontoEntry = tk.Entry(self.wrapperPopulate, width=50)
        self.ontoEntry.insert(0, "museum_onto.ttl")
        self.logEntry = tk.Entry(self.wrapperPopulate, width=50)
        self.logEntry.insert(0, "museum_log.txt")

        self.csvLoadButton = tk.Button(self.wrapperPopulate, text="Choose...", command= lambda: parent.chooseFileButtonClick(self.csvEntry), padx=30)
        self.periodLoadButton = tk.Button(self.wrapperPopulate, text="Choose...", command= lambda: parent.chooseFileButtonClick(self.periodEntry), padx=30)

        self.csvLabel.grid(sticky="e", row= 0, column=0, pady=10)
        self.csvEntry.grid(row=0, column=1, padx=10)
        self.csvLoadButton.grid( sticky="w", row=0, column=2)

        self.periodLabel.grid(sticky="e", row= 1, column=0, pady=10)
        self.periodEntry.grid(row=1, column=1, padx=10)
        self.periodLoadButton.grid(sticky="w", row=1, column=2)

        self.ontoLabel.grid(sticky="e",row=2, column=0, pady=10)
        self.ontoEntry.grid(row=2, column=1, padx=10)
        self.logLabel.grid(sticky="e", row=3, column=0, pady=10)
        self.logEntry.grid(row=3, column=1, padx=10)

        self.logText = tk.Text(self.wrapperPopulate, width=100, height=20, state="normal")
        self.logText.grid(row=4, column=0, columnspan=3)

        populateButton = tk.Button(self, text="Populate!", command= self.populateButtonClick, padx=30)
        populateButton.pack(pady=5)

    def populateButtonClick(self):
        process = DataProcess(logf=self.logEntry.get(),
            csvf=self.csvEntry.get(), ontof=self.ontoEntry.get(),
            periodf=self.periodEntry.get(), sender = self)
        process.Execute()
        return True
    
    def Choose(self, who):
        result = messagebox.askquestion("Choose", "Is " + who + " a Person[Yes] or Group[No] ?", icon="question")
        if (result == 'yes'):
            return 'p'
        else:
            return 'g'
    
    def Logger(self, message):
        self.logText.insert(tk.INSERT, message + "\n")
        self.logText.see("end")

class PeriodTab(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.wrapperPeriod = tk.LabelFrame(self, text = "Time periods", bd=3)
        self.wrapperPeriod.pack(fill="both", expand="yes", padx=20, pady=10)
        self.wrapperPeriod.columnconfigure(1, weight=1) #entry
        self.wrapperPeriod.columnconfigure(2, weight=1) #buttons

        self.wrapperPeriodConfigure = tk.LabelFrame(self, text="Time periods CSV file Columns", bd=3)
        self.wrapperPeriodConfigure.pack(fill="both", expand="yes", padx=20, pady=10)

        self.periodLabel = tk.Label(self.wrapperPeriod, text="Period CSV filename:", anchor="w")
        self.periodOntoLabel = tk.Label(self.wrapperPeriod, text="Period Ontology filename", anchor="w")

        self.periodEntry = tk.Entry(self.wrapperPeriod, width= 50) #bg, border
        self.periodEntry.insert(0, "period_data.csv")
        self.periodOntoEntry = tk.Entry(self.wrapperPeriod, width= 50) #bg, border
        self.periodOntoEntry.insert(0, "period_onto.ttl")

        self.periodLabel.grid(sticky="e", row= 0, column=0, pady=10)
        self.periodEntry.grid(row=0, column=1, padx=10)
        self.periodOntoLabel.grid(sticky="e", row= 1, column=0, pady=10)
        self.periodOntoEntry.grid(row=1, column=1, padx=10)

        self.periodLoadButton = tk.Button(self.wrapperPeriod, text="Choose...", command= lambda: parent.chooseFileButtonClick(self.periodEntry), padx=30)
        self.periodLoadButton.grid(sticky="w", row=0, column=2)

        self.trvPeriod = ttk.Treeview(self.wrapperPeriodConfigure, columns=(1,2), show="headings",
        height="4", selectmode="browse")
        self.trvPeriod.heading(1, text="Concept")
        self.trvPeriod.heading(2, text="Column name in CSV file")
        self.trvPeriod.column(1, width=150)
        self.trvPeriod.column(2, width=500)

        self.trvPeriod.tag_configure('oddrow', background='#E8E8E8')
        self.trvPeriod.tag_configure('evenrow', background='lightgray')

        with open("name_period_columns.json", 'r') as data_columns_file :
            name_period_columns = json.load(data_columns_file)

        count = 0
        for i in name_period_columns:
            if (count % 2 == 0):
                self.trvPeriod.insert("", 'end', values = (i, name_period_columns[i]), tags=('evenrow') )
            else: 
                self.trvPeriod.insert("", 'end', values = (i, name_period_columns[i]), tags=('oddrow') )
            count+=1

        self.trvPeriod.pack()

        periodOntoButton = tk.Button(self, text="Create Time period ontology", command= self.periodOntoButtonClick, padx=30)
        periodOntoButton.pack(pady=5)

    def periodOntoButtonClick(self):
        process = PeriodProcess(csvf=self.periodEntry.get(), ontof=self.periodOntoEntry.get())
        process.Execute()
        return True

class ConfigureTab(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)     

        self.wrapperConfig = tk.LabelFrame(self, text = "Database CSV file Configuration", bd=3)
        self.wrapperConfig.pack(fill="both", expand="yes", padx=20, pady=10)

        # Style
        tree_style = ttk.Style()
        tree_style.theme_use("default")
        tree_style.configure("Treeview",
            # background = "#D3D3D3",
            foreground = "black",
            rowheigth = 25,
            fieldbackground = "#D3D3D3"
        )
        tree_style.map('Treeview',
            background = [('selected', 'gray')]
        )

        #Tree Scrollbar
        self.tree_frame = tk.Frame(self.wrapperConfig)
        self.tree_scroll = tk.Scrollbar(self.tree_frame)

        self.execButton = tk.Button(self, text="Ok", command= self.execButtonClick, padx=30) #,padx= 50, pady= 50, state = 

        self.trv = ttk.Treeview(self.tree_frame, columns=(1,2), show="headings",
            height="23", yscrollcommand=self.tree_scroll.set, selectmode="browse")
        self.trv.heading(1, text="Concept")
        self.trv.heading(2, text="Column name in CSV file")
        self.trv.column(1, width=150)
        self.trv.column(2, width=500)

        self.trv.tag_configure('oddrow', background='#E8E8E8')
        self.trv.tag_configure('evenrow', background='lightgray')

        with open("name_columns.json", 'r') as data_columns_file :
            name_columns = json.load(data_columns_file)   

        count = 0
        for i in name_columns:
            if (count % 2 == 0):
                self.trv.insert("", 'end', values = (i, name_columns[i]), tags=('evenrow') )
            else: 
                self.trv.insert("", 'end', values = (i, name_columns[i]), tags=('oddrow') )
            count+=1

        #Configure Tree Scrollbar
        self.tree_scroll.config(command=self.trv.yview)
        #Select row
        self.trv.bind('<Double 1>', self.getrow)

        self.execButton.pack(pady=10)
        self.tree_frame.pack()
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.trv.pack()

    def execButtonClick (self):
        #self.execButton['text'] = entry_form.get()
        return True

    def getrow(self, event):
        rowid = self.trv.identify_row(event.y)
        item = self.trv.item(self.trv.focus())
        focused = self.trv.focus()
        user_input = simpledialog.askstring(title="Configure CSV Columns",
            prompt="Name of the column for " + item['values'][0] + "?",
            initialvalue = item['values'][1])
        if (user_input != None):
            self.trv.item(focused, values=(item['values'][0], user_input))

class QueryTab(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.queryManager = QueryProcess()
     
        self.wrapperConnect = tk.LabelFrame(self, text = "Connection", bd=3) 
        self.wrapperConnect.pack(fill="both", expand="yes", padx=20)
        self.wrapperConnect.grid_columnconfigure(1, weight=1) #expand entry

        self.wrapperList = tk.LabelFrame(self, text = "Item List", bd=3)
        self.wrapperList.pack(fill="both", expand="yes", padx=20)
        

        self.wrapperQuery = tk.LabelFrame(self, text = "Query", bd=3)
        self.wrapperQuery.pack(fill="both", expand="yes", padx=20, pady=10)
        self.wrapperQuery.grid_columnconfigure(1, weight=1) #expand entry
        

        self.wrapperItem = tk.LabelFrame(self, text = "Item Data", bd=3)
        self.wrapperItem.pack(fill="both", expand="yes", padx=20, pady=10)
        self.wrapperItem.grid_columnconfigure(1, weight=1) #expand entry

        #### CONNECT
        self.connectLabel = tk.Label(self.wrapperConnect, text="Endpoint", anchor="w")
        self.connectLabel.grid(row=0, column=0, padx=10)
        self.connectEntry = tk.Entry(self.wrapperConnect, width= 50)
        self.connectEntry.grid(sticky="we", row=0, column= 1, padx=5)
        self.loadButton = tk.Button(self.wrapperConnect, text="Test...", command= self.testButtonClick, padx=30)
        self.loadButton.grid(row=0, column=2, padx=10)

        self.connection_path = 'http://localhost:3030/dataset/query'
        self.connectEntry.insert(0, self.connection_path)

        #### LIST
        self.trv_frame = tk.Frame(self.wrapperList)
        self.trv_scroll_v = tk.Scrollbar(self.trv_frame)
        self.trv_scroll_h = tk.Scrollbar(self.trv_frame, orient=HORIZONTAL)

        #Headings for treeview
        headings = {0 : "ID",
                    1 : "Title",
                    2 : "Author",
                    3 : "Material",
                    4 : "Location",
                    5 : "Period" ,
                    6 : "Period Begin",
                    7 : "Period End",
                    8 : "Description",
                    9 : "Donor",
                    10 : "About Donor"}

        self.trv = ttk.Treeview(self.trv_frame, columns=list(range(0,len(headings))), show="headings",
            yscrollcommand=self.trv_scroll_v.set, xscrollcommand=self.trv_scroll_h.set,
            height="4", selectmode="browse")

        for i in headings:
            self.trv.heading(i, text=headings[i])
            self.trv.column(i, width=65, stretch=False)

        self.trv.tag_configure('oddrow', background='#E8E8E8')
        self.trv.tag_configure('evenrow', background='lightgray')
        
        self.trv_scroll_v.config(command=self.trv.yview)
        self.trv_scroll_h.config(command=self.trv.xview)

        self.trv_frame.pack(fill="both", expand="yes")
        self.trv_scroll_v.pack(side=tk.RIGHT, fill=tk.Y)
        self.trv_scroll_h.pack(side=tk.BOTTOM, fill=tk.X)
        self.trv.pack(fill="both", expand="yes")

        self.trv.bind('<Double 1>', self.getrow) #Double click

        #### END LIST

        #### QUERY

        self.query1Label = tk.Label(self.wrapperQuery, text="Query 1", anchor="w")
        self.query2Label = tk.Label(self.wrapperQuery, text="Query 2", anchor="w")
        self.query3Label = tk.Label(self.wrapperQuery, text="Query 3", anchor="w")
        self.query4Label = tk.Label(self.wrapperQuery, text="Query 4", anchor="w")
        self.query5Label = tk.Label(self.wrapperQuery, text="Query 5", anchor="w")

        self.query1Entry = tk.Entry(self.wrapperQuery, width= 50)
        self.query2Entry = tk.Entry(self.wrapperQuery, width= 50)
        self.query3Entry = tk.Entry(self.wrapperQuery, width= 50)
        self.query4Entry = tk.Entry(self.wrapperQuery, width= 50)
        self.query5Entry = tk.Entry(self.wrapperQuery, width= 50)

        valuesCombo = ['Title', 'Author', 'Material', 'Location', 'Period']
        self.query1Combo = ttk.Combobox(self.wrapperQuery, width= 10, values=valuesCombo, state="readonly")
        self.query2Combo = ttk.Combobox(self.wrapperQuery, width= 10, values=valuesCombo, state="readonly")
        self.query3Combo = ttk.Combobox(self.wrapperQuery, width= 10, values=valuesCombo, state="readonly")
        self.query4Combo = ttk.Combobox(self.wrapperQuery, width= 10, values=valuesCombo, state="readonly")
        self.query5Combo = ttk.Combobox(self.wrapperQuery, width= 10, values=valuesCombo, state="readonly")
        
        self.query1Label.grid(sticky="w", row= 0, column=0, pady=5)
        self.query1Entry.grid(sticky="we",row=0, column= 1)
        self.query1Combo.grid(row=0, column= 2, padx=5)

        self.query2Label.grid(sticky="w", row= 1, column=0, pady=5)
        self.query2Entry.grid(sticky="we",row=1, column= 1)
        self.query2Combo.grid(row=1, column= 2, padx=5)

        self.query3Label.grid(sticky="w", row= 2, column=0, pady=5)
        self.query3Entry.grid(sticky="we", row=2, column= 1)
        self.query3Combo.grid(row=2, column= 2, padx=5)

        self.query4Label.grid(sticky="w", row= 3, column=0, pady=5)
        self.query4Entry.grid(sticky="we", row=3, column= 1)
        self.query4Combo.grid(row=3, column= 2, padx=5)

        self.query5Label.grid(sticky="w", row= 4, column=0, pady=5)
        self.query5Entry.grid(sticky="we", row=4, column= 1)
        self.query5Combo.grid(row=4, column= 2, padx=5)

        
        self.queryButton = tk.Button(self.wrapperQuery, text="Search...", command= self.queryButtonClick, padx=30)
        self.queryButton.grid(row=5, column=0, padx=5, columnspan=2)

        #### END QUERY

        #### ITEM DATA
        self.idLabel = tk.Label(self.wrapperItem, text="ID", anchor="w")
        self.titleLabel = tk.Label(self.wrapperItem, text="Title", anchor="w")
        self.authorLabel = tk.Label(self.wrapperItem, text="Author", anchor="w")
        self.materialLabel = tk.Label(self.wrapperItem, text="Material", anchor="w")
        self.locationLabel = tk.Label(self.wrapperItem, text="Location", anchor="w")
        self.descriptionLabel = tk.Label(self.wrapperItem, text="Description", anchor="w")

        self.idEntry = tk.Entry(self.wrapperItem, width= 50)
        self.titleEntry = tk.Entry(self.wrapperItem, width= 50)
        self.authorEntry = tk.Entry(self.wrapperItem, width= 50)
        self.materialEntry = tk.Entry(self.wrapperItem, width= 50)
        self.locationEntry = tk.Entry(self.wrapperItem, width= 50)
        self.descriptionEntry = tk.Entry(self.wrapperItem, width= 50)

        self.idLabel.grid(sticky="w", row= 0, column=0, pady=5)
        self.idEntry.grid(sticky="we", row=0, column= 1, padx=5)
        self.titleLabel.grid(sticky="w", row= 1, column=0, pady=5)
        self.titleEntry.grid(sticky="we",row=1, column= 1, padx=5)
        self.authorLabel.grid(sticky="w", row= 2, column=0, pady=5)
        self.authorEntry.grid(sticky="we",row=2, column= 1, padx=5)

        self.materialLabel.grid(sticky="w", row= 3, column=0, pady=5)
        self.materialEntry.grid(sticky="we",row=3, column= 1, padx=5)
        self.locationLabel.grid(sticky="w", row= 4, column=0, pady=5)
        self.locationEntry.grid(sticky="we",row=4, column= 1, padx=5)
        self.descriptionLabel.grid(sticky="w", row= 5, column=0, pady=5)
        self.descriptionEntry.grid(sticky="we",row=5, column= 1, padx=5)

        self.updateButton = tk.Button(self.wrapperItem, text="Update...", command= self.updateButtonClick, padx=30)
        self.updateButton.grid(row=6, column=0, padx=5, pady=10, columnspan=2)

        #Disable frame before test connection
        #self.parent.setStateFrame(self.wrapperQuery, 'disable')
        #self.parent.setStateFrame(self.wrapperItem, 'disable')
        
        #### END ITEM DATA

    def queryButtonClick(self):
        #Prepare a List of pairs <data, concept>
        qList = []
        queryList = []

        qList.append(self.query1Entry.get())
        qList.append(self.query1Combo.get())
        qList.append(self.query2Entry.get())
        qList.append(self.query2Combo.get())
        qList.append(self.query3Entry.get())
        qList.append(self.query3Combo.get())
        qList.append(self.query4Entry.get())
        qList.append(self.query4Combo.get())
        qList.append(self.query5Entry.get())
        qList.append(self.query5Combo.get())

        for i in range(0, len(qList),2):
            if (qList[i] != '' and qList[i+1] != ''):
                queryList.append([qList[i], qList[i+1]])
                #print('OK ' + c1 + "...")
        
        response = self.queryManager.combinedQuery(queryList)
        self.trv.delete(*self.trv.get_children())
        for i in response:
            self.trv.insert('','end',values=i)

    def insertVal(self, obj, value):
        obj.delete(0, tk.END)
        obj.insert(0, value)

    def getrow(self, event):
        #rowid = self.trv.identify_row(event.y)
        item = self.trv.item(self.trv.focus())
        self.insertVal( self.idEntry, item['values'][0])
        self.insertVal( self.titleEntry, item['values'][1])
        self.insertVal( self.authorEntry, item['values'][2])
        self.insertVal( self.materialEntry, item['values'][3])
        self.insertVal( self.locationEntry, item['values'][4])
        self.insertVal( self.descriptionEntry, item['values'][8])

    def testButtonClick(self):
        endpoint = self.connectEntry.get()
        if (self.queryManager.testConnection(endpoint)):
            self.connection_path = endpoint
            #Enable frame after test connection
            #self.parent.setStateFrame(self.wrapperQuery, 'normal')
            #self.parent.setStateFrame(self.wrapperItem, 'normal')
            messagebox.showinfo("Test", "Server connection is Ok!")
        else:
            messagebox.showerror("Test", "Error connecting to server...")
    
    def updateButtonClick(self):
        return True

class SparqlTab(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.queryManager = QueryProcess()

        self.wrapperQuery = tk.LabelFrame(self, text = "Query", bd=3)
        self.wrapperQuery.pack(fill="both", expand="yes", padx=20, pady=10)

        self.wrapperResp = tk.LabelFrame(self, text = "Query response", bd=3)
        self.wrapperResp.pack(fill="both", expand="yes", padx=20, pady=10)

        ### Query
        self.queryText = tk.Text(self.wrapperQuery, width=100, height=20, state="normal")
        self.queryText.pack(fill="both", expand="yes", padx=20, pady=10)

        self.queryButton = tk.Button(self.wrapperQuery, text="Query...", command= self.queryButtonClick, padx=30)
        self.queryButton.pack()
        
        example = """#Sample Query
PREFIX ecrm: <http://erlangen-crm.org/170309/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX time: <http://www.w3.org/2006/time#>
PREFIX cit: <http://curiocity.org/>\n
SELECT ?s ?o ?p
WHERE { ?s ?o ?p }
LIMIT 10"""
        self.queryText.insert(tk.INSERT, example)
      
        ### Response
    
        self.respText = tk.Text(self.wrapperResp, width=100, height=20, state="normal")
        self.respText.pack(fill="both", padx=5, pady=5)

    def queryButtonClick(self):
        query = self.queryText.get("0.0" , tk.END)
        response = self.queryManager.customQuery(query)
        response = json.dumps(response, indent=2)
        self.respText.insert(tk.INSERT, response)

if __name__ == "__main__":
    root = tk.Tk()
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

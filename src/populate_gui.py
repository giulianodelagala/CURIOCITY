#Populate Tab
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog


import json
from tkinter.constants import BOTTOM, LEFT
from tkinter.filedialog import askopenfile, askopenfilename

from data_process import DataProcess
from period_process import PeriodProcess
from data_process import ReasonerProcess

class PopulateGUI(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.tabControl = PopControl(self)
        self.tabControl.pack(expand= True, fill="both")


class PopControl(ttk.Notebook):
    def __init__(self, parent):
        ttk.Notebook.__init__(self, parent, style='Cyan.TNotebook')
        self.parent = parent

        ########### Read Config File
        with open("config.json", 'r') as data_columns_file :
            self.config = json.load(data_columns_file) #config dictionary

        ##########
        self.populateTab = PopulateTab(self)
        self.add(self.populateTab, text="Ontology")
        self.periodTab = ExtrasTab(self)
        self.add(self.periodTab, text="Extras")
        self.configureTab = ConfigureTab(self)
        self.add(self.configureTab, text="Configure")

class PopulateTab(tk.Frame):   
    def __init__(self, parent: PopControl):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.tabControl = self.parent.parent.parent #link to TabControl Class

        # Widgets
        self.wrapperPopulate = tk.LabelFrame(self, text = "Populate Ontology", bd=3)
        self.wrapperPopulate.pack(fill="both", expand="yes", padx=20, pady=10)
        self.wrapperPopulate.columnconfigure(1, weight=1) #entry
        self.wrapperPopulate.columnconfigure(2, weight=1) #buttons
        self.wrapperPopulate.rowconfigure(0, weight=1)
        self.wrapperPopulate.rowconfigure(1, weight=1)
        self.wrapperPopulate.rowconfigure(2, weight=1)
        self.wrapperPopulate.rowconfigure(3, weight=1)
        
        self.wrapperLog = tk.LabelFrame(self, text = "Populate Log", bd=3)
        self.wrapperLog.pack(fill="both", expand="yes", padx=20, pady=10)

        self.csvLabel = tk.Label(self.wrapperPopulate, text="Database CSV filename:", anchor="w")
        self.periodLabel = tk.Label(self.wrapperPopulate, text="Time Period Ontology filename:", anchor="w")
        self.ontoLabel = tk.Label(self.wrapperPopulate, text="Output Ontology filename:", anchor="w")
        self.logLabel = tk.Label(self.wrapperPopulate, text="Log filename:")

        self.csvEntry = tk.Entry(self.wrapperPopulate, width= 50, bg='white') #border
        self.csvEntry.insert(0, "museum_data.csv")
        self.periodEntry = tk.Entry(self.wrapperPopulate, width= 50, bg='white')
        self.periodEntry.insert(0, "period_onto.ttl")
        self.ontoEntry = tk.Entry(self.wrapperPopulate, width=50, bg='white')
        self.ontoEntry.insert(0, "museum_onto.ttl")
        self.logEntry = tk.Entry(self.wrapperPopulate, width=50, bg='white')
        self.logEntry.insert(0, "museum_log.txt")

        self.checkMergeValue = tk.BooleanVar(self.wrapperPopulate)
        self.checkMergeValue.set(True)
        self.checkMerge = ttk.Checkbutton(self.wrapperPopulate,
            text="Merge Output", variable=self.checkMergeValue)
        
        
        self.csvLoadButton = tk.Button(self.wrapperPopulate, text="Choose...",
            command= lambda: self.tabControl.chooseFileButtonClick(self.csvEntry), padx=30)
        self.periodLoadButton = tk.Button(self.wrapperPopulate, text="Choose...",
            command= lambda: self.tabControl.chooseFileButtonClick(self.periodEntry), padx=30)

        self.csvLabel.grid(sticky="e", row= 0, column=0, pady=10)
        self.csvEntry.grid(row=0, column=1, padx=10)
        self.csvLoadButton.grid( sticky="w", row=0, column=2)

        self.periodLabel.grid(sticky="e", row= 1, column=0, pady=10)
        self.periodEntry.grid(row=1, column=1, padx=10)
        self.periodLoadButton.grid(sticky="w", row=1, column=2)

        self.ontoLabel.grid(sticky="e",row=2, column=0, pady=10)
        self.ontoEntry.grid(row=2, column=1, padx=10)
        self.checkMerge.grid(sticky="w", row=2, column=2, padx=10)

        self.logLabel.grid(sticky="e", row=3, column=0, pady=10)
        self.logEntry.grid(row=3, column=1, padx=10)
        
        self.logText = tk.Text(self.wrapperLog, width=100, height=20, state="normal")
        self.logText.pack(fill="both", expand="yes", padx=10, pady=10)

        populateButton = tk.Button(self, text="Populate!", command= self.populateButtonClick, padx=30)
        populateButton.pack(pady=5)

    def populateButtonClick(self):
        invalid = self.GetInvalidData()
        ##### Call to Data Processing Layer
        process = DataProcess(logf=self.logEntry.get(),
            csvf=self.csvEntry.get(), ontof=self.ontoEntry.get(),
            periodf=self.periodEntry.get(), invalid=invalid, sender = self)
        if (process.Execute(format='xml')): #TODO
            messagebox.showinfo(message="Data Process correct!, RDF file saved")
            ##### Merging rdf triples
            if (self.checkMergeValue.get() == True):
                #### Merge
                process.MergeOntos(format='xml') #TODO
            else:
                return True
        else:
            messagebox.showerror(message="Data Process Error")
            return False
        


    def GetInvalidData(self):
        # invalid_text = self.invalidText.get("1.0",tk.END)
        return self.parent.config['Invalid'].split(", ")
    
    def Choose(self, who):
        result = messagebox.askquestion("Choose", "Is " + who + " a Person[Yes] or Group[No] ?", icon="question")
        if (result == 'yes'):
            return 'p'
        else:
            return 'g'
    
    def Logger(self, message):
        self.logText.insert(tk.INSERT, message + "\n")
        self.logText.see("end")

class ExtrasTab(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.tabControl = self.parent.parent.parent #link to TabControl Class

        self.wrapperPeriod = tk.LabelFrame(self, text = "Time periods", bd=3)
        self.wrapperPeriod.pack(fill="both", expand="yes", padx=20, pady=10)
        self.wrapperPeriod.columnconfigure(1, weight=1) #entry
        self.wrapperPeriod.columnconfigure(2, weight=1) #buttons
        self.wrapperPeriod.rowconfigure(0, weight=1)
        self.wrapperPeriod.rowconfigure(1, weight=1)
        self.wrapperPeriod.rowconfigure(2, weight=1)

        self.wrapperReasoner = tk.LabelFrame(self, text="Reasoner", bd=3)
        self.wrapperReasoner.pack(fill="both", expand="yes", padx=20, pady=10)
        self.wrapperReasoner.columnconfigure(1, weight=1) #entry
        self.wrapperReasoner.columnconfigure(2, weight=1) #buttons
        self.wrapperReasoner.rowconfigure(0, weight=1)
        self.wrapperReasoner.rowconfigure(1, weight=1)
        self.wrapperReasoner.rowconfigure(2, weight=1)

        self.wrapperLog = tk.LabelFrame(self, text = "Populate Log", bd=3)
        self.wrapperLog.pack(fill="both", expand="yes", padx=20, pady=10)

        ###### Period Ontology Options
        self.periodLabel = tk.Label(self.wrapperPeriod, text="Period CSV filename:", anchor="w")
        self.periodOntoLabel = tk.Label(self.wrapperPeriod, text="Period Ontology filename:", anchor="w")

        self.periodEntry = tk.Entry(self.wrapperPeriod, width= 50, bg='white') #bg, border
        self.periodEntry.insert(0, "period_data.csv")
        self.periodOntoEntry = tk.Entry(self.wrapperPeriod, width= 50, bg='white') #bg, border
        self.periodOntoEntry.insert(0, "period_onto.ttl")

        self.periodLabel.grid(sticky="e", row= 0, column=0, pady=10)
        self.periodEntry.grid(row=0, column=1, padx=10)
        self.periodOntoLabel.grid(sticky="e", row= 1, column=0, pady=10)
        self.periodOntoEntry.grid(row=1, column=1, padx=10)

        self.periodLoadButton = tk.Button(self.wrapperPeriod, text="Choose...",
            command= lambda: self.tabControl.chooseFileButtonClick(self.periodEntry), padx=30)
        self.periodLoadButton.grid(sticky="w", row=0, column=2)

        periodOntoButton = tk.Button(self.wrapperPeriod, text="Create Time period ontology", command= self.periodOntoButtonClick, padx=30)
        periodOntoButton.grid(row=2, column=1, pady=5)

        ###### Reasoner Options
        self.reasonLabel = tk.Label(self.wrapperReasoner, text="Merged Ontology filename:", anchor="w")
        self.reasonOutputLabel = tk.Label(self.wrapperReasoner, text="Output Reasoner filename:", anchor="w")
        self.reasonEntry = tk.Entry(self.wrapperReasoner, width= 50, bg='white')
        self.reasonEntry.insert(0, "reasoner_input.ttl")

        self.reasonOutputEntry = tk.Entry(self.wrapperReasoner, width= 50, bg='white')
        self.reasonOutputEntry.insert(0, "reasoner_output.ttl")
        self.reasonLoadButton = tk.Button(self.wrapperReasoner, text="Choose...",
            command= lambda: self.tabControl.chooseFileButtonClick(self.reasonEntry), padx=30)
        self.reasonExecuteButton = tk.Button(self.wrapperReasoner, text="Execute Reasoner",
            command= lambda: self.reasonerExecute(input=self.reasonEntry.get(),
            output=self.reasonOutputEntry.get()), padx=30)
        
        self.reasonLabel.grid(sticky="e", row= 0, column=0, pady=10)
        self.reasonEntry.grid(row=0, column=1, padx=10)
        self.reasonLoadButton.grid(sticky="w", row=0, column=2)
        self.reasonOutputLabel.grid(sticky="e", row= 1, column=0, pady=10)
        self.reasonOutputEntry.grid(row=1, column=1, padx=10)
        self.reasonExecuteButton.grid(row=2, column=1, pady=5)

        ###### Log
        self.logText = tk.Text(self.wrapperLog, width=100, height=20, state="normal")
        self.logText.pack(fill="both", expand="yes", padx=10, pady=10)

    def reasonerExecute(sel, input:str, output:str):
        reasoner = ReasonerProcess(file_input=input, file_output=output)
        if (reasoner.ExecuteReasoner()):
            return True
        else:
            print('ERROR')
            return False

    def periodOntoButtonClick(self):
        process = PeriodProcess(csvf=self.periodEntry.get(), ontof=self.periodOntoEntry.get())
        process.Execute()
        return True

class ConfigureTab(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        self.wrapperField = tk.LabelFrame(self, text = "Data Configuration", bd=3)
        self.wrapperField.pack(fill="both", expand="yes", padx=20, pady=10)
        self.wrapperField.columnconfigure(1, weight=1) #entry

        self.wrapperConfig = tk.LabelFrame(self, text = "Database CSV file Configuration", bd=3)
        self.wrapperConfig.pack(fill="both", expand="yes", padx=20, pady=10)

        self.wrapperPeriodConfigure = tk.LabelFrame(self, text="Time periods CSV file Columns", bd=3)
        self.wrapperPeriodConfigure.pack(fill="both", expand="yes", padx=20, pady=10)

        ### Buttons
        self.wrapperButtons = tk.LabelFrame(self, bd=0)
        self.wrapperButtons.rowconfigure(0, weight=1)
        self.wrapperButtons.columnconfigure(0, weight=1)
        self.wrapperButtons.columnconfigure(1, weight=1)
        self.wrapperButtons.columnconfigure(2, weight=1)
        self.wrapperButtons.pack(fill="both", expand="yes", padx=20, pady=10)

        self.execButton = tk.Button(self.wrapperButtons, text="Apply", command= self.applyButtonClick, padx=30) #,padx= 50, pady= 50, state = 
        self.saveButton = tk.Button(self.wrapperButtons, text="Save Config", command= self.saveButtonClick, padx=30)
        self.loadButton = tk.Button(self.wrapperButtons, text="Default Config", command= self.loadButtonClick, padx=30)
        self.execButton.grid(row=0, column=0)
        self.saveButton.grid(row=0, column=1)
        self.loadButton.grid(row=0, column=2)

        ########### Data Configuration
        self.invalidLabel = tk.Label(self.wrapperField, text="Invalid field data:")
        self.invalidText = tk.Text(self.wrapperField, width=78, height=4, state="normal")  
        self.invalidLabel.grid(sticky=tk.NE, row=0, column=0, pady=10)   
        self.invalidText.grid(sticky=tk.NSEW, row=0, column=1, columnspan=2, padx=10, pady=10)

        ########### CSV Data Configuration
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

        self.trv = ttk.Treeview(self.tree_frame, columns=(1,2), show="headings",
            height="15", yscrollcommand=self.tree_scroll.set, selectmode="browse")
        self.trv.heading(1, text="Concept")
        self.trv.heading(2, text="Column name in CSV file")
        self.trv.column(1, width=150)
        self.trv.column(2, width=500)

        self.trv.tag_configure('oddrow', background='#E8E8E8')
        self.trv.tag_configure('evenrow', background='#A9DDD8')

        #Configure Tree Scrollbar
        self.tree_scroll.config(command=self.trv.yview)
        #Select row
        self.trv.bind('<Double 1>', lambda event: self.getrow(event, self.trv))

        self.tree_frame.pack()
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.trv.pack()

        ##### Period Configure
        self.trvPeriod = ttk.Treeview(self.wrapperPeriodConfigure, columns=(1,2), show="headings",
        height="4", selectmode="browse")
        self.trvPeriod.heading(1, text="Concept")
        self.trvPeriod.heading(2, text="Column name in CSV file")
        self.trvPeriod.column(1, width=150)
        self.trvPeriod.column(2, width=500)

        #Select row
        self.trvPeriod.bind('<Double 1>', lambda event: self.getrow(event, self.trvPeriod))

        self.trvPeriod.tag_configure('oddrow', background='#E8E8E8')
        self.trvPeriod.tag_configure('evenrow', background='#A9DDD8')
        self.trvPeriod.pack()

        self.fillConfigData()   

    def fillConfigData(self):
        #### Invalid Data
        self.invalidText.insert(tk.INSERT, self.parent.config['Invalid'])
        #### CSV Config Data
        count = 0
        for i in self.parent.config['CSV']:
            if (count % 2 == 0):
                self.trv.insert("", 'end',
                    values = (i, self.parent.config['CSV'][i]), tags=('evenrow') )
            else: 
                self.trv.insert("", 'end',
                    values = (i, self.parent.config['CSV'][i]), tags=('oddrow') )
            count+=1

        #### Period Config Data
        count = 0
        for i in self.parent.config['Period']:
            if (count % 2 == 0):
                self.trvPeriod.insert("", 'end',
                    values = (i, self.parent.config['Period'][i]), tags=('evenrow') )
            else: 
                self.trvPeriod.insert("", 'end',
                    values = (i, self.parent.config['Period'][i]), tags=('oddrow') )
            count+=1

    #TODO Warning OK Info Window 

    def applyButtonClick (self):
        #Set Config Dictionary
        #Invalidad Text
        self.parent.config['Invalid'] = self.invalidText.get("1.0",tk.END).strip()
        #Iterate Treview CSV
        for item in self.trv.get_children():
            field = self.trv.item(item=item)['values']
            self.parent.config['CSV'][field[0]] = field[1]
        #Iterate Treeview Period
        for item in self.trvPeriod.get_children():
            field = self.trvPeriod.item(item=item)['values']
            self.parent.config['Period'][field[0]] = field[1]
        print(self.parent.config)
        return True

    def saveButtonClick(self):
        with open('config.json', 'w') as save_file:
            json.dump(self.parent.config, save_file, indent=4, ensure_ascii=False)
        return True

    def updateConfigData(self):
        #Set Config Dictionary
        #Invalidad Text
        #self.parent.config['Invalid'] = self.invalidText.get("1.0",tk.END).strip()
        #Iterate Treview CSV
        for item in self.trv.get_children():
            field = self.trv.item(item=item)['values']
            self.trv.set(item=item, column=2, value=self.parent.config['CSV'][field[0]])
        #Iterate Treeview Period
        for item in self.trvPeriod.get_children():
            field = self.trvPeriod.item(item=item)['values']
            self.trvPeriod.set(item=item, column=2, value=self.parent.config['Period'][field[0]])
        return True

    def loadButtonClick(self):
        #filename = askopenfilename()
        #print(filename)
        config_backup = self.parent.config
        try:
            with open('config_default.json', 'r') as load_file:
                self.parent.config = json.load(load_file)
            self.updateConfigData()
            return True
        except:
            self.parent.config = config_backup
            print("ERROR")
            return False

    def getrow(self, event, who):
        rowid = who.identify_row(event.y)
        item = who.item(who.focus())
        focused = who.focus()
        user_input = simpledialog.askstring(title="Configure CSV Columns",
            prompt="Name of the column for " + item['values'][0] + "?",
            initialvalue = item['values'][1])
        if (user_input != None):
            who.item(focused, values=(item['values'][0], user_input))
#query_gui.py
from os import stat
import tkinter as tk
from tkinter import BooleanVar, Button, PhotoImage, ttk
from tkinter import messagebox
from tkinter import StringVar
from tkinter.filedialog import askopenfilename

from PIL import Image
from PIL import ImageTk

import json

from query_process import QueryProcess

class QueryGUI(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.tabControl = QueControl(self)
        self.tabControl.pack(expand= True, fill="both")


class QueControl(ttk.Notebook):
    def __init__(self, parent):
        ttk.Notebook.__init__(self, parent, style = 'Blue.TNotebook')
        self.parent = parent
        
        self.queryTab = QueryTab(self)
        self.add(self.queryTab, text="Search")
        self.sparqlTab = SparqlTab(self)
        self.add(self.sparqlTab, text="Sparql")
        self.queryManager = QueryProcess()


class QueryTab(tk.Frame):
    def __init__(self, parent:QueControl):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        
        self.select = [] #For selection purposes #TODO? uniform variables
        self.select_author = []
        self.select_material = []
        self.select_location = []
     
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
        self.connectLabel = tk.Label(self.wrapperConnect, text="Query Endpoint", anchor="w")
        self.connectLabel.grid(row=0, column=0, padx=10)
        self.connectEntry = tk.Entry(self.wrapperConnect, width= 50, bg='white')
        self.connectEntry.grid(sticky="we", row=0, column= 1, padx=5)
        self.testButton = tk.Button(self.wrapperConnect, text="Test...", command= self.testButtonClick, padx=30)
        self.testButton.grid(row=0, column=2, padx=10)

        self.connection_path = 'http://159.65.77.213:3030/dataset/query'
        self.connectEntry.insert(0, self.connection_path)

        self.updateEndpointLabel = tk.Label(self.wrapperConnect, text="Update Endpoint", anchor="w")
        self.updateEndpointLabel.grid(row=1, column=0, padx=10)
        self.updateEndpointEntry = tk.Entry(self.wrapperConnect, width= 50, bg='white')
        self.updateEndpointEntry.grid(sticky="we", row=1, column= 1, padx=5)

        self.updateEndpoint_path = 'http://159.65.77.213:3030/dataset/update'
        self.updateEndpointEntry.insert(0, self.updateEndpoint_path)

        self.userLabel = tk.Label(self.wrapperConnect, text="User", anchor="w")
        self.userLabel.grid(row=2, column=0, padx=10)
        self.userEntry = tk.Entry(self.wrapperConnect, width= 50, bg='white')
        self.userEntry.grid(sticky="we", row=2, column= 1, padx=5)

        self.passwordLabel = tk.Label(self.wrapperConnect, text="Password", anchor="w")
        self.passwordLabel.grid(row=3, column=0, padx=10)
        self.passwordEntry = tk.Entry(self.wrapperConnect, width= 50, bg='white', show='*')
        self.passwordEntry.grid(sticky="we", row=3, column= 1, padx=5)
        
        self.user = 'admin'
        self.userEntry.insert(0, self.user)
        self.password = 'curiocity@2021'
        self.passwordEntry.insert(0, self.password)

        #### LIST
        self.trv_frame = tk.Frame(self.wrapperList)
        self.trv_scroll_v = tk.Scrollbar(self.trv_frame)
        self.trv_scroll_h = tk.Scrollbar(self.trv_frame, orient=tk.HORIZONTAL)

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
                    10 : "About Donor",
                    11 : "Verified"}

        self.trv = ttk.Treeview(self.trv_frame, columns=list(range(0,len(headings))), show="headings",
            yscrollcommand=self.trv_scroll_v.set, xscrollcommand=self.trv_scroll_h.set,
            height="4", selectmode="browse")

        for i in headings:
            self.trv.heading(i, text=headings[i])
            self.trv.column(i, width=65, stretch=False)

        self.trv.tag_configure('oddrow', background='#E8E8E8')
        self.trv.tag_configure('evenrow', background='#A7D1E7')
        
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

        self.query1Entry = tk.Entry(self.wrapperQuery, width= 50, bg='white')
        self.query2Entry = tk.Entry(self.wrapperQuery, width= 50, bg='white')
        self.query3Entry = tk.Entry(self.wrapperQuery, width= 50, bg='white')
        self.query4Entry = tk.Entry(self.wrapperQuery, width= 50, bg='white')
        self.query5Entry = tk.Entry(self.wrapperQuery, width= 50, bg='white')

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

        self.wrapperInsertButtons = tk.LabelFrame(self.wrapperItem, text = "", bd=0) 

        self.idLabel = tk.Label(self.wrapperItem, text="ID", anchor="w")
        self.titleLabel = tk.Label(self.wrapperItem, text="Title", anchor="w")
        self.authorLabel = tk.Label(self.wrapperItem, text="Author", anchor="w")
        self.materialLabel = tk.Label(self.wrapperItem, text="Material", anchor="w")
        self.locationLabel = tk.Label(self.wrapperItem, text="Location", anchor="w")
        self.descriptionLabel = tk.Label(self.wrapperItem, text="Description", anchor="w")

        self.validatedValue = BooleanVar()
        self.validatedCheck = ttk.Checkbutton(self.wrapperItem,
            text="Validated", variable=self.validatedValue)
        self.validatedValue.set(False)

        update_photo = PhotoImage(master=self.parent.parent.parent.canvas, file='img/update1.png')
        search_photo = PhotoImage(master=self.parent.parent.parent.canvas, file='img/search-icon1.png')
        add_photo = PhotoImage(master=self.parent.parent.parent.canvas, file='img/add1.png')
        delete_photo = PhotoImage(master=self.parent.parent.parent.canvas, file='img/delete1.png')

        # self.idUpdButton = tk.Button(self.wrapperItem, text="Update",
        #     command= lambda: self.updateButtonClick('id'), state=tk.DISABLED, padx=30)
        self.titleUpdButton = tk.Button(self.wrapperItem, text="Update", image=update_photo,
            command= lambda:self.updateButtonClick('title'), state=tk.DISABLED, padx=30)
        self.titleUpdButton.image = update_photo
        self.validatedUpdButton = tk.Button(self.wrapperItem, text="Update", image=update_photo,
            command= lambda:self.updateButtonClick('validated'), state=tk.DISABLED, padx=30)
        self.validatedUpdButton.image = update_photo
        self.authorUpdButton = tk.Button(self.wrapperItem, text="Update", image=update_photo,
            command= lambda:self.updateButtonClick('author'), state=tk.DISABLED, padx=0)
        self.authorUpdButton.image = update_photo
        self.materialUpdButton = tk.Button(self.wrapperItem, text="Update", image=update_photo,
            command= lambda:self.updateButtonClick('material'), state=tk.DISABLED, padx=30)
        self.materialUpdButton.image = update_photo
        self.locationUpdButton = tk.Button(self.wrapperItem, text="Update", image=update_photo,
            command= lambda:self.updateButtonClick('location'), state=tk.DISABLED, padx=30)
        self.locationUpdButton.image = update_photo
        self.descriptionUpdButton = tk.Button(self.wrapperItem, text="Update", image=update_photo,
            command= lambda:self.updateButtonClick('description'), state=tk.DISABLED, padx=30)
        self.descriptionUpdButton.image = update_photo

        self.authorSearchButton = tk.Button(self.wrapperItem, text="Search", image=search_photo,
            command= lambda:self.searchWindowButtonClick('author'), state=tk.DISABLED, padx=0)
        self.authorSearchButton.image = search_photo
        self.materialSearchButton = tk.Button(self.wrapperItem, text="Search", image=search_photo,
            command= lambda:self.searchWindowButtonClick('material'), state=tk.DISABLED, padx=0)
        self.materialSearchButton.image = search_photo
        self.locationSearchButton = tk.Button(self.wrapperItem, text="Search", image=search_photo,
            command= lambda:self.searchWindowButtonClick('location'), state=tk.DISABLED, padx=0)
        self.locationSearchButton.image = search_photo

        self.artifactAddButton= tk.Button(self.wrapperItem, text="Add", image=add_photo,
            command= lambda:self.addButtonClick('artifact'), state=tk.NORMAL, padx=0)
        self.artifactAddButton.image = add_photo
        self.artifactDelButton= tk.Button(self.wrapperItem, text="Delete", image=delete_photo,
            command= lambda:self.deleteButtonClick('artifact'), state=tk.NORMAL, padx=0)
        self.artifactDelButton.image = delete_photo


        self.buttons = [self.validatedUpdButton, self.titleUpdButton,
            self.authorUpdButton, self.materialUpdButton, self.locationUpdButton, self.descriptionUpdButton]
        self.searchButtons = [self.materialSearchButton, self.authorSearchButton, self.locationSearchButton]

        self.idEntry = tk.Entry(self.wrapperItem, width= 30, bg='white',
            disabledbackground='white', disabledforeground='gray', state=tk.DISABLED)
        self.titleEntry = tk.Entry(self.wrapperItem, width= 30, bg='white',
            disabledbackground='white', disabledforeground='gray')
        self.authorEntry = tk.Entry(self.wrapperItem, width= 30, bg='white',
            disabledbackground='white', disabledforeground='gray', state=tk.DISABLED)
        self.materialEntry = tk.Entry(self.wrapperItem, width= 30, bg='white',
            disabledbackground='white', disabledforeground='gray', state=tk.DISABLED)
        self.locationEntry = tk.Entry(self.wrapperItem, width= 30, bg='white',
            disabledbackground='white', disabledforeground='gray', state=tk.DISABLED)
        self.descriptionEntry = tk.Entry(self.wrapperItem, width= 30, bg='white', disabledbackground='white', disabledforeground='gray')

        # self.idEntry.bind('<Key>', lambda event: self.activateButton(event, self.idUpdButton) )
        self.validatedCheck.bind('<Button>', lambda event: self.activateButton(event, self.validatedUpdButton) )
        self.titleEntry.bind('<Key>', lambda event: self.activateButton(event, self.titleUpdButton) )
        self.authorEntry.bind('<Key>', lambda event: self.activateButton(event, self.authorUpdButton) )
        self.materialEntry.bind('<Key>', lambda event: self.activateButton(event, self.materialUpdButton) )
        self.locationEntry.bind('<Key>', lambda event: self.activateButton(event, self.locationUpdButton) )
        self.descriptionEntry.bind('<Key>', lambda event: self.activateButton(event, self.descriptionUpdButton) )

        self.idLabel.grid(sticky="w", row= 0, column=0, pady=5)
        self.idEntry.grid(sticky="we", row=0, column= 1, padx=5)
        self.artifactAddButton.grid(row=0, column= 2, padx=5)
        self.artifactDelButton.grid(row=0, column= 3, padx=5)
        ttk.Separator(self.wrapperItem, orient=tk.VERTICAL).grid(sticky="ns", row=0, column=4)
        self.validatedCheck.grid(sticky="we", row=0, column= 5, padx=5)
        self.validatedUpdButton.grid(row=0, column= 6)

        self.titleLabel.grid(sticky="w", row= 1, column=0, pady=5)
        self.titleEntry.grid(sticky="we",row=1, column= 1, columnspan=5, padx=5)
        self.titleUpdButton.grid(row=1, column= 6, padx=5)

        self.authorLabel.grid(sticky="w", row= 2, column=0, pady=5)
        self.authorEntry.grid(sticky="we",row=2, column= 1, columnspan=5, padx=5)
        self.authorUpdButton.grid(row=2, column= 6, padx=5)
        self.authorSearchButton.grid(row=2, column=7)

        self.materialLabel.grid(sticky="w", row= 3, column=0, pady=5)
        self.materialEntry.grid(sticky="we",row=3, column= 1, columnspan=5, padx=5)
        self.materialUpdButton.grid(row=3, column= 6, padx=5)
        self.materialSearchButton.grid(row=3, column=7)

        self.locationLabel.grid(sticky="w", row= 4, column=0, pady=5)
        self.locationEntry.grid(sticky="we",row=4, column= 1, columnspan=5, padx=5)
        self.locationUpdButton.grid(row=4, column= 6, padx=5)
        self.locationSearchButton.grid(row=4, column=7)

        self.descriptionLabel.grid(sticky="w", row= 5, column=0, pady=5)
        self.descriptionEntry.grid(sticky="we",row=5, column= 1, columnspan=5, padx=5)
        self.descriptionUpdButton.grid(row=5, column= 6, padx=5)

        self.wrapperInsertButtons.grid(row=6, columnspan=6, padx=20)

        self.okInsertButton = tk.Button(self.wrapperInsertButtons, text="Ok", command= self.insertOkButtonClick, padx=30)
        # self.okInsertButton.grid(row=0, column=0, padx=5, pady=10)
        # self.okInsertButton.grid_forget()
        self.cancelInsertButton = tk.Button(self.wrapperInsertButtons, text="Cancel", command= self.insertCancelButtonClick, padx=30)
        # self.cancelInsertButton.grid(row=0, column=1, padx=5, pady=10)
        # self.cancelInsertButton.grid_forget()


        
        #### END ITEM DATA
    def deleteButtonClick(self, type):
        #TODO type of delete
        id = self.idEntry.get()
        #ask for confirmation
        if (messagebox.askyesno("Delete artifact", "Do you really want to eliminate this object?")):
            #ID not exists show error
            if (self.parent.queryManager.checkID(id) ):
                if (self.parent.queryManager.deleteQuery(id)):
                    messagebox.showinfo("Success", "Object eliminated successfully")
                    return True
                else:
                    messagebox.showerror("Error", "There was an error while attempting to eliminate object")    
                    return False
            else:
                #ID not exists, show error
                messagebox.showerror("Error", "ID not exist in repository")
                return False
        

    def addButtonClick(self, option):
        #Show Ok & Cancel Buttons
        self.okInsertButton.grid(row=0, column=0, padx=5)
        self.cancelInsertButton.grid(row=0, column=1, padx=5)
        #Enable search buttons & Id Entry
        for button in self.searchButtons:
            button.configure(state=tk.NORMAL)
        self.idEntry.configure(state=tk.NORMAL)

        return True

    def insertOkButtonClick(self):
        #Check for full entries 
        for child in self.wrapperItem.winfo_children():
            if (child.winfo_class() == 'Entry'):
                if (child.get() == ''):
                    messagebox.showerror("Error", "Please fill out all form entries")
                    return False
        #Check if ID Exist
        if ( messagebox.askyesno("Add new artifact", "Do you want to create a new artifact?")):
            id = self.idEntry.get()
            if (self.parent.queryManager.checkID(id) ):
                #ID exists, show error
                messagebox.showerror("Error", "ID exists in repository already!")
                return False
            else:
                author = "<" + self.select_author[0] + ">"
                material = "<" + self.select_material[0] + ">"
                location = "<" + self.select_location[0] + ">"
                if (self.parent.queryManager.insertQuery(id=id, title=self.titleEntry.get(),
                    author=author, material= material, location= location,
                    description= self.descriptionEntry.get() )):
                    messagebox.showinfo("Info", "Artifact data inserted correctly!")
                    return True
                else:
                    messagebox.showerror("Error", "Error inserting Artifact data")
                    return False
        else:
            return False
        
    def insertCancelButtonClick(self):
        self.okInsertButton.grid_forget()
        self.cancelInsertButton.grid_forget()
        # Disable ID Entry      
        self.idEntry.configure(state=tk.DISABLED)
        return True
    
    def activateButton(self, event, button):
        button['state'] = 'normal'

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
        
        response = self.parent.queryManager.combinedQuery(queryList)
        ### Fill treeview with response
        self.trv.delete(*self.trv.get_children())
        count = 0
        for row in response:
            if (count % 2 == 0):    
                self.trv.insert('','end',values=(
                    row['id_l']['value'],
                    row['artifact_l']['value'],
                    row['author_l']['value'],
                    row['material_l']['value'],
                    row['location_l']['value'],
                    row['period_l']['value'],
                    row['begin_d']['value'],
                    row['end_d']['value'],
                    row['note']['value'],
                    row['donor_l']['value'],
                    row['note_donor']['value'],
                    row['verified']['value']) , tags=('evenrow'))
            else:
                self.trv.insert('','end',values=(
                    row['id_l']['value'],
                    row['artifact_l']['value'],
                    row['author_l']['value'],
                    row['material_l']['value'],
                    row['location_l']['value'],
                    row['period_l']['value'],
                    row['begin_d']['value'],
                    row['end_d']['value'],
                    row['note']['value'],
                    row['donor_l']['value'],
                    row['note_donor']['value'],
                    row['verified']['value']) , tags=('oddrow'))
            count+=1
        
    def insertVal(self, obj, value):
        obj.delete(0, tk.END)
        obj.insert(0, value)

    def getrow(self, event):
        # Call for Double click in Treeview
        #rowid = self.trv.identify_row(event.y)
        self.item = self.trv.item(self.trv.focus())
        #Insert values in Entrys for edition
        self.__updateDisabledEntry( self.idEntry, self.item['values'][0])
        self.insertVal( self.titleEntry, self.item['values'][1])
        self.__updateDisabledEntry( self.authorEntry, self.item['values'][2])
        self.__updateDisabledEntry( self.materialEntry, self.item['values'][3])
        self.__updateDisabledEntry( self.locationEntry, self.item['values'][4])
        self.insertVal( self.descriptionEntry, self.item['values'][8])

        if (self.item['values'][11] == 'true'):
            self.validatedValue.set(True)
        else:
            self.validatedValue.set(False)     
        self.__DisableButtonsExcept()

    def testButtonClick(self):
        endpoint = self.connectEntry.get()
        if (self.parent.queryManager.testConnection(endpoint)):
            self.connection_path = endpoint
            #Enable buttons after test connection     
            # self.titleUpdButton['state'] = tk.NORMAL
            # self.authorUpdButton['state'] = tk.NORMAL
            # self.materialUpdButton['state'] = tk.NORMAL
            # self.locationUpdButton['state'] = tk.NORMAL
            # self.descriptionUpdButton['state'] = tk.NORMAL
            self.authorSearchButton['state'] = tk.NORMAL
            self.materialSearchButton['state'] = tk.NORMAL
            self.locationSearchButton['state'] = tk.NORMAL

            messagebox.showinfo("Test", "Server connection is Ok!")
        else:
            messagebox.showerror("Test", "Error connecting to server...")   

    def updateButtonClick(self, field:str):
        id = self.item['values'][0]
        before = ''
        after = ''
        ## Update from Entry value
        if (field == 'id'):
            before=self.item['values'][0]
            after=self.idEntry.get()
        elif (field == 'title'):
            before= "\"" + self.item['values'][1] + "\""
            after= "\"" + self.titleEntry.get() + "\""
        elif (field == 'description'):
            before= "\"" + self.item['values'][8] + "\""
            after= "\"" + self.descriptionEntry.get() + "\""
        ## Update from self.select
        elif (field == 'author'):
            before = '?author'
            after = "<" + self.select[0] + ">"
            # return True
        elif (field == 'material'):
            before = '?material'
            after = "<" + self.select[0] + ">"
            # return True
        elif (field == 'location'):
            before = '?location'
            after = "<" + self.select[0] + ">"
            # return True
        elif (field == 'validated'):
            if (self.item['values'][11] == 'true'):
                before = ':Verified'
                after = ':Unverified'
            else:
                before = ':Unverified'
                after = ':Verified'
        self.parent.queryManager.updateQuery(field, id, before, after)

    def searchWindowButtonClick(self, field:str):
        newWindow = InstanceWindow(self, field)
        newWindow.title("Instances of " + field)
        ### Get Instance from popup window
        self.wait_window(newWindow)
        if (self.select != []):
            if (field == 'author'):
                self.__updateDisabledEntry(self.authorEntry, self.select[1])
                self.__DisableButtonsExcept(self.authorUpdButton)
            if (field == 'material'):
                self.__updateDisabledEntry(self.materialEntry, self.select[1])
                self.__DisableButtonsExcept(self.materialUpdButton)
            if (field == 'location'):
                self.__updateDisabledEntry(self.locationEntry, self.select[1])
                self.__DisableButtonsExcept(self.locationUpdButton)
        return True
    
    def __updateDisabledEntry(self, entry:tk.Entry, value):
        entry.configure(state=tk.NORMAL)
        self.insertVal( entry, value=value )
        entry.configure(state=tk.DISABLED)

    def __DisableButtonsExcept(self, button:tk.Button=None):
        #Disable buttons except related
        for i in self.buttons:
            if (i == button):
                i['state'] = tk.NORMAL
            else:
                i['state'] = tk.DISABLED
        

class SparqlTab(tk.Frame):
    def __init__(self, parent:QueControl):
        tk.Frame.__init__(self, parent)
        # self.queryManager = QueryProcess()
        self.parent = parent

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
        response = self.parent.queryManager.customQuery(query)
        response = json.dumps(response, indent=2)
        self.respText.insert(tk.INSERT, response)

class InstanceWindow(tk.Toplevel):
    def __init__(self, parent:QueryTab, instance):
        tk.Toplevel.__init__(self, parent)

        self.parent = parent
        self.instance = instance

        # self.dic_instances_select = {
        #     'author' : self.parent.select_author,
        #     'material' : self.parent.select_material,
        #     'location' : self.parent.select_location}

        self.wrapperList = tk.LabelFrame(self, text = "Item List", bd=3)
        self.wrapperList.pack(fill="both", expand="yes", padx=20)

        self.wrapperButton = tk.LabelFrame(self, text = "", bd=0)
        self.wrapperButton.pack(fill="both", expand="yes", padx=20)
        
        #### LIST
        self.trv_frame = tk.Frame(self.wrapperList)
        self.trv_scroll_v = tk.Scrollbar(self.trv_frame)
        self.trv_scroll_h = tk.Scrollbar(self.trv_frame, orient=tk.HORIZONTAL)

        #Headings for treeview
        headings = {0 : "ID",
                    1 : "Label"}

        self.trv = ttk.Treeview(self.trv_frame, columns=list(range(0,len(headings))), show="headings",
            yscrollcommand=self.trv_scroll_v.set, xscrollcommand=self.trv_scroll_h.set,
            height="4", selectmode="browse")

        for i in headings:
            self.trv.heading(i, text=headings[i])
            self.trv.column(i, width=150, stretch=False)

        self.trv.tag_configure('oddrow', background='#E8E8E8')
        self.trv.tag_configure('evenrow', background='lightgray')
        
        self.trv_scroll_v.config(command=self.trv.yview)
        self.trv_scroll_h.config(command=self.trv.xview)

        self.trv_frame.pack(fill="both", expand="yes")
        self.trv_scroll_v.pack(side=tk.RIGHT, fill=tk.Y)
        self.trv_scroll_h.pack(side=tk.BOTTOM, fill=tk.X)
        self.trv.pack(fill="both", expand="yes")

        #### Buttons
        self.searchEntry = tk.Entry(self.wrapperButton, width= 20)
        self.searchButton = tk.Button(self.wrapperButton, text="Search", command= self.searchButtonClick, padx=30)
        self.okButton = tk.Button(self.wrapperButton, text="OK", command= self.okButtonClick, padx=30)
        self.cancelButton = tk.Button(self.wrapperButton, text="Cancel", command= self.cancelButtonClick, padx=30)
        
        self.searchEntry.grid(row=0, column= 0, padx=10)
        self.searchButton.grid(row=0, column= 1, padx=10)
        self.okButton.grid(row=1, column=0, padx=10)
        self.cancelButton.grid(row=1, column=1, padx=10)

    def searchButtonClick(self):

        response = self.parent.parent.queryManager.instanceQuery(self.instance, self.searchEntry.get().strip())
        self.trv.delete(*self.trv.get_children())
        for i in response:
            self.trv.insert('','end',values=i)
        return True

    def okButtonClick(self):
        item = self.trv.item(self.trv.focus())
        if (item['values'] != ''):
            self.parent.select = item['values']
            if ( self.instance == 'author'):
                self.parent.select_author = item['values']
            elif ( self.instance == 'material'):
                self.parent.select_material = item['values']
            elif ( self.instance == 'location'):
                self.parent.select_location = item['values']
            self.destroy()
    
    def cancelButtonClick(self):
        self.destroy()
        return True
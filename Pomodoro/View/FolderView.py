from tkinter import *
from .NotifyView import NotifyView


class FolderView(Frame):
    def __init__(self, master):
        super().__init__(master, bg="white", height=600, width=1000)
        self.Fid = 0

        self.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.place_forget()
        self.visible = False
        self.NotifyView = NotifyView(self)
        # Close button
        self.closeBtn = Button(
            self,
            text="X",
            bg="red",
            fg="White",
            padx=20,
            pady=10
        )
        self.closeBtn.place(relx=1.0, rely=0.0, anchor=NE)

        # Table container
        self.table = Frame(self, bg="white")
        self.table.place(relx=0.5, rely=0.5, anchor=CENTER)
        
      


        # Submit button
        self.submitBtn = Button(
            self,
            text="Ok",
            fg="White",
            padx=20,
            bg="green",
            pady=10        
        )
        self.submitBtn.place(relx=0.9, rely=0.9, anchor="se")

    def renderItem(self, i, f,addLoad,addDelete,addCreate,addCreateTask):
        #accept function
        Label(self.table, text=str(i), bg="white", font=("Arial", 11)).grid(row=i, column=0, sticky="w", padx=10, pady=5)
        Label(self.table, text=f["FolderName"], bg="white", font=("Arial", 11)).grid(row=i, column=1, sticky="w", padx=10, pady=5)
        Button(self.table, text="Open", padx=10,
               command=lambda: self.renderDetail(f,addLoad,addDelete,addCreate,addCreateTask)).grid(row=i, column=2, sticky="w", padx=10, pady=5)
      
        #load btn
        load_btn = Button(
          self.table, 
          text="Load", 
          padx=10)
        
        load_btn.config(command=lambda Fid=f["Fid"]: addLoad(Fid))

         # placing
        load_btn.grid(row=i, column=3, sticky="w", padx=5, pady=5)
          
        #delete btn
        del_btn = Button(
            self.table,
            text = "Delete",
            padx=10
        )

        del_btn.config(command=lambda Fid=f["Fid"]:addDelete(Fid))

        #placing
        del_btn.grid(row=i,column=4,sticky="w",padx=0,pady=5)

    def folder_input(self,add_folder):
        i=self.Fid + 1

        # Index
        Label(self.table, text=str(i), bg="white", font=("Arial", 11)).grid(
            row=i, column=0, sticky="w", padx=10, pady=5
        )

        # Folder Name input
        NameEntry = Entry(self.table, bg="white", font=("Arial", 11))
        NameEntry.insert(0, "") 
        NameEntry.grid(row=i, column=1, sticky="w", padx=10, pady=5)

       

        #Add button
        Add_button = Button(
            self.table,
            text="Add",
            command= lambda Fid = i : add_folder(NameEntry.get().strip()),
            bg="lightgreen",
            font=("Arial", 10)
        )

        #place
        Add_button.grid(row=i, column=2, padx=10, pady=5)

    def task_input(self,folder,Fid, row, add_task=None):
        #index
        index_label = Label(self.table, text=row, bg="white", font=("Arial", 11))
        index_label.grid(row=row, column=0,padx=10, pady=5,sticky="w")

        # Entry for task title
        task_entry = Entry(self.table, font=("Arial", 11), width=25)
        task_entry.grid(row=row, column=1, padx=10, pady=5, sticky="w")

        # Spinbox for Pomodoro count
        pomodoro_entry = Spinbox(
            self.table,
            from_=0, to=10,
            width=5,
            font=("Arial", 10)
        )
        pomodoro_entry.grid(row=row, column=2, padx=10, pady=5, sticky="w")

        # Save button
        save_btn = Button(
            self.table,
            text="Save",
            font=("Arial", 10),
            bg="lightgreen"
        )
        save_btn.grid(row=row, column=3, padx=10, pady=5)

        # Hook save button to handler

     
        save_btn.config(
            command=lambda: add_task(
                folder,
                task_entry.get().strip(),
                int(pomodoro_entry.get())
            )
        )
       
    def renderHeader(self,add_folder):
        Label(self.table, text="Index", font=("Arial", 12, "bold"), bg="white", padx=10).grid(row=0, column=0, sticky="w")
        Label(self.table, text="Title", font=("Arial", 12, "bold"), bg="white", padx=10).grid(row=0, column=1, sticky="w")
        Label(self.table, text="Action", font=("Arial", 12, "bold"), bg="white", padx=10).grid(row=0, column=2, sticky="w")

        Button(
            self.table,
            text="Create Folder",
            bg="blue",
            fg="white",
            padx=10,
            pady=5,
            command=add_folder
        ).grid(row=0, column=3, sticky="e", padx=10)


     
      

    def renderDetail(self, folder,handler,handler2,handler3,create_task):
        # clear table first
        for widget in self.table.winfo_children():
            widget.destroy()

        # Header row
        headers = ["Index", "Title", "Pomodoro"]
        for col, header in enumerate(headers):
            Label(
                self.table,
                text=header,
                font=("Arial", 14, "bold"),
                bg="white",
                padx=10,
                pady=5
            ).grid(row=0, column=col, sticky="w")

        #add task
        Button(
            self.table, text="Add +", padx=10,
            command=lambda: create_task(folder,folder["Fid"],len(folder.get("Tasks", [])) + 1)
        ).grid(row=0, column=4, sticky="w")


        # Render tasks
        if(folder.get("Tasks", [])):
            for i, task in enumerate(folder.get("Tasks", []), start=1):
                Label(self.table, text=str(i), bg="white", font=("Arial", 11)).grid(row=i, column=0, sticky="w", padx=10, pady=5)
                Label(self.table, text=task.get("Tcontent", ""), bg="white", font=("Arial", 11)).grid(row=i, column=1, sticky="w", padx=10, pady=5)
                Label(self.table, text=task.get("Pomodoro", ""), bg="white", font=("Arial", 11)).grid(row=i, column=2, sticky="w", padx=10, pady=5)
        else:
          i = 1

        # Back button 
        Button(self.table, text="Back", padx=10,
                command=lambda: self.renderList(self.lastFolders,handler,handler2,handler3,create_task)
        ).grid(row=i+1, column=0, columnspan=4, pady=15)

      
    

   

    def renderList(self, folders,handler,handler2,handler3,handler4):
        #get load function from controller 

        self.lastFolders = folders  # store for back button
        # Clear old table
        for widget in self.table.winfo_children():
            widget.destroy()

        # Table headers
        self.renderHeader(handler3)

        # Populate rows
        for i, f in enumerate(folders, start=1):
            self.renderItem(i, f,handler,handler2,handler3,handler4)
            self.Fid += 1
    
    def clear_folder(self):
     for widget in self.table.winfo_children():
        widget.destroy()
     self.Fid = 0


    

    def show(self, folders,handler,handler2,handler3,handler4):
        self.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.visible = True
        self.renderList(folders,handler,handler2,handler3,handler4)

    def hide(self):
        self.place_forget()
        self.visible = False

    def toggleModal(self, folders,handler,handler2,handler3,handler4):
        if not self.visible:
            self.show(folders,handler,handler2,handler3,handler4)
        else:
            self.hide()

    def popout(self,msg,bg = "green",fg = "white",config=False,
            delay = 3000):
        if config:
            self.NotifyView.config(bg=bg)
            self.NotifyView.msg.config(fg=fg,bg=bg)
        if not config:
            #set back to default 
            self.NotifyView.config(bg=bg)
            self.NotifyView.msg.config(fg=fg,bg=bg)
        self.NotifyView.show(msg)
        self.after(delay, self.NotifyView.hide)          
                    
    def renderControl(self,handler):
        handler()


    def closeControl(self, handler):
        self.closeBtn.config(command=handler)

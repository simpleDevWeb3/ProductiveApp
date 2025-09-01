from tkinter import *
from .NotifyView import NotifyView


class FolderView(Frame):
    def __init__(self, master):
        super().__init__(master, bg="white", height=600, width=1000)

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

    def renderItem(self, i, f,addLoad,addDelete):
        #accept function
        Label(self.table, text=str(i), bg="white", font=("Arial", 11)).grid(row=i, column=0, sticky="w", padx=10, pady=5)
        Label(self.table, text=f["FolderName"], bg="white", font=("Arial", 11)).grid(row=i, column=1, sticky="w", padx=10, pady=5)
        Button(self.table, text="Open", padx=10,
               command=lambda: self.renderDetail(f,addLoad,addDelete)).grid(row=i, column=2, sticky="w", padx=10, pady=5)
      
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


    def renderHeader(self):
        Label(self.table, text="Index", font=("Arial", 12, "bold"), bg="white", padx=10).grid(row=0, column=0, sticky="w")
        Label(self.table, text="Title", font=("Arial", 12, "bold"), bg="white", padx=10).grid(row=0, column=1, sticky="w")
        Label(self.table, text="Action", font=("Arial", 12, "bold"), bg="white", padx=10).grid(row=0, column=2, sticky="w")
      

    def renderDetail(self, folder,handler,handler2):
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

        # Render tasks
        for i, task in enumerate(folder.get("Tasks", []), start=1):
            Label(self.table, text=str(i), bg="white", font=("Arial", 11)).grid(row=i, column=0, sticky="w", padx=10, pady=5)
            Label(self.table, text=task.get("Tcontent", ""), bg="white", font=("Arial", 11)).grid(row=i, column=1, sticky="w", padx=10, pady=5)
            Label(self.table, text=task.get("Pomodoro", ""), bg="white", font=("Arial", 11)).grid(row=i, column=2, sticky="w", padx=10, pady=5)

        # Back button 
        Button(self.table, text="Back", padx=10,
                command=lambda: self.renderList(self.lastFolders,handler,handler2)
        ).grid(row=i+1, column=0, columnspan=4, pady=15)
            

   

    def renderList(self, folders,handler,handler2):
        #get load function from controller 

        self.lastFolders = folders  # store for back button
        # Clear old table
        for widget in self.table.winfo_children():
            widget.destroy()

        # Table headers
        self.renderHeader()

        # Populate rows
        for i, f in enumerate(folders, start=1):
            self.renderItem(i, f,handler,handler2)
    
    def clear_folder(self):
     for widget in self.table.winfo_children():
        widget.destroy()

    def show(self, folders,handler,handler2):
        self.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.visible = True
        self.renderList(folders,handler,handler2)

    def hide(self):
        self.place_forget()
        self.visible = False

    def toggleModal(self, folders,handler,handler2):
        if not self.visible:
            self.show(folders,handler,handler2)
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


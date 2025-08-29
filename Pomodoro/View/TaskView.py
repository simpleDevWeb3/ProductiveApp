from tkinter import *

class TaskView(Frame):
    def __init__(self, master):
        super().__init__(master, bg="#BA4949")
        self.pack(fill="both", expand=True)
      
        # Task Section Container
        self.TaskSection = Frame(self, bg="#BA4949", width=500, height=350)
        self.TaskSection.pack(expand=True)
        self.TaskSection.pack_propagate(False)

        #Current Task working
        self.currentTaskSection = Frame(self.TaskSection,bg="#BA4949")
        self.currentTaskSection.pack(fill='x',padx=20,pady=1)

        self.currentTask = Label(self.currentTaskSection, text="Welcome Back!", fg="white", bg="#BA4949", font=("Arial", 20, "bold"))
        self.currentTask.pack(anchor=CENTER)

        # Header Section for title + add button
        self.HeaderSection = Frame(self.TaskSection, bg="#BA4949")
        self.HeaderSection.pack(fill='x', padx=20, pady=(20, 5))

        # Title (left)
        self.Title = Label(self.HeaderSection, text="Task", fg="white", bg="#BA4949", font=("Arial", 20, "bold"))
        self.Title.pack(side=LEFT)

        # Add Task Button (right)
        self.AddBtn = Button(self.HeaderSection,
                             text="+ Add Task",
                             font=("Arial", 12),
                             bg="#BA4949",
                             fg="#FFFFFF",
                             padx=10,
                             pady=5,
                             borderwidth=0,
                             highlightthickness=0,
                             activebackground="#BA4949",  # optional: keep consistent on click
                             activeforeground="#FFFFFF") 
        self.AddBtn.pack(side=RIGHT)

        # Bottom border under HeaderSection
        self.borderLine = Frame(self.TaskSection, bg="white", height=2)
        self.borderLine.pack(fill='x', padx=20, pady=(0, 10))

        # Task list area (placeholder)
        self.TaskList = Frame(self.TaskSection, bg="#BA4949")
        self.TaskList.pack(fill='both', expand=True, padx=20)

       
        #init Id for btn
        self.task_counter = 0 




    def AddTaskHandler(self,handler):
        self.AddBtn.config(command=handler)
       # print(data)
    
    def Render(self,data,addDelete):
        task_frame = Frame(self.TaskList, bg="#E39090", height=50)
        task_frame.pack(fill=X, pady=5)
        task_frame.pack_propagate(False)

        task_entry = Label(task_frame, font=("Arial", 12), width=30, text=data["Tcontent"], fg="white",bg="#E39090")
   
        task_entry.pack(side=LEFT, padx=10, pady=10)

        pomodoro_entry = Label(
          task_frame, 
          text=f"{data["Count"]}/{data["Pomodoro"]}",
          width=5,
          fg="white",
          bg="#E39090",
         )

        pomodoro_entry.pack(side=LEFT,padx=8,pady=10)

        delete_btn = Button(task_frame,
                        text="Delete",
                        font=("Arial", 10),
                        bg="#D96F6F",
                        fg="white")
        delete_btn.config(command=lambda tid=data["Tid"], b=delete_btn, e=task_entry: addDelete(tid, b, e))
        delete_btn.pack(side=RIGHT, padx=10)
        for key, value in data.items():
                print(f"{key}: {value}")
    
    def genId(self,task):
    #function to genereate latest id
        currentId = None
        task_id = None
        i = 0
        for t in task:
            i += 1
            if i == len(task): 
                currentId = t["Tid"]

        if currentId is not None:
            task_id = int(currentId) + 1
        else:
            task_id = 1 

        return task_id
    #function to clear ui inside task list
    def clear_task(self):
        for widget in self.TaskList.winfo_children():
            widget.destroy()


    def renderInputTodo(self,AddTask,task):

        task_id = self.genId(task)#generate latest id 

        self.AddBtn.config(state=DISABLED)
        # Create task frame
        task_frame = Frame(self.TaskList, bg="#E39090", height=50)
        task_frame.pack(fill=X, pady=5)
        task_frame.pack_propagate(False)

        # Entry widget for task description
        task_entry = Entry(task_frame, font=("Arial", 12), width=30)
        task_entry.pack(side=LEFT, padx=10, pady=10)

        #Spinbox widget for pomodoro number
        pomodoro_entry = Spinbox(
        task_frame, 
        from_=0, to=10,
        width=5,
        font=("Arial", 10)
        )
        
        pomodoro_entry.pack(side=LEFT,padx=8,pady=10)
     

        # Save button (with ID and reference)
        save_btn = Button(task_frame,
                        text="Save",
                        font=("Arial", 10),
                        bg="#D96F6F",
                        fg="white")
        save_btn.config(command=lambda tid=task_id, btn=save_btn, entry=task_entry ,frame= task_frame, pomodoro= pomodoro_entry : AddTask(tid,frame, btn, entry,pomodoro))
        save_btn.pack(side=RIGHT, padx=10)
        
    def disRunTask(self,data):
        currentTask = data[0]["Tcontent"]
        index = data[0]["Tid"]
        self.currentTask.config(text=f"#{index} {currentTask}")
        
    def disSnozzing(self):
        self.currentTask.config(text="Snozzing Time!")
    def renderMsg(self,msg):
        self.currentTask.config(text=msg)

    def RenderTask(self,data,addDelete):
     
         for task in data:
            print(task)
            self.Render(task,addDelete)
            self.task_counter+=1

 
               

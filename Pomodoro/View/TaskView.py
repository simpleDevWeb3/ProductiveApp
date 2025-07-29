from tkinter import *

class TaskView(Frame):
    def __init__(self, master):
        super().__init__(master, bg="#BA4949")
        self.pack(fill="both", expand=True)

        # Task Section Container
        self.TaskSection = Frame(self, bg="#BA4949", width=500, height=350)
        self.TaskSection.pack(expand=True)
        self.TaskSection.pack_propagate(False)

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
    
    def createTask(self):
        self.task_counter += 1
        task_id = self.task_counter
        self.AddBtn.config(state=DISABLED)
        # Create task frame
        task_frame = Frame(self.TaskList, bg="#E39090", height=50)
        task_frame.pack(fill=X, pady=5)
        task_frame.pack_propagate(False)

        # Entry widget for task description
        task_entry = Entry(task_frame, font=("Arial", 12), width=30)
        task_entry.pack(side=LEFT, padx=10, pady=10)

        # Save button (with ID and reference)
        save_btn = Button(task_frame,
                        text="Save",
                        font=("Arial", 10),
                        bg="#D96F6F",
                        fg="white")
        save_btn.config(command=lambda tid=task_id, b=save_btn, e=task_entry: self.AddTask(tid, b, e))
        save_btn.pack(side=RIGHT, padx=10)

    def AddTask(self, tid, button, entry):
        task_text = entry.get().strip()

        if task_text:
            print(f"[Task #{tid}] Saved: {task_text}")
            entry.config(bg="#E39090")
            entry.config(state="readonly")
            button.config(text="Delete", command=lambda: self.removeTask(tid, button, entry))
        
            self.AddBtn.config(state=NORMAL)
        else:
            print(f"[Task #{tid}] Empty! Please type something.")

    def removeTask(self, tid, button, entry):
        task_frame = button.master
        task_frame.destroy()
        print(f"[Task #{tid}] Removed.")
                
    def AddTaskHandler(self):
        self.AddBtn.config(command=self.createTask)

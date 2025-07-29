from tkinter import *

class SettingView(Frame):
    def __init__(self,master):
      super().__init__(master, bg="white", height=500,width=500)
      self.place(relx=0.5, rely=0.5,anchor=CENTER)
      self.place_forget()
      self.visible = False

      self.closeBtn = Button(
         self,
         text="X",
         bg="red",
         fg="White",
         padx=20,
         pady=10
      )
      self.submitBtn = Button(
         self,
         text="Ok",
         fg="White",
         padx=20,
         bg="green",
         pady=10        
      )
      self.resetBtn = Button(
         self,
         text="Reset",
         fg="White",
         padx=20,
         bg="red",
         pady=10        
      )
      self.Title = Label(
         self,
         text="Settings",
         font=("Arial",20,"bold"),
         bg="White"
      )
     
      self.TimerSection = Frame(
         self,
         padx=10,
         pady=10
      )
      self.TimerTitle = Label(
         self.TimerSection,
         text="Timer",
         font=("Arial",15,"bold")
      )
      self.PomoLabel = Label(
         self.TimerSection, 
         text="Pomodoro",
         font=("Arial",15,"bold")
      )
      self.ShortLabel = Label(
         self.TimerSection, 
         text="Short Break",
         font=("Arial",15,"bold")
      )
      self.LongLabel = Label(
         self.TimerSection, 
         text="Long Break",
         font=("Arial",15,"bold")
      )
      self.inputPomodoro =Spinbox(
          self.TimerSection, 
          from_=0, to=100,
          width=5,
          font=("Arial", 20)
         )
      self.inputLongBreak =Spinbox(
          self.TimerSection, 
          from_=0, to=100,
          width=5,
          font=("Arial", 20)
         )
      self.inputShortBreak=Spinbox(
          self.TimerSection, 
          from_=0, to=100,
          width=5,
          font=("Arial", 20)
         )

      self.Title.place(x=20,y=10,anchor=NW)
      self.closeBtn.place(relx=1.0, rely=0.0, anchor=NE) 
      self.TimerSection.place(relx=0.5, rely=0.5, anchor="center")
      self.TimerTitle.grid(
         row=0,
         column=2, 
      )
      self.PomoLabel.grid(
         row=1, 
         column=1, 
         padx=5, 
         pady=5
      )
      self.LongLabel.grid(
         row=1, 
         column=2, 
         padx=5, 
         pady=5
      )
      self.ShortLabel.grid(
         row=1, 
         column=3, 
         padx=5, 
         pady=5
      )
      self.inputPomodoro.grid(
         row=2, 
         column=1, 
         padx=5, 
         pady=5
      )
      self.inputShortBreak.grid(
         row=2, 
         column=2, 
         padx=5, 
         pady=5
      )
      self.inputLongBreak.grid(
         row=2, 
         column=3, 
         padx=5, 
         pady=5
      )
      self.resetBtn.place(
          relx=0.1,
          rely=0.9,
          anchor="sw"
       )
      self.submitBtn.place(
         relx=0.9,
         rely=0.9,
         anchor="se"
      )
      
    
    def show(self):
        # Show and center the frame
        self.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.visible = True

    def hide(self):
        # Show and center the frame
        self.place_forget()
        self.visible = False

    def toggleModal(self):
        if not self.visible:
          self.show()
        elif self.visible:
          self.hide()

    def closeControl(self,handler):
       self.closeBtn.config(command=handler)


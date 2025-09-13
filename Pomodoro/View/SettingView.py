from tkinter import *
from .NotifyView import NotifyView

class SettingView(Frame):
    def __init__(self,master):
      super().__init__(master, bg="white", height=500,width=500)
      self.place(relx=0.5, rely=0.5,anchor=CENTER)
      self.place_forget()
      self.visible = False
      self.NotifyView = NotifyView(self)
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
      self.inputShortBreak=Spinbox(
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
      self.ShortLabel.grid(
         row=1, 
         column=2, 
         padx=5, 
         pady=5
      )
      self.LongLabel.grid(
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
      
    #Notification helper
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

    def show(self,pomodoro,shortBreak,longBreak):
        # Show and center the frame
        self.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.visible = True

        self.inputLongBreak.delete(0, "end")
        self.inputLongBreak.insert(0,longBreak)

        self.inputShortBreak.delete(0, "end")
        self.inputShortBreak.insert(0,shortBreak)

        self.inputPomodoro.delete(0, "end")
        self.inputPomodoro.insert(0,pomodoro)
        print(pomodoro,shortBreak,longBreak)

       

    def hide(self):
        # Show and center the frame
        
        self.place_forget()
        self.visible = False

    def toggleModal(self,pomodoro,shortBreak,longBreak):
        if not self.visible:
          self.show(pomodoro,shortBreak,longBreak)
        elif self.visible:
          self.hide()

    def closeControl(self,handler):
       self.closeBtn.config(command=handler)
   
   
    def get_timer(self,handler):
      pomodoro = self.inputPomodoro.get()
      shortbreak = self.inputShortBreak.get()
      longbreak = self.inputLongBreak.get()
  
      handler(pomodoro, shortbreak, longbreak)
   
    def set_timer(self,handler):
       self.get_timer(handler)

    def reset_timer(self,handler):
      self.inputPomodoro.delete(0, "end")   # clear any old text
      self.inputPomodoro.insert(0, "25")   # set new text

      self.inputShortBreak.delete(0, "end")   # clear any old text
      self.inputShortBreak.insert(0, "5")   # set new text

      self.inputLongBreak.delete(0, "end")   # clear any old text
      self.inputLongBreak.insert(0, "10")   # set new text
      self.popout("Timer reset!")
      self.get_timer(handler)

    def saveControl(self,handler):
      self.submitBtn.config(command=lambda: self.set_timer(handler))

   
    def resetControl(self,handler):
       self.resetBtn.config(command=lambda: self.reset_timer(handler))


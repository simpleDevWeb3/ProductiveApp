from tkinter import *
from .Pomodoro import Pomodoro
 
# Application 
class PomodoroApp(Tk):
    def __init__(self):
        super().__init__() 
        self.geometry("500x350")
        self.title("Pomodoro Timer")
        
        
        self.Main=Pomodoro(self)

        self.mainloop()


#Application #2

#Application #3


#Start Application
PomodoroApp()
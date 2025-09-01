from tkinter import *
from Pomodoro.Pomodoro import Pomodoro
 
# Application 
class App(Tk):
    def __init__(self):
        super().__init__() 
        self.geometry("500x350")
        self.title("Pomodoro Timer")
        
        
        self.Main=Pomodoro(self)

        self.mainloop()

#Start Application
App()


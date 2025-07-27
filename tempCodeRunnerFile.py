from tkinter import *
from Pomodoro.Pomodoro import Pomodoro

class App(Tk):
    def __init__(self):
        super().__init__() 
        self.geometry("600x400")
        self.title("Pomodoro Timer")
        
        
        self.Main=Pomodoro(self)

        self.mainloop()

App()


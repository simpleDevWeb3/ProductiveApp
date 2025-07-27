from tkinter import *
from .View.NavView import Navbar
from .View.TimerView import TimerView
from .Controller import init

class Pomodoro(Frame):
    def __init__(self,master):
        super().__init__(master,bg='#BA4949')
        self.pack(expand=True, fill="both")
        self.navbar = Navbar(self)
        self.timerView = TimerView(self)
        init(self.timerView) 

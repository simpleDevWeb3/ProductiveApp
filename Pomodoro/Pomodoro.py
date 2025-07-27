from tkinter import *
from .Model import Model
from .View.NavView import Navbar
from .View.TimerView import TimerView


class Pomodoro(Frame):

    def __init__(self,master):
        super().__init__(master,bg='#BA4949')
        self.pack(expand=True, fill="both")
        self.navbar = Navbar(self)
        self.timerView = TimerView(self)
        self.timerId = None  
        self.init()
        
        #config 
        self.mode = Model.State["CurrentMode"] 
        self.min = Model.Timer[Model.State["CurrentMode"]]["Minute"]
        self.sec = Model.Timer[Model.State["CurrentMode"]]["Seconds"]
################################### ##################





    ################################
    #TIMER
    ##################################
    def startTimer(self):
         if Model.State["isStart"]:  # prevent timer goe crazy
             return
         
         Model.State["isStart"] = True
         self.countdown()
         self.timerView.renderTimer(self.min,self.sec)
         self.timerView.toggleStartButtonText(Model.State["isStart"])

    def stopTimer(self):
         Model.State["isStart"] = False
         if self.timerId:
            self.after_cancel(self.timerId)
            self.timerId = None
         self.timerView.renderTimer(self.min,self.sec)
         self.timerView.toggleStartButtonText(Model.State["isStart"])
    
    def countdown(self):
        if Model.State["isStart"]:
            #guarding operation before minus min
            if self.sec > 0:

                self.sec-= 1

            elif self.min > 0:

                self.min -= 1
                self.sec = 59

            else:
                self.stopTimer()
                self.resetTimer()
                return  # timer ends

            self.timerView.renderTimer(self.min,self.sec)
            self.timerId = self.after(1000, self.countdown) 

    def timerControl(self):
        #Timer Mode
        print(self.min,self.sec)

        self.timerView._startBtn.config(state=DISABLED)
        self.after(300, lambda: self.timerView._startBtn.config(state=NORMAL))
        
    

        if Model.State["isStart"] == False:
            self.startTimer()
        else:
            self.stopTimer()

  
      
    ###########################################

    ########Config Timer########
    
    def resetTimer(self):
       self.min = Model.Timer[Model.State["CurrentMode"]]["Minute"]
       self.sec = Model.Timer[Model.State["CurrentMode"]]["Seconds"]

    def modeControl(self,timerMode):
        print(timerMode)

        self.mode = timerMode  
       
        Model.State["CurrentMode"] = timerMode 
        self.stopTimer()
        self.resetTimer()
     
        self.timerView.renderTimer(self.min,self.sec)
            
        
        # Highlight the right button
        if self.mode == "Pomodoro":
            self.timerView.highlightModeButton(self.timerView.pomodoroBtn)
        elif self.mode == "ShortBreak":
            self.timerView.highlightModeButton(self.timerView.shortBreakBtn)
        elif self.mode == "LongBreak":
            self.timerView.highlightModeButton(self.timerView.longBreakBtn)

    ######################

     
    def init(self):
         self.timerView.setStartHandler(self.timerControl)
         self.timerView.setModeHandler(self.modeControl)

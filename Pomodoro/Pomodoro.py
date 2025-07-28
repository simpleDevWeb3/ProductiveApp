from tkinter import *
from .Model import Model
from .View.NavView import Navbar
from .View.TimerView import TimerView


class Pomodoro(Frame):

    def __init__(self,master):
        super().__init__(master,bg='#BA4949')
        #UI Container
        self.pack(expand=True, fill="both")
        self.navbar = Navbar(self)
        self.timerView = TimerView(self)
        self.timerId = None  
       
        
        # config
       # self.state = Model.get_state()
        #self.mode,Model.get_Mode() = self.state.get("CurrentMode"),self.state.get("isStart")  

        #self.timer = Model.get_timer(self.mode)     
        #self.min, self.sec = self.timer.get("Minute", 0), self.timer.get("Seconds", 0)

        #UI Event Listener
        self.init()
################################### ##################





    ################################
    #TIMER
    ##################################
    def startTimer(self):
         if Model.get_Start():  # prevent timer goe crazy
             return
         
         #Model.State["isStart"] = True
         Model.set_Start(True)
         print(Model.get_Start(),"From start Timer")
         
         self.countdown()
         self.timerView.renderTimer(Model.get_timer('Min'),Model.get_timer('Sec'))
         self.timerView.toggleStartButtonText(Model.get_Start())

    def stopTimer(self):
         Model.set_Start(False)
         if self.timerId:
            self.after_cancel(self.timerId)
            self.timerId = None
         self.timerView.renderTimer(Model.get_timer('Min'),Model.get_timer('Sec'))
         self.timerView.toggleStartButtonText(Model.get_Start())
         print(Model.get_Mode())
    def countdown(self):
     if Model.get_Start():
        min_left = Model.get_timer("Min")
        sec_left = Model.get_timer("Sec")

        if sec_left > 0:
            Model.decrease_Timer("Sec", 1)
        elif min_left > 0:
            Model.decrease_Timer("Min", 1)
            Model.set_Timer("Sec", 59)
        else:
            self.stopTimer()
            Model.resetTimer()
            self.timerView.renderTimer(Model.get_timer('Min'), Model.get_timer('Sec'))
            return  # Timer ends

        # Update timer view
        self.timerView.renderTimer(Model.get_timer('Min'), Model.get_timer('Sec'))
        self.timerId = self.after(1000, self.countdown)

    def timerControl(self):
        #Timer Mode
        print(Model.Timer)

        self.timerView._startBtn.config(state=DISABLED)
        self.after(300, lambda: self.timerView._startBtn.config(state=NORMAL))
        
    

        if not Model.get_Start():
            self.startTimer()
        else:
            self.stopTimer()

  
      
    ###########################################

    ########Config Timer########
    

    def modeControl(self,timerMode):
        print(timerMode)

        #self.mode = timerMode  
        #Model.State["CurrentMode"] = timerMode 

        Model.set_Mode(timerMode)
        self.stopTimer()
        Model.resetTimer()
     
        self.timerView.renderTimer(Model.get_timer('Min'),Model.get_timer('Sec'))
            
        
        # Highlight the right button
        if Model.get_Mode() == "Pomodoro":
            self.timerView.highlightModeButton(self.timerView.pomodoroBtn)
        elif Model.get_Mode() == "ShortBreak":
            self.timerView.highlightModeButton(self.timerView.shortBreakBtn)
        elif Model.get_Mode() == "LongBreak":
            self.timerView.highlightModeButton(self.timerView.longBreakBtn)

    ######################

     
    def init(self):
         self.timerView.setStartHandler(self.timerControl)
         self.timerView.setModeHandler(self.modeControl)

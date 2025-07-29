from tkinter import *
from .Model import Model
from .View.TimerView import TimerView
from .View.SettingView import SettingView
from .View.TaskView import TaskView

# Pomodoro Initialize  
class Pomodoro(Frame):

    def __init__(self,master):
        super().__init__(master,bg='#BA4949')
        #UI Container
        self.pack(expand=True, fill="both")
    
        self.timerView = TimerView(self)
        self.TaskView = TaskView(self)

        self.timerId = None  
        self.overlay = Frame(self,bg="#555555")
        self.settingView =SettingView(self.overlay)
      
       
        self.openModal = False
        self.init()
################################### ##################
    ##############################
    #Navigation Bar
    ##############################
    
    
    def settingControl(self):
      print("Setting")
      if not self.openModal:
        self.overlay.place(x=0, y=0, relwidth=1, relheight=1)
        self.settingView.toggleModal()
        self.openModal = True
      elif self.openModal:
        self.overlay.place_forget()
        self.settingView.toggleModal()
        self.openModal = False


    




    ###################################


    ################################
    #TIMER
    ##################################
    def startTimer(self):
         
         print(Model.get_timer('Min'),Model.get_timer('Sec'))
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
        print("sec_left", sec_left)

        if min_left == 0 and sec_left == 0:
            self.stopTimer()
            Model.resetTimer()
            self.timerView.renderTimer(Model.get_timer('Min'), Model.get_timer('Sec'))
            return  # Timer ends
        if sec_left > 0:
            Model.decrease_Timer("Sec", 1)
        elif min_left > 0:
            Model.decrease_Timer("Min", 1)
            Model.set_Timer("Sec", 59)

        Model.save_data()

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
    
    def changeMode(self,timerMode):
        Model.set_Mode(timerMode)
        self.timerView.renderTimer(Model.get_timer('Min'),Model.get_timer('Sec'))

         # Highlight the right button
        if Model.get_Mode() == "Pomodoro":
            self.timerView.highlightModeButton(self.timerView.pomodoroBtn)
        elif Model.get_Mode() == "ShortBreak":
            self.timerView.highlightModeButton(self.timerView.shortBreakBtn)
        elif Model.get_Mode() == "LongBreak":
            self.timerView.highlightModeButton(self.timerView.longBreakBtn)

    def modeControl(self,timerMode):
        print(timerMode)

        #self.mode = timerMode  
        #Model.State["CurrentMode"] = timerMode 
        # setting mode base on button type
        Model.set_Mode(timerMode)

        # stop timer
        self.stopTimer()
        # reset Timer to the Mode state
        Model.resetTimer()

        #Render Mode Timer
        self.changeMode(timerMode)

       # self.timerView.renderTimer(Model.get_timer('Min'),Model.get_timer('Sec'))
            
        
       

    ######################

     
    def init(self):
         #LOAD CLIENT DATA
         Model.load_data()
         print("init", Model.get_timer('Min'),Model.get_timer('Sec'))

         #RENDER TIMER
         self.timerView.renderTimer(Model.get_timer('Min'),Model.get_timer('Sec'))
        
        #CHECK WETHER BEFORE TIMER IS START? 
         if Model.get_Start():
            print("run timer ")
            print(Model.Timer)
            self.startTimer()

        # render client current mode
         self.changeMode(Model.get_Mode())
         
         #self.modeControl(Model.get_Mode())
        
        
        # attached handler for button
         self.timerView.setSettingHandler(self.settingControl)
       
          
         self.timerView.setStartHandler(self.timerControl)
         self.timerView.setModeHandler(self.modeControl)
         self.settingView.closeControl(self.settingControl)

         self.TaskView.AddTaskHandler()

       

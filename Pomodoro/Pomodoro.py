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
        self.task_counter = 0
       
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
         if Model.get_Mode() == "Pomodoro":
            self.TaskView.disRunTask(Model.get_task())
         else:
            self.TaskView.disSnozzing()

    def stopTimer(self):
         Model.set_Start(False)
         if self.timerId:
            self.after_cancel(self.timerId)
            self.timerId = None
         self.timerView.renderTimer(Model.get_timer('Min'),Model.get_timer('Sec'))
         self.timerView.toggleStartButtonText(Model.get_Start())
         print(Model.get_Mode())

        
    def taskDone(self):
        Model.remove_Task(Model.getFirstTid())
        print("Before",Model.Task)
        Model.load_data()
        print("After",Model.Task)
        self.TaskView.clear_task()
        self.TaskView.RenderTask(Model.Task,self.RemoveTask)

    def countdown(self):
     if Model.get_Start():
        min_left = Model.get_timer("Min")
        sec_left = Model.get_timer("Sec")
        print("sec_left", sec_left)

        if min_left == 0 and sec_left == 0:
            self.stopTimer()
            Model.resetTimer()
            self.timerView.renderTimer(Model.get_timer('Min'), Model.get_timer('Sec'))

            if Model.get_Mode() == "Pomodoro":
                #self.taskDone()
                if(len(Model.Task)>0 ):
                    print("counting")
                    Model.set_Count(+1)
                    self.TaskView.clear_task()
                    self.TaskView.RenderTask(Model.Task,self.RemoveTask)
                    
                    if Model.Task[0]["Pomodoro"] == Model.Task[0]["Count"]:
                        self.taskDone()
                        
                self.modeControl("ShortBreak")
                self.TaskView.renderMsg("Let's Take a Break!")
                
            elif Model.get_Mode() == "ShortBreak" or "LongBreak":
                self.modeControl("Pomodoro")
                self.TaskView.renderMsg("Let's Focus Now!")

           
            return  # Timer ends
        if sec_left > 0:
            Model.decrease_Timer("Sec", 1)
        elif min_left > 0:
            Model.decrease_Timer("Min", 1)
            Model.set_Timer("Sec", 59)

        Model.save_data()

        # Update timer view
        self.timerView.renderTimer(Model.get_timer('Min'), Model.get_timer('Sec'))
        self.timerId = self.after(1, self.countdown)

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
        print(timerMode)
        print(Model.get_timer('Min'))
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
   
        if timerMode == "Pomodoro":
            self.TaskView.renderMsg("Let's Start Focus!")
        else:
            self.TaskView.renderMsg("Let's Take A Break!") 

       # self.timerView.renderTimer(Model.get_timer('Min'),Model.get_timer('Sec'))
            
        
       

    ######################
    def SaveTask(self, tid,frame, button, entry,spinbox):
        task_text = entry.get().strip()
        pomodoro_num = int(spinbox.get().strip())
        if task_text and pomodoro_num > 0:
            print(f"[Task #{tid}] Saved: {task_text}")
            TContent = task_text
            Tid = tid
            Pomodoro = pomodoro_num
            Model.create_Task(Tid,TContent,Pomodoro)
            frame.destroy()
            entry.destroy()
            spinbox.destroy()
            button.destroy()
           
            self.TaskView.Render(Model.Task[-1],self.RemoveTask)
            self.TaskView.AddBtn.config(state="normal")    
          
           
        else:
            print(f"[Task #{tid}] Empty! Please type something or Pomodor must > 0.")

    def RemoveTask(self, tid, button, entry):
        task_frame = button.master
        task_frame.destroy()
        Model.remove_Task(tid)
        print(f"[Task #{tid}] Removed.")
            
    def createTask(self):
        #render task
        self.TaskView.renderInputTodo(self.SaveTask,Model.Task)
        

        #save data
    def TaskController(self):
        self.createTask()
     
    def init(self):
         #LOAD CLIENT DATA
         Model.load_data()
         print(Model.Task)
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
         #render task
         self.TaskView.RenderTask(Model.Task,self.RemoveTask)
        
        # attached handler for button
         self.timerView.setSettingHandler(self.settingControl)
       
          
         self.timerView.setStartHandler(self.timerControl)
         self.timerView.setModeHandler(self.modeControl)
         self.settingView.closeControl(self.settingControl)

         self.TaskView.AddTaskHandler(self.TaskController)
       

       

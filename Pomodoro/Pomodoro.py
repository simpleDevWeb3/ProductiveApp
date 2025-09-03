from tkinter import *
from .Model import Model
from .View.TimerView import TimerView
from .View.SettingView import SettingView
from .View.TaskView import TaskView
from .View.NotifyView import NotifyView
from .View.FolderView import FolderView
import time
import winsound

# Pomodoro Initialize  
class Pomodoro(Frame):

    def __init__(self,master):
        super().__init__(master,bg='#BA4949')

        #Fid
        self.Fid = 0

        #UI Container
        self.pack(expand=True, fill="both")
    
        self.timerView = TimerView(self)
        self.TaskView = TaskView(self)
        self.NotifyView = NotifyView(self)
   
        self.timerId = None  
        self.overlay = Frame(self,bg="#555555")
        self.settingView =SettingView(self.overlay)
        self.FolderView = FolderView(self.overlay)
        self.task_counter = 0
         
        self.openModal = False
        self.init()

################################### ##################
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

    #ring bgm 
    def ring(self,seconds,ring_file):
       for remaining in range(seconds, 0, -1):
        print(f"Time left: {remaining}", end="\r")
        time.sleep(1)

        # Play once at the end
        winsound.PlaySound(ring_file, winsound.SND_FILENAME | winsound.SND_ASYNC)
            
    ##############################
    #Navigation Bar
    ##############################

    def loadControl(self,id):
     #Get Folder Name
     FName = ""

     #data logic only
     #delete original task
     # make shallow copy of task so it wont effect real data
     for t in  Model.get_task().copy():
        print("Wanted delete: ", t["Tid"])
        Model.remove_Task(t["Tid"])


     #replace the task
     for i, f in enumerate(Model.get_folder(), start=1):
        if(id == f["Fid"]):
            print(f"Folder {i}: {f['FolderName']}")
            folder = f 
            FName = f["FolderName"]
            for j, t in enumerate(folder.get("Tasks", []), start=1): 
                print(f"   Task {j}: {t['Tcontent']} | Time: {t.get('Time','')} | Pomodoro: {t.get('Pomodoro','')}")
                Model.create_Task(t["Tcontent"],t["Pomodoro"])

     #view logic 
     # delete previouse view
     self.TaskView.clear_task()

     # rerender view with new data
     self.TaskView.RenderTask(Model.Task,self.RemoveTask)
     #close modal
     self.folderControl()
     #msg
     self.popout(f"{FName} loaded succesfully")
    
    def folderControl(self):
      print("Setting")
      #render modal
      if not self.openModal:
        self.overlay.place(x=0, y=0, relwidth=1, relheight=1)
        self.FolderView.toggleModal(Model.get_folder(),self.loadControl,self.delFolder,self.F_createControl,self.F_saveTaskControl,self.F_delTaskControl)
        self.openModal = True

      #close modal
      elif self.openModal:
        self.overlay.place_forget()
        self.FolderView.toggleModal(Model.get_folder(),self.loadControl,self.delFolder,self.F_createControl,self.F_saveTaskControl,self.F_delTaskControl)
        self.openModal = False

    def delFolder(self,Fid):
       #delete data 
       S_Folder = Model.remove_folder(Fid)
       #clear view
       self.FolderView.clear_folder()

       #render back view
       self.FolderView.renderList(Model.get_folder(),self.loadControl,self.delFolder,self.F_createControl,self.F_saveTaskControl,self.F_delTaskControl)       

       #Msg
       self.FolderView.popout(f"Folder #[{S_Folder["FolderName"]}] deleted!")

                
   
    
    def F_add_folder(self,Fname):
        print("Fname ", Fname)

        #creat folder data
        Model.create_folder(Fname)

        #clear view
        self.FolderView.clear_folder()

        #rerender view
        self.FolderView.renderList(Model.get_folder(),self.loadControl,self.delFolder,self.F_createControl,self.F_saveTaskControl,self.F_delTaskControl)



    def F_createControl(self):
        self.FolderView.folder_input(self.F_add_folder)
    
    def settingControl(self):
      print("Setting")
      if not self.openModal:
        self.overlay.place(x=0, y=0, relwidth=1, relheight=1)
        self.settingView.toggleModal(Model.get_timerMode("Pomodoro"),Model.get_timerMode("ShortBreak"),Model.get_timerMode("LongBreak"))
        self.openModal = True

      elif self.openModal:
        self.overlay.place_forget()
        self.settingView.toggleModal(Model.get_timerMode("Pomodoro"),Model.get_timerMode("ShortBreak"),Model.get_timerMode("LongBreak"))
        self.openModal = False
    
    def F_createTask(self,Folder,task_name,pomodoro):
        print("Task: " + task_name)

        #create task data 
        Model.f_create_Task(Folder,task_name,pomodoro)

        #clear view
        self.FolderView.clear_folder()

        #rerender view
        self.FolderView.renderDetail(Folder,self.loadControl,self.delFolder,self.F_createControl,self.F_saveTaskControl,self.F_delTaskControl)

    def F_saveTaskControl(self,folder,Fid,row):
        
        self.FolderView.task_input(folder,Fid,row,self.F_createTask)
    
    def F_delTaskControl(self,Folder,Task):
        Tid = Task["Tid"]
        #delete task data
        Model.f_remove_task(Folder,Tid)
        #clear view
        self.FolderView.clear_folder()
        #rerender view
        self.FolderView.renderDetail(Folder,self.loadControl,self.delFolder,self.F_createControl,self.F_saveTaskControl,self.F_delTaskControl)

    def setTimer (self,pomodoro,shortBreak,longBreak):
        Model.set_TimerMode("Pomodoro",pomodoro)
        Model.set_TimerMode("ShortBreak",shortBreak)
        Model.set_TimerMode("LongBreak",longBreak)
        Model.resetTimer()
        self.timerView.renderTimer(Model.get_timer('Min'),Model.get_timer('Sec'))
    
        
        




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
        self.popout(f"Task #[{Model.getFirstTid()}] done!")
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
            Model.create_Task(TContent,Pomodoro)
            frame.destroy()
            entry.destroy()
            spinbox.destroy()
            button.destroy()
           
            self.TaskView.Render(Model.Task[-1],self.RemoveTask)
            self.TaskView.AddBtn.config(state="normal")    
            self.popout(f"[Task #{tid} Added!")
        elif task_text == "":
            self.popout(f"[Task #{tid}] Empty! Please type something ","red","white",True)
        else:
            self.popout(f"[Task #{tid}] Session must atleast 1 ","red","white",True)

    def RemoveTask(self, tid, button, entry):
        task_frame = button.master
        task_frame.destroy()
        Model.remove_Task(tid)
        self.popout(f"[Task #{tid}] Removed.")
            
    def createTask(self):
        #render task
        self.TaskView.renderInputTodo(self.SaveTask,Model.Task)
        
 
            
    #save data
    def TaskController(self):
        self.createTask()

    ###########################################################
    #Folder function
    ###########################################################

     
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
         self.TaskView.setFolderHandler(self.folderControl)


        # attached handler for button
         self.timerView.setSettingHandler(self.settingControl)
         
    
         self.timerView.setStartHandler(self.timerControl)
         self.timerView.setModeHandler(self.modeControl)
         

         
         self.settingView.closeControl(self.settingControl)
         self.settingView.saveControl(self.setTimer)
         self.settingView.resetControl(self.setTimer)

         self.FolderView.closeControl(self.folderControl)



         self.TaskView.AddTaskHandler(self.TaskController)
       

       

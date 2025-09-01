from .Config import *  # Must define: Minute, Seconds, Min, Sec, isStart, CurrentMode, DATA_FILE
import json
import os

# Get client Data and Write client data
class Model:
    Mode = {}
    State = {}
    Timer = {}
    Task = []
    Folder = []
    @staticmethod
    def load_data():
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as file:
                data = json.load(file)
                Model.Mode = data.get("Mode", {})
                Model.State = data.get("State", {})
                Model.Timer = data.get("Timer", {})
                Model.Task = data.get("Task",[])
                Model.Folder = data.get("Folder",[])
        else:
            print(" File does not exist. Using defaults.")
            # Default values for first-time users
            Model.Mode = {
                "Pomodoro": {Minute: 25, Seconds: 0},
                "ShortBreak": {Minute: 5, Seconds: 0},
                "LongBreak": {Minute: 10, Seconds: 0}
            }
            Model.State = {
                isStart: False,
                CurrentMode: "Pomodoro"
                
            }
            Model.Task = [
                {
                    "Tid":1,
                    "Tcontent":"Sleep",
                    "Pomodoro":1,
                    "Sec_Left": 200,
                    "Count":0
                },

                {
                    "Tid":2,
                    "Tcontent":"Wakeup",
                    "Pomodoro":1,
                    "Sec_Left":200,
                    "Count":0
                }
            ]
            Model.Folder = [
                {   "Fid":1,
                    "FolderName": "Morning Routine",
                    "Tasks": [
                        {
                            "Tid": 1,
                            "Tcontent": "Sleep",
                            "Pomodoro": 1,
                            "Sec_Left": 200,
                            "Count": 0
                        },
                        {
                            "Tid": 2,
                            "Tcontent": "Wakeup",
                            "Pomodoro": 1,
                            "Sec_Left": 200,
                            "Count": 0
                        }
                    ]
                },
                {   "Fid":2,
                    "FolderName": "Work",
                    "Tasks": [
                        {
                            "Tid": 3,
                            "Tcontent": "Coding",
                            "Pomodoro": 2,
                            "Sec_Left": 300,
                            "Count": 0
                        }
                    ]
                }
            ]
            Model.resetTimer()
            Model.save_data() 

        

    @staticmethod
    def save_data():
        with open(DATA_FILE, 'w') as file:
            json.dump({
                "Mode": Model.Mode,
                "State": Model.State,
                "Timer": Model.Timer,
                "Task": Model.Task,
                "Folder":Model.Folder
            }, file, indent=4)

    def f_create_Task(Folder,Task,pomodoro):
        print("Ongoing create: ", Task)
        F = Folder
        for f in Model.Folder:
         if F["Fid"] == f["Fid"]:
            if len(F["Tasks"]) > 0:
             print("Creating....")
             last_task = F["Tasks"][-1]
             new_id = last_task["Tid"] + 1
            else:
             print("Creating.... first task")
             new_id = 1

            f["Tasks"].append(
                {
                    "Tid": new_id,
                    "Tcontent": Task,     
                    "Pomodoro": pomodoro,
                    "Count":0,
                }
            )
            Model.save_data()

    def f_remove_task(Folder:dict, Tid):
        F = Folder
        delete_item  =  None
        select_folder = None
        print("delete task: " , Tid)

        for f in Model.Folder:
            if F["Fid"] == f["Fid"]:
              select_folder = f
              break

        for t in select_folder["Tasks"]:
            if t["Tid"] == Tid:
              delete_item = t
              break
    
        if delete_item:
           select_folder["Tasks"].remove(delete_item)
           Model.save_data()
        return



    @staticmethod
    def create_Task(Task,pomodoro):
        print("Ongoing create: ", Task)

        if len(Model.Task) > 0:
         print("Creating....")
         last_task = Model.Task[-1]
         new_id = last_task["Tid"] + 1
        else:
         print("Creating.... first task")
         new_id = 1
     

        Model.Task.append(
            {
                "Tid": new_id,
                "Tcontent": Task,     
                "Pomodoro": pomodoro,
                "Count":0,
                
            })
        Model.save_data()
    
    @staticmethod
    def remove_Task(selected_id):
        print(selected_id)
        deleteItem  = None
        for task in Model.Task:
            if task["Tid"] == selected_id:
                deleteItem = task
                print(task)
        if deleteItem:
            print("delete", deleteItem)
            Model.Task.remove(deleteItem)
            Model.save_data()
        else:
            print("Not found task")

    @staticmethod
    def getFirstTid():
        return Model.Task[0]["Tid"]
    
    @staticmethod
    def get_timer(key):
        return Model.Timer.get(key, 0)


    
    @staticmethod
    def set_Count(val):
        Model.Task[0]["Count"]+= val
        Model.save_data()
    @staticmethod
    def set_Timer(key, val):
        Model.Timer[key] = val
        Model.save_data()

    @staticmethod
    def set_TimerMode(key,val):
        Model.Mode[key]["Minute"] = int(val)
        Model.save_data()

    @staticmethod
    def decrease_Timer(key, val):
        Model.Timer[key] -= val
        Model.save_data()
        # Optionally auto-save: Model.save_data()

    @staticmethod
    def resetTimer():
        mode = Model.State[CurrentMode]
        Model.Timer[Min] = Model.Mode[mode][Minute]
        Model.Timer[Sec] = Model.Mode[mode][Seconds]
        Model.save_data()

    @staticmethod
    def get_folder():
        return Model.Folder 
    
    @staticmethod
    def get_s_folder(Fid):
        SelectedFolder = None
        for Folder in Model.Folder:
            if Folder["Fid"] == Fid:
                SelectedFolder= Folder
                print(SelectedFolder)
                return SelectedFolder
        return ""
    
    @staticmethod
    def remove_folder(Fid):
        print("Delete data: ", Fid)
        deleteItem  =  Model.get_s_folder(Fid)
         
        if deleteItem:
            print("delete", deleteItem)
            Model.Folder.remove(deleteItem)
            Model.save_data()
            return deleteItem
        else:
            print("Not found task")
   
    @staticmethod         
    def create_folder(FolderName):
        #get last folder id 
        if len(Model.Folder)> 0:
            last_folder = Model.Folder[-1]
            new_id = last_folder["Fid"] + 1
        else:
            new_id = 1

        Model.Folder.append(
            {
                "Fid": new_id,
                "FolderName":FolderName,
                "Tasks":[]
                
            })
        Model.save_data()

    @staticmethod
    def get_state():
        return Model.State
    @staticmethod
    def get_task():
        print(Model.Task)
        return Model.Task


    @staticmethod
    def get_timerMode(mode):
        return Model.Mode.get(mode)['Minute']
    @staticmethod
    def get_Mode():
        return Model.State.get(CurrentMode)

    @staticmethod
    def get_Start():
        return Model.State.get(isStart)

    @staticmethod
    def set_Mode(mode):
        Model.State[CurrentMode] = mode
        #Model.resetTimer()
        Model.save_data()

    @staticmethod
    def set_Start(start):
        Model.State[isStart] = start
        Model.save_data()

   

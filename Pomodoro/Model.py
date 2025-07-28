from .Config import *

class Model:

    # Modes and their predefined time values
    Mode = {
        "Pomodoro": {
            Minute: 25,
            Seconds: 0
        },
        "ShortBreak": {
            Minute: 5,
            Seconds: 0
        },
        "LongBreak": {
            Minute: 10,
            Seconds: 0
        }
    }

    
    State = {
        isStart: False,
        CurrentMode: "Pomodoro"
    }

   
    Timer = {
        Min: Mode[State[CurrentMode]][Minute],
        Sec: Mode[State[CurrentMode]][Seconds]
    }

    @staticmethod
    def get_timer(key):
        return Model.Timer.get(key, 0)
    
    @staticmethod
    def set_Timer(key, val):
        Model.Timer[key] = val

    @staticmethod
    def decrease_Timer(key, val):
        Model.Timer[key] -= val

    @staticmethod
    def resetTimer():
        mode = Model.State[CurrentMode]
        Model.Timer[Min] = Model.Mode[mode][Minute]
        Model.Timer[Sec] = Model.Mode[mode][Seconds]
    
    @staticmethod
    def get_state():
        return Model.State

    @staticmethod
    def get_Mode():
        return Model.State.get(CurrentMode)

    @staticmethod
    def get_Start():
        return Model.State.get(isStart)

    @staticmethod
    def set_Mode(mode):
        Model.State[CurrentMode] = mode
        Model.resetTimer()
    
    @staticmethod
    def set_Start(start):
        Model.State[isStart] = start

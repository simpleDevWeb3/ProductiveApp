from .Config import *  # Must define: Minute, Seconds, Min, Sec, isStart, CurrentMode, DATA_FILE
import json
import os

class Model:
    Mode = {}
    State = {}
    Timer = {}

    @staticmethod
    def load_data():
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as file:
                data = json.load(file)
                Model.Mode = data.get("Mode", {})
                Model.State = data.get("State", {})
                Model.Timer = data.get("Timer", {})
        else:
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
            Model.resetTimer()

        

    @staticmethod
    def save_data():
        with open(DATA_FILE, 'w') as file:
            json.dump({
                "Mode": Model.Mode,
                "State": Model.State,
                "Timer": Model.Timer
            }, file, indent=4)

    @staticmethod
    def get_timer(key):
        return Model.Timer.get(key, 0)

    @staticmethod
    def set_Timer(key, val):
        Model.Timer[key] = val
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
        #Model.resetTimer()
        Model.save_data()

    @staticmethod
    def set_Start(start):
        Model.State[isStart] = start
        Model.save_data()

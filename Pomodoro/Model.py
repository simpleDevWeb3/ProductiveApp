class Model:
    Minute = "Minute"
    Seconds = "Seconds"
    isStart = "isStart"
    CurrentMode= "CurrentMode"
  
    Timer ={
        "Pomodoro": {
            Minute: 25,
            Seconds: 0
        },
       "ShortBreak": {
            Minute:  5,
            Seconds: 0
        },
        "LongBreak": {
            Minute: 10,
            Seconds: 0
        }
    }
        
    State = {
        isStart : False,
        CurrentMode : 'Pomodoro'
    }
    

    

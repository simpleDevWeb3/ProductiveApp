from .Model import Model

def timerControl():
  print(Model.Timer)



def init(TimerView):
    TimerView.setStartHandler(timerControl)

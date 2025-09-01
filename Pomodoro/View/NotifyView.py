from tkinter import *
class NotifyView(Frame):
  def __init__(self,master, height=55,width=400):
    #placeholder
    super().__init__(master, bg="green", height=height,width=width)
    self.place(relx=0.5, y=-height, anchor="n")

    #msg 
    self.msg = Label(self, text="Task #1 Done!", bg="green", fg="white")
    self.msg.pack(padx=10, pady=10)


  def show(self,message):
    self.msg.config(text=message)
    self._slideIn()
  
  def _slideIn(self,target_y=0,step=5,delay=10):
    #Slide frame down
    current_y = self.winfo_y()
    if current_y < target_y:
      self.place_configure(y=abs(current_y))
      self.after(delay,self._slideIn,target_y,delay)
  
  def hide(self,delay=10):
    #slde frame up out of view
    current_y = self.winfo_y()
    if current_y > -self.winfo_height():
      self.place_configure(y=-abs(current_y))
      self.after(delay,self.hide,delay)
      
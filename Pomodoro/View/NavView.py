from tkinter import *
class Navbar(Frame):
    def __init__(self,master):
        super().__init__(master, bg="#333", height=50,width=500)
        self.pack(fill='x')

      # Left and Right Sections in NavBar
        leftSection = Frame(
              self, 
              bg="white"
            )
        leftSection.pack(
              side=LEFT,
              padx=10
            )

        RightSection = Frame(
              self,
              bg=self['bg']
            )
        RightSection.pack(
              side=RIGHT, 
              padx=10, 
              pady=5
            )

        settingBtn = Button(
              RightSection, 
              text="Settings"
            )
        
        reportBtn = Button(
              RightSection, 
              text="Report"
            )

        settingBtn.pack(side=LEFT, padx=5)
        reportBtn.pack(side=LEFT, padx=5)
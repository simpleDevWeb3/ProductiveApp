from tkinter import *

class TimerView(Frame):
    def __init__(self, master):
        super().__init__(master, bg="#BA4949")
        self.pack(fill="both", expand=True)

        TimerSection = Frame(self, bg='#c26566', width=500, height=350)
        TimerSection.pack(expand=True)
        TimerSection.pack_propagate(False)

        # Top Section
        _Ttop = Frame(TimerSection, bg=TimerSection['bg'], height=50)
        _Ttop.pack(fill='x', pady=10)
        _Ttop.pack_propagate(False)

        _TbtnContainer = Frame(_Ttop)
        _TbtnContainer.pack(expand=True)
        _TbtnContainer.columnconfigure((0, 1, 2), weight=1)

        # Save buttons as instance variables so you can access them later
        self.pomodoroBtn = Button(_TbtnContainer, text="Pomodoro",
                                  font=("Arial", 12, 'bold'), fg='white',
                                  bg='#E493A2', padx=20, pady=10,
                                  borderwidth=0, highlightthickness=0,
                                 )

        self.shortBreakBtn = Button(_TbtnContainer, text="Short Break",
                                    font=("Arial", 12, 'bold'), fg='white',
                                    bg=TimerSection['bg'], padx=20, pady=10,
                                    borderwidth=0, highlightthickness=0)

        self.longBreakBtn = Button(_TbtnContainer, text="Long Break",
                                   font=("Arial", 12, 'bold'), fg='white',
                                   bg=TimerSection['bg'], padx=20, pady=10,
                                   borderwidth=0, highlightthickness=0)

        self.pomodoroBtn.grid(row=0, column=0)
        self.shortBreakBtn.grid(row=0, column=1)
        self.longBreakBtn.grid(row=0, column=2)

     

        # Center Timer Display
        _Tcenter = Frame(TimerSection, bg=TimerSection['bg'], height=200)
        _Tcenter.pack(fill='x')
        _Tcenter.pack_propagate(False)

        self._lTimerLabel = Label(_Tcenter,
                                  fg="white", bg=TimerSection['bg'],
                                  font=("Arial", 100))
        self._lTimerLabel.pack(expand=True)

        # Bottom Section
        _Tbottom = Frame(TimerSection, bg=TimerSection['bg'], height=120)
        _Tbottom.pack(fill='x', pady=(0, 40))
        _Tbottom.pack_propagate(False)

        self._startBtn = Button(_Tbottom, text='START',
                                font=("Arial", 15, "bold"),
                                fg=TimerSection['bg'], bg='White',
                                padx=40, pady=30)
        self._startBtn.pack(expand=True)


    def renderTimer(self, minutes, seconds):
        time_str = f"{minutes:02}:{seconds:02}"
        self._lTimerLabel.config(text=time_str)
        print(f"[renderTimer] Rendering: { minutes}:{seconds}")

    def toggleStartButtonText(self,isStart):
   
        new_text = "STOP" if isStart  else "START"
        self._startBtn.config(text=new_text)

    def setStartHandler(self, handler):
        self._startBtn.config(command=handler)
        
    
    def setModeHandler(self, handler):
        self.pomodoroBtn.config(command=lambda: handler("Pomodoro"))
        self.shortBreakBtn.config(command=lambda: handler("ShortBreak"))
        self.longBreakBtn.config(command=lambda: handler("LongBreak"))

    def highlightModeButton(self, selected):
        buttons = [self.pomodoroBtn, self.shortBreakBtn, self.longBreakBtn]
        
        for btn in buttons:
            btn.config(bg='#c26566')  # Reset all to default
        selected.config(bg="#E493A2")    # Highlight the clicked one

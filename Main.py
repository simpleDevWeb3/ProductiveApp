from tkinter import Tk, Frame, Button, Label
from Pomodoro.program import PomodoroApp
from DiscussionRoom import testProgram
from Expense.expenses_tracker  import ExpenseApp

class Main(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("500x350")
        self.title("Pomodoro Timer - Main")

        # Center frame
        frame = Frame(self)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title label
        Label(frame, text="Welcome to Productivity Tools", font=("Arial", 16)).pack(pady=20)

        # Pomodoro button
        Button(frame, text="Start Pomodoro", width=20, command=self.open_pomodoro).pack(pady=10)

        # Discussion Room button
        Button(frame, text="Discussion Room", width=20, command=self.open_discussionRoom).pack(pady=10)

        # Expense button
        Button(frame, text="Expense", width=20, command=self.open_expense).pack(pady=10)

        # (Future) You can add more options here
        Button(frame, text="Exit", width=20, command=self.quit).pack(pady=10)

        self.mainloop()
   
    def open_pomodoro(self):
        # Open PomodoroApp in a new window
        PomodoroApp()
      
    def open_expense(self):
        # Open PomodoroApp in a new window
        ExpenseApp()

    def open_discussionRoom(self):
        # Open PomodoroApp in a new window
        testProgram.main()


# Start Application
Main()

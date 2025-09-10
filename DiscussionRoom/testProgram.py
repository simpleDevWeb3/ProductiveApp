from DiscussionRoom.DiscussionRoom import DiscussionRoom
from DiscussionRoom.CyberCenter import CyberCenter
from DiscussionRoom.Library import Library
from DiscussionRoom.Availability import Availability
from DiscussionRoom.BookingHistory import BookingHistory
import datetime
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import json

YEAR = datetime.date.today().year
rooms = []
history = []
GUI_window = False #use to prevent multiple window being created -> window
app = True  #use to prevent duplicated GUI being created -> frame
room_to_display_parameter = []

window = Tk()
window.configure(bg="lightblue")
window.geometry("800x700")
window.resizable(False, True)
window.withdraw()

class discussionRoomGUI:
    def __init__(self):

        self.load_data()

        HomePage()   
        window.mainloop()

        self.write_data()


    def load_data(self):
        try:
            with open("Availability.json", "r") as file:
                dataFromFile = json.load(file)
            
            for data in dataFromFile:
                Availability(data.get("id"), data.get("slots"))
        except Exception as e:
            print("Availability-", e)
            
        try:
            with open("DiscussionRoom.json", "r") as file:
                dataFromFile = json.load(file)

            for data in dataFromFile:
                if data.get("location") == "Cyber Center":
                    rooms.append(CyberCenter(data.get("id"), data.get("name"), data.get("location"), data.get("equipment")))
                elif data.get("location") == "Library":
                    rooms.append(Library(data.get("id"), data.get("name"), data.get("location"), data.get("capacity")))
        except Exception as e:
            print("DiscussionRoom-", e)
            
        try:
            with open("BookingHistory.json", "r") as file:
                dataFromFile = json.load(file)
            
            for data in dataFromFile:
                room = linear_search(data.get("room"), rooms)
                if not room == -1:
                    history.append(BookingHistory(room, data.get("date"), data.get("time"), data.get("bookingDate")))
        except Exception as e:
            print("BookingHistory-", e)
    
    def write_data(self):
        list = []
        with open("BookingHistory.json", "w") as file:
            for h in history:
                list.append(h.json())
            json.dump(list, file, indent=4)

        list = []
        with open("Availability.json", "w") as file:
            for obj in Availability.availability():
                list.append(obj.json())
            json.dump(list, file, indent=4)
        rooms.clear()
        history.clear()

class HomePage:
    def __init__(self):
        self.frame = Frame(window, bg="lightblue")
        self.frame.pack(expand=True)
        self.print_HomePage()

    def print_HomePage(self):
        window.title("Discussion Room Booking")

        btRoomList = Button(self.frame, 
                            text="Room List", 
                            font=("Calibri", 20, "bold"),
                            width=22, height=3, 
                            bg="steelblue",
                            command=self.displayRoomList)
        
        btHistory = Button(self.frame, 
                           text="Booking History",
                            font=("Calibri", 20, "bold"),
                            width=22, height=3, 
                            bg="deep sky blue",
                            command=self.displayHistory)
        
        btExit = Button(self.frame, 
                        text="Exit",                             
                        font=("Calibri", 20, "bold"),
                        width=22, height=3, 
                        bg="red",
                        command=self.exit)

        btRoomList.grid(row=1, column=1, pady=5, padx=15)
        btHistory.grid(row=3, column=1, pady=5, padx=15)
        btExit.grid(row=4, column=1, pady=5, padx=15)

    def displayRoomList(self):
        self.frame.destroy()
        for r in rooms:
            print(r.displayBrief())
        RoomList()

    def displayHistory(self):
        self.frame.destroy()
        for h in history:
            print(h)
        History()

    def exit(self):
        if tkinter.messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            #self.frame.destroy()
            window.withdraw()
            global app, GUI_window
            GUI_window = False
            app = False
     
class RoomList:
    _previousPage = None

    def __init__(self, rooms_to_display = rooms, asc = False):
        if RoomList._previousPage:
            RoomList._previousPage.destroy()

        self.asc = not asc  #use for sorting direction
        self.rooms_to_display = rooms_to_display
        self.frameForDetail = False

        self.print_RoomList()

    def print_RoomList(self):
        window.title("Room List")
        self.frame = Frame(window, bg="lightblue")
        self.frame.pack()

        style = ttk.Style()
        style.configure("Treeview", font=("Calibri", 12), rowheight=30)         # table content
        style.configure("Treeview.Heading", font=("Calibri", 14, "bold"))       # header
        style.map("Treeview", background=[("selected", "#2EA6DE")])

        HEARDER = ("No.", "ID", "Name", "Location", "Available (Slots)")
        self.table = ttk.Treeview(self.frame, columns=HEARDER, show="headings")

        for header in HEARDER:
            self.table.heading(header, text=header, command=lambda c=header: self.on_header_click(c))
        
        self.table.column("No.",       width=50,  anchor="w")   # left align
        self.table.column("ID",        width=100, anchor="center")
        self.table.column("Name",      width=315, anchor="w")       
        self.table.column("Location",  width=150, anchor="w")
        self.table.column("Available (Slots)", width=180, anchor="center")

        self.rooms_record = {}
        for i, room in enumerate(self.rooms_to_display, start=1):
            record_id = self.table.insert("", END, values=(i, *room.displayBriefForGuiTable())) # values -> split(*) and merge with no.
            self.rooms_record[record_id] = room     #assign unique id for each row

        self.table.pack(fill="both", expand=True)
        self.table.bind("<<TreeviewSelect>>", self.viewDetail)  #view detail when room selected

        self.frame2 = Frame(self.frame, bg="lightblue")
        self.frame2.pack()

        btBack = Button(self.frame2, 
                        text="Back", 
                        font=("Calibri", 12),
                        width=10, 
                        command=self.back)
        btBack.grid(row=2, column=4, padx=10, ipadx=10, pady=10)    

        btBook = Button(self.frame2, 
                        text="Book", 
                        font=("Calibri", 12),
                        width=10, 
                        command=self.booking)
        btBook.grid(row=2, column=5, padx=10, ipadx=10, pady=10)

        RoomList._previousPage = self

    def destroy(self):
        self.frame.destroy()

    def back(self):
        self.destroy()
        HomePage()
    
    def extractRoom(self, event):
        selected_row = self.table.focus()
        room = self.rooms_record.get(selected_row)
        print(room)
        return room

    def viewDetail(self, event):
        room = self.extractRoom(event)
        if self.frameForDetail:
            self.frameForDetail.destroy() 
            
        self.frameForDetail = RoomDetail(self.frame, room)

    def booking(self, event = None):
        room = self.extractRoom(event)
        if room:
            if not room.totalSlotsAvailable() == 0:
                if self.frameForDetail:
                    self.frameForDetail.destroy() 
                
                global room_to_display_parameter
                room_to_display_parameter = [self.rooms_to_display, self.asc]
                self.frameForDetail = Booking_Date(self.frame, room)

            else:
                tkinter.messagebox.showerror("Error", "The room is not available.")
        else:         
            tkinter.messagebox.showerror("Error", "Please select a room.")

    def on_header_click(self, column):
        print(f"Header clicked: {column}")
        room_to_display = DiscussionRoom.OrderBy(list.copy(rooms), column, self.asc)
        self.destroy()
        RoomList(room_to_display, self.asc)

class RoomDetail:
    def __init__(self, frame, room):
        self.frame1 = Frame(frame)
        self.frame1.pack(pady=10)
        self.room = room
        self.print_RoomDetail()

    def print_RoomDetail(self):
        Label(self.frame1, 
              text=self.room, 
              font=("Calibri", 16), 
              justify=LEFT
              ).pack(padx=40, pady=20)
        
        Button(self.frame1, 
               bg="grey", 
               text="Close", 
               font=("Calibri", 12), 
               justify=RIGHT, 
               command=self.destroy
               ).pack(ipadx=20, pady=10)

    def destroy(self):
        self.frame1.destroy()

class Booking_Date:
    def __init__(self, frame, room):
        self.room = room
        self.frame = frame
        self.print_BookingDate()

    def print_BookingDate(self):
        self.frame1 = Frame(self.frame, bg="azure")
        self.frame1.pack(pady=10)

        Label(self.frame1,
              bg="azure",
              text="Booking", 
              justify="center", 
              font=("Calibri", 25, "bold")
              ).grid(row=1, 
                     column=1, 
                     columnspan=2, 
                     pady=10)  
        
        Label(self.frame1,
              bg="azure",
              text="Date: ",
              font=("Arail", 12, "bold"),
              ).grid(row=2, column=1, padx=(40, 0), pady=(10, 20))

        # Dropdown options
        dateOptions = []
        for date in self.room.slots.slots.keys():
            i = self.room.totalSlotsAvailable_date(date)
            if not i == 0:
                dateOptions.append(date)
        print(dateOptions)

        # Tkinter variable
        self.selected_date = StringVar(value=dateOptions[0])    #display the first date

        # Change font for listbox (dropdown part of Combobox)
        window.option_add("*TCombobox*Listbox*Font", ("Calibri", 12))

        # Create Combobox
        dropdown = ttk.Combobox(self.frame1, 
                                font=("Arail", 12),
                                textvariable=self.selected_date,
                                values=dateOptions, 
                                state="readonly")
        dropdown.grid(row=2, column=2, padx=(0, 40), pady=(10, 20))

        # Set default value
        dropdown.bind("<<ComboboxSelected>>", self.showTimeAvailable)   #enable real time display time available
        self.showTimeAvailable()
        
    def destroy(self):
        self.frame1.destroy()

    def showTimeAvailable(self, event=None):
        Booking_Time(self.frame1, self.room, self.selected_date.get())

class Booking_Time:
    def __init__(self, frame, room, dateSelected):
        self.room = room
        self.date = dateSelected
        self.frame = frame

        self.print_BookingTime()

    def print_BookingTime(self):
        Label(self.frame, 
              bg="azure",
              text="Time: ",
              font=("Arail", 12, "bold"),
              ).grid(row=3, column=1, padx=(50, 10), pady=(0, 20))

        # Dropdown options
        timeOptions = []
        for time, availability in self.room.slots.slots.get(self.date).items(): #get available time slots
            if availability:
                timeOptions.append(time)
        print(timeOptions)

        # Tkinter variable
        self.selected_time = StringVar()

        # Create Combobox
        dropdown = ttk.Combobox(self.frame, 
                                font=("Arail", 12),
                                textvariable=self.selected_time, 
                                values=timeOptions, 
                                state="readonly")
        dropdown.grid(row=3, column=2, padx=(10, 50), pady=(0, 20))

        # Set default value (optional)
        dropdown.current(0)
        
        Button(self.frame, 
               text="Submit",
               font=("Arail", 12), 
               bg="lightgreen",
               width=10, 
               justify="center", 
               command=self.make_booking
               ).grid(row=4, column=1, columnspan=2, pady=10)
    
    def make_booking(self):
        self.room.updateSlotStatus(self.date, self.selected_time.get())
        history.insert(0, BookingHistory(self.room, self.date, self.selected_time.get(), datetime.date.today().strftime("%d-%m-%Y")))
        tkinter.messagebox.showinfo("Successfully", "Your booking has been successfully made.")
        print(history[0])
        self.frame.destroy()
        global room_to_display_parameter
        self.frameForDetail = RoomList(room_to_display_parameter[0], room_to_display_parameter[1])
        
class History:
    def __init__(self):
        window.title("History")
        self.frameForDetail = False
        self.print_History()
    
    def print_History(self):
        self.frame = Frame(window, bg="lightblue")
        self.frame.pack()

        style = ttk.Style()
        style.configure("Treeview", font=("Calibri", 12), rowheight=30)     # table content style
        style.configure("Treeview.Heading", font=("Calibri", 14, "bold"))   # header style

        HEARDER = ("No.", "Room ID", "Room", "Location", "Date", "Time", "Booking Date")
        self.table = ttk.Treeview(self.frame, columns=HEARDER, show="headings")
        
        for header in HEARDER:
            self.table.heading(header, text=header)

        self.table.column("No.",            width=45,  anchor="w")  # left align
        self.table.column("Room ID",        width=80, anchor="center")
        self.table.column("Room",           width=200, anchor="w")       
        self.table.column("Location",       width=145, anchor="w")
        self.table.column("Date",           width=100, anchor="center")
        self.table.column("Time",           width=100, anchor="center")
        self.table.column("Booking Date",   width=125, anchor="center")

        self.history_record = {}
        for i, h in enumerate(history, start=1):
            record_id = self.table.insert("", END, values=(i, *h.displayBriefForGuiTable())) # values -> split(*) and merge with no.
            self.history_record[record_id] = h     #assign unique id for each row

        self.table.pack()
        self.table.bind("<<TreeviewSelect>>", self.viewDetail)  #view detail when room selected

        Button(self.frame, 
               bg="grey",
               text="Back", 
               font=("Calibri", 12),
               command=self.back
               ).pack(ipadx=30, pady=10)

    def back(self):
        self.frame.destroy()
        HomePage()

    def extractHistory(self, event):
        selected_row = self.table.focus()
        h = self.history_record.get(selected_row)
        print(h)
        return h

    def viewDetail(self, event):
        h = self.extractHistory(event)
        if self.frameForDetail:
            self.frameForDetail.destroy() 
            
        self.frameForDetail = RoomDetail(self.frame, h.room)

def linear_search(target, list):
    for value in list:
        if target == value:
            return value
    return -1

def exit():
    if tkinter.messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        window.withdraw()
        global GUI_window, app
        GUI_window = False
        app = False

def main():
    window.protocol("WM_DELETE_WINDOW", exit)   #custom exit event
    global GUI_window

    if not GUI_window:
        GUI_window = not GUI_window

        window.deiconify()
        if app:
            discussionRoomGUI()

        print("The program is end.")

from DiscussionRoom.CyberCenter import CyberCenter
from DiscussionRoom.Library import Library
from DiscussionRoom.Availability import Availability
#from Student import Student
from DiscussionRoom.BookingHistory import BookingHistory
import datetime
from tkinter import *
from tkinter import ttk
import tkinter.simpledialog
import tkinter.messagebox
import json

YEAR = datetime.date.today().year
rooms = []
history = []

window = Tk()
window.configure(bg="lightblue")
window.geometry("800x700")
window.resizable(False, True)
window.withdraw()

class discussionRoomGUI:
    def __init__(self):
        HomePage()        
        window.mainloop()

class HomePage:
    def __init__(self):
        window.title("Discussion Room Booking")

        self.frame = Frame(window, bg="lightblue")
        self.frame.pack(expand=True)

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
                            command=self.displayHistory)
        
        btExit = Button(self.frame, 
                        text="Exit",                             
                        font=("Calibri", 20, "bold"),
                        width=22, height=3, 
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
            window.destroy()
     
class RoomList:
    _previousPage = None

    def __init__(self):
        if RoomList._previousPage:
            RoomList._previousPage.destroy()

        window.title("Room List")
        self.frameForDetail = False

        self.frame = Frame(window, bg="lightblue")
        self.frame.pack()

        """***************************************************************TABLE"""
        style = ttk.Style()
        style.configure("Treeview", font=("Calibri", 12), rowheight=30)          # table content
        style.configure("Treeview.Heading", font=("Calibri", 14, "bold"))  # header

        HEARDER = ("No.", "ID", "Name", "Location", "Available (Slots)")
        self.table = ttk.Treeview(self.frame, columns=HEARDER, show="headings")

        for header in HEARDER:
            self.table.heading(header, text=header)
        
        self.table.column("No.",       width=50,  anchor="w")   # left align
        self.table.column("ID",        width=100, anchor="center")
        self.table.column("Name",      width=315, anchor="w")       
        self.table.column("Location",  width=150, anchor="w")
        self.table.column("Available (Slots)", width=180, anchor="center")

        self.rooms_record = {}
        for i, room in enumerate(rooms, start=1):
            record_id = self.table.insert("", END, values=(i, *room.displayBriefForGuiTable())) # values -> split(*) and merge with no.
            self.rooms_record[record_id] = room     #assign unique id for each row

        self.table.pack(fill="both", expand=True)
        self.table.bind("<<TreeviewSelect>>", self.viewDetail)  #view detail when room selected

        """***************************************************************"""
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
                
                self.frameForDetail = Booking_Date(self.frame, room)

            else:
                tkinter.messagebox.showerror("Error", "The room is not available.")
        else:         
            tkinter.messagebox.showerror("Error", "Please select a room.")

class RoomDetail:
    def __init__(self, frame, room):
        self.frame1 = Frame(frame)
        self.frame1.pack(pady=10)

        Label(self.frame1, text=room, font=("Calibri", 12), justify=LEFT).pack(padx=10, pady=10)
        btn = Button(self.frame1, bg="grey", text="Close", font=("Calibri", 12), justify=RIGHT, command=self.destroy)
        btn.pack(ipadx=20, pady=10)

    def destroy(self):
        self.frame1.destroy()

class Booking_Date:
    def __init__(self, frame, room):
        self.frame1 = Frame(frame, bg="azure")
        self.frame1.pack(pady=10)

        self.room = room
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
        for date in room.slots.slots.keys():
            i = room.totalSlotsAvailable_date(date)
            if not i == 0:
                dateOptions.append(date)
        print(dateOptions)

        # Tkinter variable
        self.selected_date = StringVar(value=dateOptions[0])

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
        Label(frame, 
              bg="azure",
              text="Time: ",
              font=("Arail", 12, "bold"),
              ).grid(row=3, column=1, padx=(50, 10), pady=(0, 20))

        # Dropdown options
        timeOptions = []
        for time, availability in room.slots.slots.get(dateSelected).items(): #get available time slots
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
               command=self.show_selection
               ).grid(row=4, column=1, columnspan=2, pady=10)
    
    def show_selection(self):
        self.room.updateSlotStatus(self.date, self.selected_time.get())
        history.insert(0, BookingHistory(self.room, self.date, self.selected_time.get(), datetime.date.today().strftime("%d-%m-%Y")))
        tkinter.messagebox.showinfo("Successfully", "Your booking has been successfully made.")
        print(history[0])
        self.frame.destroy()
        RoomList()
        
class History:
    def __init__(self):
        self.frame = Frame(window, bg="white")
        self.frame.pack()

        """***************************************************************TABLE"""
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

        for i, h in enumerate(history, start=1):
            self.table.insert("", END, values=(i, *h.displayBriefForGuiTable()))

        self.table.pack()

        Button(self.frame, 
               bg="grey",
               text="Back", 
               font=("Calibri", 12),
               command=self.back
               ).pack(ipadx=30, pady=10)

    def back(self):
        self.frame.destroy()
        HomePage()

def linear_search(target, list):
    for value in list:
        if target == value:
            return value
    return -1

def d(x = "--------"):
    print(f"------------------{x}-------------------")

def menuMsg(*args):
    d(f"{args[0]}")

    for x in range(1, len(args)):
        print(f"{args[x]}")

def strInputValidation(msg):
    while True:
        value = input(msg)

        if value.isalpha():
            return value
        else:
            print("Only alphbetic characters is allowed")

def intInputValidation(min, max, msg):
    while True:
        try:
            value = int(input(msg))
            if min <= int(value) <= max:
                return int(value)
            elif int(value) > max or int(value) < min:
                print(f"Please enter number between {min} and {max}")

        except ValueError:
            print("Please enter number.")

def idInputValidation(msg):
    value = input(msg)

    while True:
        if value[:3].isalpha() and value[3:].isdigit() and len(value) == 7:
            return value
        elif len(value) != 7:
            print("The maximum length of id is 7 characters.")
        else:
            print("Please follow the ID format, XXX1234.")

        value = input(msg)

def dateInputValidation():
    while True:
        try:
            m = intInputValidation(1, 12, "Month: ")
            d = intInputValidation(1, 31, "Day: ")
            date = datetime.date(YEAR, m, d)
            return date.strftime("%d-%m-%Y")
        except ValueError:
            print(f"{d}-{m}-{YEAR} is not a valid date.")

def timeInputValidation():
    h = intInputValidation(8, 17, "Hour: ")
    m = intInputValidation(0, 59, "Minustes: ")
    return datetime.time(h, m)

def viewDetails(room):
    while True:
        d("Room Details")
        print(room)

        menuMsg("",  "1 Book", "0 Back")
        choice = intInputValidation(0, 1, "Enter no. :")
        match choice:
            case 1:
                if room.status == False:
                    print("The room is unavailable")
                else:
                    bookingRoom(room)
                break
            case 0:
                break
                            
def viewRoom():
    back = False
    while not back:
        d("Room List")
        print(f"{'No.':<5s}{'ID':<10s}{'Name':<20s}{'Location':<20s}")

        for x in range(len(rooms)):
            print(f"{x + 1:<5d}{rooms[x].displayBrief()}")

        menuMsg("", f"\n1 - {len(rooms)} View details", "0 Back")
        choice = intInputValidation(0, len(rooms), "Enter no. :")
        match choice:
            case 0:
                back = True
            case _:
                viewDetails(rooms[choice - 1])

def bookingRoom(room):
    menuMsg("Booking", "Please enter the date:- ")
    date = dateInputValidation()
    while True:
        print("From Time: ")
        fromTime = timeInputValidation()
        print("To Time: ")
        toTime = timeInputValidation()
        time1 = datetime.datetime.combine(datetime.date.today(), fromTime)
        time2 = datetime.datetime.combine(datetime.date.today(), toTime)

        if (time2 - time1).total_seconds() / 60 <= 30:
            print("The minimum booking duration is 30 minutes")
        elif (time2 - time1).total_seconds() / 60 >= 120:
            print("The maximum booking duration is 2 hours")
        else:
            break 

    room.status = False
    history.append(BookingHistory(room, date, fromTime, toTime))

def returnKey():
    d("Return Room's Key'")
    print("Please enter the Room ID you want to return.")
    roomID = input("Room ID: ")

    roomIdFound = False
    for h in history:
        if h.room == roomID:
            print("Return successfully.")
            h.room.status = True
            roomIdFound = True
    
    if roomIdFound == False:
        print("Ambigious room ID entered.")

    roomIdFound = False

def bookingHistory():
    menuMsg("Booking History")
    for h in history:
        print("Stud ID.\tRoom ID.\tRoom Name\tLocation\tDate\tTime")
        print(h)

def main():

    while True:
        menuMsg("Home Pge", "1. Room List", "2. Return Room's Key", "3. Booking History", "0. Exit")
        choice = intInputValidation(0, 3, "Enter no. :")
        
        match choice:
            case 1:
                viewRoom()
            case 2:
                returnKey()
            case 3:
                bookingHistory()
            case 0:
                break

def main():
    #if __name__ == "__main__":
    if True:
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

        window.deiconify()
        discussionRoomGUI()

        list = []
        with open("BookingHistory.json", "w") as file:
            for h in history:
                list.append(h.json())
            json.dump(list, file, indent=4)

        list = []
        with open("DiscussionRoom.json", "w") as file:
            for room in rooms:
                list.append(room.json())
            json.dump(list, file, indent=4)
        
        list = []
        with open("Availability.json", "w") as file:
            for obj in Availability.availability():
                list.append(obj.json())
            json.dump(list, file, indent=4)
            

        #main()


import datetime
import json

class BookingHistory:
    def __init__(self, room, date, time, bookingDate):
        self._room = room
        self._date = date
        self._time = time
        self._bookingDate = bookingDate

    @property
    def room(self):
        return self._room

    @property
    def date(self):
        return self._date

    @property
    def time(self):
        return self._time

    @property
    def bookinfDate(self):
        return self._bookingDate
    
    def __str__(self):
        return f"{self._room.displayBrief()}\t{self._date}\t{self._time}\t{self._bookingDate}"
    
    def displayBriefForGuiTable(self):
        return (*self._room.commonAttribute(), self._date, self._time, self._bookingDate)
    
    def json(self):
        return {"room": self._room.ID, "date": self._date, "time": self._time, "bookingDate": self._bookingDate}



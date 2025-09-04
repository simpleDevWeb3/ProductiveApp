from DiscussionRoom.Availability import Availability

class DiscussionRoom:
    _totalRoom = 0

    def __init__(self, ID, name, location):
        self._ID = ID
        self._name = name
        self._location = location
        self._slots = Availability.Get(self._ID)
        DiscussionRoom._totalRoom += 1

    @property
    def ID (self):
        return self._ID

    @property
    def name (self):
        return self._name

    @property
    def location(self):
        return self._location
    
    @property
    def slots(self):
        return self._slots
    
    @name.setter
    def name (self, name):
        self._name = name

    @location.setter
    def location (self, location):
        self._location = location

    def __eq__(self, value):
        return self._ID == value

    def __str__ (self):
        return f"ID\t\t: {self._ID}\nName\t\t: {self._name}\nRoom location\t: {self._location}\n"

    def updateSlotStatus(self, date, time):
        self._slots.toggle_availability(date, time)
    
    def totalSlotsAvailable(self):
        return self._slots.totalSlotsAvailable()

    def totalSlotsAvailable_date(self, date):
        return self._slots.totalSlotsAvailable_date(date)

    def displayBrief(self):
        return f"{self._ID:<10s}{self._name:<30s}{self._location:<5s}"
    
    def displayBriefForGuiTable (self):
        return (self._ID, self.name, self.location, f"{self.totalSlotsAvailable()}" if not self.totalSlotsAvailable() == 0 else "Unavailable")

    def commonAttribute (self):
        return (self._ID, self.name, self.location)
    
    def json(self):
        return {"id": self._ID, "name": self._name, "location": self._location}

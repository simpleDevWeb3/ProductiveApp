import datetime

class Availability:
    _availability = {}   #all availability
    _TIME_SLOT = ["9:00-11:00", "11:00-13:00", "13:00-1500", "15:00-17:00"]

    def __init__(self, id, availability):
        self._id = id
        self._slots = {}
        date_keys = list(availability.keys())   #get all keys(dates)
        last_date = datetime.datetime.strptime(date_keys[-1], "%d-%m-%Y").date()    #convert the last date from string into date

        for i in range(1, 4):
            date = datetime.date.today() + datetime.timedelta(days=i)
            
            if date <= last_date:
                date = date.strftime("%d-%m-%Y")
                self._slots[date] = dict(zip(Availability._TIME_SLOT, availability.get(date)))  #load availability
            else:
                self._slots[date.strftime("%d-%m-%Y")] = dict(zip(Availability._TIME_SLOT, [True, True, True, True]))   #new availability

        if Availability._availability.get(self._id):
            Availability._availability.pop(self._id)    #remove the previous availability

        Availability._availability[self._id] = self     #add the up to date availability

    @classmethod
    def availability(cls):
        return cls._availability.values()
    
    @property
    def id(self):
        return self._id
    
    @property
    def slots(self):
        return self._slots
    
    def __str__(self):
        return f"{self._id}\t{self._slots}"

    def __eq__(self, id):
        return self._id == id

    def toggle_availability(self, date, time):
        status = self._slots.get(date).get(time)
        self._slots.get(date).update({time: not status })

    def totalSlotsAvailable(self):
        i = 0
        for date in self._slots.values():
            for time in date.values():
                if time:
                    i += 1
        return i
    
    #all or any
    def totalSlotsAvailable_date(self, date):
        i = 0
        for time in self._slots.get(date).values():
            if time:
                i += 1
        return i

    def json(self):
        list = {}
        for date, time in self._slots.items():
            listTime = []
            for available in time.values():
                listTime.append(available)
            list[date] = listTime
        return {"id": self._id, "slots": list}

    @classmethod
    def Get(cls, id):
        for obj in cls._availability.values():
            if obj == id:
                return obj
            
    """
    @classmethod
    def Last(cls, id):
        dates = cls._availability.get(id)
        if dates is not None:
            keys = dates.slots.keys()
            return datetime.strptime(keys[-1], "%d-%m-%Y")
        else:
            return datetime.date.today() 
    """
    """
    @classmethod
    def Find(cls, id, date):
        for room_id, slots in cls._availability:
            if room_id == id:
                return slots._slots.get(date)
    """
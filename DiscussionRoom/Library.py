from DiscussionRoom.DiscussionRoom import DiscussionRoom

class Library(DiscussionRoom):
    def __init__(self, ID, name, location, capacity):
        super().__init__(ID, name, location)
        self._capacity = capacity

    @property
    def capacity (self):
        return self._capacity
    
    @capacity.setter
    def capacity (self, capacity):
        self._capacity = capacity
    
    def __str__ (self):
        return super().__str__() + f"Capacity\t\t: {self._capacity}"
    
    def json(self):
        json = super().json()
        json["capacity"] = self._capacity
        return json
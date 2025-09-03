from DiscussionRoom.DiscussionRoom import DiscussionRoom

class CyberCenter(DiscussionRoom):
    def __init__(self, ID, name, location, equipment):
        super().__init__(ID, name, location)
        self._equipment = equipment

    @property
    def equipment (self):
        return self._equipment
    
    @equipment.setter
    def equipment (self, equipment):
        self._equipment = equipment
    
    def __str__ (self):
        return super().__str__() + f"Equipment : {self._equipment}"
    
    def json(self):
        json = super().json()
        json["equipment"] = self._equipment
        return json
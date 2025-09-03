class Student:
    def __init__(self, studId, studName):
        self._studId = studId
        self._studName = studName

    @property
    def studId(self):
        return self._studId
    
    @property
    def studName(self):
        return self._studName
    
    @studName.setter
    def studName(self, studName):
        self._studName = studName

    def __eq__(self, value):
        return self._studId == value
    
    def __str__(self):
        return f"Student ID: {self._studName}\nStudent Name: {self._studName}\n"
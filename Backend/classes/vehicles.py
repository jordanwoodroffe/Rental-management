from abc import ABC, abstractmethod

class Vehicle (ABC):
   
    @abstractmethod
    def __init__(self, id, make, model, year, rentStatus):
        self.id = id
        self.make = make
        self.model = model
        self.year = year
        self.rentStatus = rentStatus
        
    #Gets
    def getMake(self):
        return self.make
    
    def getModel(self):
        return self.model
    
    def getYear(self): 
        return self.year

    def getRentStatus(self):
        return self.year
    
    def getID(self):
        return self.id

    #Sets
    def setMake(self, make):
        self.make = make
    
    def setModel(self, model):
        self.model = model
    
    def setYear(self, year): 
        self.year = year

    def setRentStatus(self, status):
        self.year = status
    
    #Actions
    @abstractmethod
    def rent(self):
        #to be completed
        pass

    @abstractmethod
    def addRecord(self, record):
        pass


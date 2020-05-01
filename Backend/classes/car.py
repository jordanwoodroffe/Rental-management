from abc import ABC, abstractmethod
from rentalRecord import RentalRecords
from vehicles import Vehicle
from datetime import date

class Car (Vehicle):

    def __init__(self, id, make, model, year, rentStatus):
        super().__init__(make, model, year, rentStatus, id)
        #this holds rentalRecord objects, rental history
        self.rentalRecords = list()

    #takes customer object in parathesis, return true if successful
    def rentCar(self, rate, customer):
        time = date.today()
        if self.getRentStatus == False:
            #create rentalRecord for car
            self.addRecord(RentalRecords(customer.getID, self.getID, time, None, rate))
            #create rentalRecords for user
            customer.addRecord(RentalRecords(customer.getID, self.getID, time, None, rate))
            #change rent status
            self.setRentStatus = True
            return True
        else:
            return False

    def returnCar(self, rate, customer):
        time = date.today()
        if self.getRentStatus == True:
            #update rentalRecord for car
            self.rentalRecords[-1].setReturn(time)
            #update rentalRecords for user
            customer.rentalRecords[-1].setReturn(time)
            #change rent status
            self.setRentStatus = False
            return True
        else:
            return False

    def addRecord(self, record):
        self.rentalRecords.append(record)


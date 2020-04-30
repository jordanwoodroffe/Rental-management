class RentalRecords ():

    def __init__(self, customer_id, vehicle_id, rentDate, returnDate, rate):
        self.customer_id = customer_id
        self.vehicle_id = vehicle_id
        self.rentDate = rentDate
        self.returnDate = returnDate
        self.DailyRate = rate
        

     #this holds rentalRecord objects
        self.rentalRecords = list()

    #Gets
    def getCustomerId(self):
        return self.customer_id
    
    def getVehicleId(self):
        return self.vehicle_id

    def getRentDate(self):
        return self.rentDate

    def getRate(self):
        return self.DailyRate

    def getDays(self):
        return self.numOfDays

    #Sets
    def setCustomerId(self, id):
        self.customer_id = id
    
    def setVehicleId(self, id):
        self.vehicle_id = id

    def setRentDate(self, date):
        self.rentDate = date

    def setRate(self, rate):
        self.DailyRate = rate

    def setReturn(self, returnDate):
        self.returnDate = returnDate

    def setDays(self, days):
        self.numOfDays = days
    
    
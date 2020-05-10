class Customer ():

    def __init__(self, firstName, lastName, id):
        self.firstName = firstName
        self.lastName = lastName
        self.id = id
        #this is a list rentalRecord Objects
        self.rentalRecords = list()

    #Gets
    def getFirstName(self):
        return self.firstName
    
    def getLastName(self):
        return self.lastName

    def getID(self):
        return self.id
    
    #Sets
    def setFirstName(self, firstName):
        self.firstName = firstName
    
    def setLastName(self, lastName):
        self.lastName = lastName

    def setID(self, id):
        self.id = id

    #Action
    def addRecord(self, record):
        self.rentalRecords.append(record)

    

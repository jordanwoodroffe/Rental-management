from classes.vehicles import Vehicle
from classes.car import Car
from classes.customer import Customer
from classes.rentalRecord import RentalRecords

def main():

    #test car object
    car1 = Car (342523, "ford", "fiesta", 2010, False)
    #test customer object
    customer1 = Customer ("Jordan", "Woodroffe", 234242)
    #test rent status
    if (car1.getRentStatus == False): 
        car1.rentCar(3.00, customer1)
        print (customer1.rentalRecords)
        
if __name__ == "__main__": main()
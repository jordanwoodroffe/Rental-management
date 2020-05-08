import socket


#Clientside Setup
serverAddressPort   = ("localhost", 20001)
bufferSize          = 1024
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Login
print ("Enter Username")
username = input()
print ("Enter Password")
password = input()
print ("Logging in...")
loginDetails = "_login" + "_user_" + username + "_pass_" + password
# Encode and send login details
loginBytes = str.encode(loginDetails)
UDPClientSocket.sendto(loginBytes, serverAddressPort)
#Recieve login response, response either successful or not
msgFromServer = UDPClientSocket.recvfrom(bufferSize)
response = msgFromServer[0]

if response == b'successful':
    print ("login success")
    
    while (True):

        def rentCar():
            print("enter car id")
            id = "_rentCar" + input()
            #conditions are met on server side (car id exists && is not currently rented)
            carRequestBytes = str.encode(id)
            UDPClientSocket.sendto(carRequestBytes, serverAddressPort)
            #recieve message
            msgFromServer = UDPClientSocket.recvfrom(bufferSize)
            rentResponse = msgFromServer[0]
                
            if (rentResponse == b'successful'):
                print ("car rented succesfully")
                return
            else:
                print ("car is currently rented or car ID is invalid")
                return
                
        def returnCar():
            print("enter car id")
            id = "_returnCar" + input()
            #conditions are met on server side (car id exists && is currently rented)
            carRequestBytes = str.encode(id)
            UDPClientSocket.sendto(carRequestBytes, serverAddressPort)
            #recieve message
            msgFromServer = UDPClientSocket.recvfrom(bufferSize)
            returnResponse = msgFromServer[0]
                
            if (returnResponse == b'successful'):
                print ("car returned succesfully")
                return
            else:
                print ("car is not currently rented or car ID is invalid")
                return
        
        def controller():
            #Menu Controller        
            options = {
                "1: Rent a Car": "",
                "2: Return a Car":"",
                "3: Exit": ""
            }
            for x in options: 
                print (x)
              
            print ("select an option") 
            selectedOption = input()
            if (selectedOption == "1"):
                rentCar()
                return
            elif (selectedOption == "2"):
                returnCar()
                return
            else:
                print("invalid choice")
                return
          
        controller()
else:
    print("incorrect login details")
    
print ("Logged out")
    
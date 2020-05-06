import socket

localIP     = "localhost"
localPort   = 20001
bufferSize  = 1024

#Initalize server
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")


def rentCar(details):
    idCar = details[8,0]
    #***Check with DB***
    #Check db if id exists
    #Check db if currently rented
    #Update object in db
    #Send response 'successful' to client
    msgFromServer       = "successful"
    bytesToSend         = str.encode(msgFromServer)
    UDPServerSocket.sendto(bytesToSend, address)
    return
    
def returnCar(details):
   #***Check with DB***
    #Check db if id exists
    #Check db if currently rented
    #Update object in db
    #Send response 'successful' to client
    msgFromServer       = "successful"
    bytesToSend         = str.encode(msgFromServer)
    UDPServerSocket.sendto(bytesToSend, address)
    return
    
#will be fixed soon, needs to convert encoded details into a string
def login(details):
    #***Check with DB***
    #Check db if user exists
    #Send response 'successful' to client
    msgFromServer       = "successful"
    bytesToSend         = str.encode(msgFromServer)
    UDPServerSocket.sendto(bytesToSend, address)
    return

#Incoming datagrams
while(True):

    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    clientMsg = "Message from Client:{}".format(message)
    clientIP  = "Client IP Address:{}".format(address)
    
    #Debugging
    print (clientMsg)
    
    #Translate response into a method
    while(True):
        if ("_rentCar" in clientMsg):
            rentCar(clientMsg)
            break
       
            
        if ("_login" in clientMsg):
            login(clientMsg)
            break
        
        if ("_returnCar" in clientMsg):
            returnCar(clientMsg)
            break
      
    

    
    
    
    
   



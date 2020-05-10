import socket
import datetime

localIP     = "localhost"
localPort   = 20001
bufferSize  = 1024

#Initalize server
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")


def rentCar(input):
    idCar = input [30:-1]
    date = datetime.now()
    if('''Check db if id exists'''): 
        if(''''Check db if currently rented'''):
            '''Update object status with datetime in db''''
            #msgFromServer       = "successful"
            #bytesToSend         = str.encode(msgFromServer)
            #UDPServerSocket.sendto(bytesToSend, address)
    
    else:
        #msgFromServer       = "unsuccessful"
        #bytesToSend         = str.encode(msgFromServer)
        #UDPServerSocket.sendto(bytesToSend, address)
    return
    
def returnCar(input):
    idCar = input [32:-1]
    date = datetime.now()
    if('''Check db if id exists'''): 
        if(''''Check db if currently rented'''):
            '''Update object status with datetime in db''''
            #msgFromServer       = "successful"
            #bytesToSend         = str.encode(msgFromServer)
            #UDPServerSocket.sendto(bytesToSend, address)
    
    else:
        #msgFromServer       = "unsuccessful"
        #bytesToSend         = str.encode(msgFromServer)
        #UDPServerSocket.sendto(bytesToSend, address)
    return
    
def login(input):
    userIndex = input.find('_user_')
    passIndex = input.find ('_pass_')
    username = input [userIndex + 6:passIndex]
    password = input [passIndex + 6:-1]
    
    if('''Check db if username/ password exists in DB'''): 
        #msgFromServer       = "successful"
        #bytesToSend         = str.encode(msgFromServer)
        #UDPServerSocket.sendto(bytesToSend, address)
    
    else:
        #msgFromServer       = "unsuccessful"
        #bytesToSend         = str.encode(msgFromServer)
        #UDPServerSocket.sendto(bytesToSend, address)
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
      
    

    
    
    
    
   



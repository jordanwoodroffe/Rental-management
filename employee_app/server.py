import socket
import datetime
import json, requests
from flask import Flask, render_template, request, redirect, Response
from datetime import datetime

app = Flask(__name__)
localIP     = "localhost"
localPort   = 20001
bufferSize  = 1024
URL = "http://193.116.105.6:1000" 

#Initalize server
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))
global message
global address
message = None
address = None
print("UDP server up and listening")

""" Incoming Datagram reciever
The monitors the messages recieved and performs the server options according to
the message. It will decode them and run the method related to the message.
"""
#Incoming datagrams
def incomingFeed():    
 
    while(True):

        global message
        global address
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        clientMsg = "Message from Client:{}".format(message)
        clientIP  = "Client IP Address:{}".format(address)
                
        #Translate response into a method
        while(True):
            if ("_unloCar" in clientMsg):
                unlockCar(clientMsg)
                break
           
            if ("_lockedCar" in clientMsg):
                lockCar(clientMsg)
                break

""" unlocks car
:return (bool) returns true if the car was successfully unlocked using the 
parameters given to it via the client application.
"""

#Sets cars locked status to unlocked
def unlockCar(input):
    global message
    global address
    userIndex = input.find('_user_')
    idCarIndex = input.find('_unloCar')
    email = input [userIndex + 6:-1]
    idCar = input [idCarIndex + 8:userIndex]
    
    print(idCar)
    print(email)

    result = requests.put("{}{}".format(URL, "/engineer/unlock_car"),params={"car_id": idCar, "engineer_id": email})    
        
    if result.status_code == 200:
        msgFromServer       = "successful"
        bytesToSend         = str.encode(msgFromServer)
        if address is not None: ## Allows us to unittest, this will be set usually.
            UDPServerSocket.sendto(bytesToSend, address)
        return True
        
    else:
        msgFromServer       = "unsuccessful"
        bytesToSend         = str.encode(msgFromServer)
        if address is not None: ## Allows us to unittest, this will be set usually.
            UDPServerSocket.sendto(bytesToSend, address)
        return False
    return

""" locks car
:return (bool) returns true if the car was successfully locked using the 
parameters given to it via the client application.
"""

#Sets cars locked status to locked
def lockCar(input):
    global message
    global address
    userIndex = input.find('_user_')
    email = input [userIndex + 6:-1]
    idCar = input [32:userIndex]
                                                                                                                                    
    result = requests.put("{}{}".format(URL, "/engineer/unlock_car"),params={"car_id": idCar, "engineer_id": email})    

    if result.status_code == 200:
        msgFromServer       = "successful"
        bytesToSend         = str.encode(msgFromServer)
        if address is not None: ## Allows us to unittest, this will be set usually.
            UDPServerSocket.sendto(bytesToSend, address)
        return True
        
    else:
        msgFromServer       = "unsuccessful"
        bytesToSend         = str.encode(msgFromServer)
        if address is not None: ## Allows us to unittest, this will be set usually.
            UDPServerSocket.sendto(bytesToSend, address)
        return False
    return

""" main method
runs the incomingFeed loop method when the server.py file is ran
so the server can recieve messages.
"""

def main():
    incomingFeed()
    
if __name__ == '__main__':
    incomingFeed()
  


      
    
   
   
   
  
    
    
   



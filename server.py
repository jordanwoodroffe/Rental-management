import socket
import datetime
import json, requests
import threading
from flask import Flask, render_template, request, redirect, Response
app = Flask(__name__)
localIP     = "localhost"
localPort   = 20001
bufferSize  = 1024
URL = "http://127.0.0.1:5000/" 

#Initalize server
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")
    
#Incoming datagrams
def incomingFeed():

    def unlockCar(input):
        userIndex = input.find('_user_')
        passIndex = input.find ('_pass_')
        email = input [userIndex + 6:passIndex]
        idCar = input [30:userIndex]
        result = requests.get("{}{}".format(URL, "car"),params={"car_id": idCar})    
        data = result.json()
        
        #if data['code'] == 'SUCCESS':
            #msgFromServer       = "successful"
            #bytesToSend         = str.encode(msgFromServer)
            #UDPServerSocket.sendto(bytesToSend, address)
           
            #if(''''Check db if currently rented'''):
                #'''Update object status with datetime in db''''
                #msgFromServer       = "successful"
                #bytesToSend         = str.encode(msgFromServer)
                #UDPServerSocket.sendto(bytesToSend, address)
        
        #else:
            #msgFromServer       = "unsuccessful"
            #bytesToSend         = str.encode(msgFromServer)
            #UDPServerSocket.sendto(bytesToSend, address)
        return
    
   
    def returnCar(input):
        userIndex = input.find('_user_')
        passIndex = input.find ('_pass_')
        email = input [userIndex + 6:passIndex]
        idCar = input [32:userIndex]
        
        #if('''Check db if id exists'''): 
            #if(''''Check db if currently rented'''):
                #'''Update object status with datetime in db''''
                #msgFromServer       = "successful"
                #bytesToSend         = str.encode(msgFromServer)
                #UDPServerSocket.sendto(bytesToSend, address)
        
        #else:
            #msgFromServer       = "unsuccessful"
            #bytesToSend         = str.encode(msgFromServer)
            #UDPServerSocket.sendto(bytesToSend, address)
        return
    
    def login(input):
        userIndex = input.find('_user_')
        passIndex = input.find ('_pass_')
        username = input [userIndex + 6:passIndex]
        password = input [passIndex + 6:-1]
        idCar = input [30:-1]
        result = requests.get("{}{}".format(URL, "users/authenticate"),params={"user_id": username, "password": password})    
        data = result.json()
        
        if data['code'] == 'SUCCESS':
            msgFromServer       = "successful"
            bytesToSend         = str.encode(msgFromServer)
            UDPServerSocket.sendto(bytesToSend, address)
        
        else:
            msgFromServer       = "unsuccessful"
            bytesToSend         = str.encode(msgFromServer)
            UDPServerSocket.sendto(bytesToSend, address)
        return

    def getLocation(input):
        latitudeIndex = input.find('_location')
        longitudeIndex = input.find(',')
        latitude = input [latitudeIndex + 9:longitudeIndex]
        longitude = input [longitudeIndex + 1: -1]
        print (latitude)
        print (longitude)
        return

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
                unlockCar(clientMsg)
                break
           
            if ("_login" in clientMsg):
                login(clientMsg)
                break
            
            if ("_returnCar" in clientMsg):
                returnCar(clientMsg)
                break
            
            if ("_location" in clientMsg):
                getLocation(clientMsg)
                break  
    

@app.route('/')
def index(): 
    points = [{"car_id": "s123", "model_id": 123, "model": "test", "name": "ford", "cph": 49000, "locked": 0, "lng": 144.3690243, "lat": -37.8934276},
             {"car_id": "s123", "model_id": 123, "model": "test", "name": "hyundai", "cph": 40000, "locked": 0, "lng": 145.3690243, "lat": -37.8934276},
             {"car_id": "s123", "model_id": 123, "model": "test", "name": "holden", "cph": 38000, "locked": 0, "lng": 146.3690243, "lat": -37.8934276}] 
    return render_template('index.html', points=json.dumps(points))
                
if __name__ == '__main__':
    t1 = threading.Thread(target=incomingFeed, args=()) 
    t2 = threading.Thread(target=app.run, args=())
    t1.start()
    t2.start()
    t1.join()
    t2.join()
      
    
    
   
   
   
  
    
    
   



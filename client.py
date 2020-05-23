import socket
import FacialRecognition
import pickle
import json, requests
import time
import threading
import sys

car_id = "VSB296" 

#Clientside Setup
serverAddressPort   = ("localhost", 20001)
bufferSize          = 1024
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

def locationTimer():
    while True:
        time.sleep(10)
        info = requests.get('http://ipinfo.io/json').json()
        location = "_location" + info['loc'] + "_id" + car_id
        locationBytes = str.encode(location)
        UDPClientSocket.sendto(locationBytes, serverAddressPort)
  
def interface():
    # Login
    print ("Enter Username")
    username = input()
    print ("Type 1 if you are login via password. Type 2 if logging in via face unlock.")
    option = input()
    if (option == "1"):
        print ("Enter Password")
        password = input()
        print ("Logging in...")
        loginDetails = "_login" + "_user_" + username + "_pass_" + password
        loginBytes = str.encode(loginDetails)

    elif (option == "2"):

        detector = FacialRecognition.FaceDetector()
        login = detector.capture_user(images=["face.jpg"], min_faces=1)
        # encoded
        temp = pickle.dumps(login)
        # file = temp.decode("utf-8")
        # str(file, 'utf-8')

        print("Logging in...")
        loginBytes = temp

    # Encode and send login details
    UDPClientSocket.sendto(loginBytes, serverAddressPort)
    # Recieve login response, response either successful or not
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    response = msgFromServer[0]

    if response == b'successful':
        print("login success")
        
        while (True):

            def unlockCar():
        
                id = "_rentCar" + car_id + "_user_" + username + "_pass_" + password
                #send message to server    
                carRequestBytes = str.encode(id)
                UDPClientSocket.sendto(carRequestBytes, serverAddressPort)
                #recieve message
                msgFromServer = UDPClientSocket.recvfrom(bufferSize)
                rentResponse = msgFromServer[0]
                    
                if (rentResponse == b'successful'):
                    print ("car unlocked successfully")
                    return
                else:
                    print ("car is currently rented")
                    return
                    
            def returnCar():
        
                id = "_returnCar" + car_id + "_user_" + username + "_pass_" + password
                #send message to server
                carRequestBytes = str.encode(id)
                UDPClientSocket.sendto(carRequestBytes, serverAddressPort)
                #recieve message
                msgFromServer = UDPClientSocket.recvfrom(bufferSize)
                returnResponse = msgFromServer[0]
                    
                if (returnResponse == b'successful'):
                    print ("car returned successfully")
                    return
                else:
                    print ("car is not currently rented")
                    return
            
            def controller():
                #Menu Controller        
                options = {
                    "1: Unlock Car": "",
                    "2: Return a Car":"",
                    "3: Exit": ""
                }
                for x in options: 
                    print (x)
                
                print ("select an option") 
                selectedOption = input()
                if (selectedOption == "1"):
                    unlockCar()
                    return
                elif (selectedOption == "2"):
                    returnCar()
                    return
                elif (selectedOption == "3"):
                    sys.exit(0)
                    return
                else:
                    print("invalid choice")
                    return
            controller()
    else:
        print("incorrect login details")
    
if __name__ == '__main__':
    t1 = threading.Thread(target=interface, args=()) 
    t2 = threading.Thread(target=locationTimer, args=())
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    
 
    
    
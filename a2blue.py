import bluetooth

def scan():
    print("Scanning...")
    nearby_devices = bluetooth.discover_devices(lookup_names=True)
    print("Found %d devices" % len(nearby_devices))

    for addr, name in nearby_devices:
        devName = name
        print (devName)

def login():
    print("Scanning...")
    nearby_devices = bluetooth.discover_devices(lookup_names=True)
    
    for addr, name in nearby_devices:
        for key, value in macList.items():
            if (key == addr):
                print ("Login successful")


def addDevice():
    print ("Enter Device Name")
    deviceName = input()
    print("Scanning...")
    nearby_devices = bluetooth.discover_devices(lookup_names=True)
    for addr, name in nearby_devices:
        devName = name
        devMac = addr
        if (devName == deviceName):
            macList[devMac] = devName
            print ("Found device and added")
            return
    print ("Device not found, unable to add")
    return

def interface():
    while (True):   
        options = {
            "1: Add device": "",
            "2: Scan login":"",
            "3: Scan for nearby devices":"",
            "3: Exit": ""
            }
        for x in options: 
            print (x)
        print ("Select an option...")
        selectedOption = input()
        if (selectedOption == "1"):
            addDevice()          
        elif (selectedOption == "2"):
           login()
        elif (selectedOption == "3"):
           scan()
        elif (selectedOption == "4"):
           print ("selected 4")
        else:
            print("invalid choice")
           
if __name__ == "__main__":
   macList = {'exampleTest': '111111'} #to be filled by cloud db list
   interface()





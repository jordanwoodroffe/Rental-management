# IOT Assignment 2
Private repo for Assignment 2 PIoT - Car Share Application

## Setup
- update variables inside .env file:   
  - DB_NAME: name of your database in Google Cloud SQL instance
  - DB_USER: user name for Google Cloud SQL instance (default is root)
  - DB_PASS: user password for Google Cloud SQL instance
  - LOCAL_IP: IP of device - web-app accessible over local network


- setup port-forwarding on master network if operating across multiple networks

## How to start
- To start the server, run:

```sh
$ cd IOTA2
$ flask run
```
The website will run at ***LOCAL_IP:5000***

## How to use
- populate the database with data if empty:
  - ```/populate``` endpoint provides auto-load function for sample data [```test_data/*.csv```](https://github.com/jordanwoodroffe/IOTA2/test_data)
- the master pi web app is used to register, and once logged in a user can book vehicles, cancel bookings, search cars, view locations, and register for facial unlock of vehicles
- the agent console app is used to authenticate users, where they can login with credentials or by face, and then unlock or return a vehicle
## Requirements
- You need at least 2 x Raspberry Pi 3 Model B
  - 1 agent: client.pyå
  - 1 master: server.py, app.py
- You need Python3 and Pip
- To install dependencies, run:
```sh
pip install -r requirements.txt
```

## Group members
- [Đào Việt Quang](https://github.com/DanDanDao)
- [Donald U'Ren](https://github.com/donald-uren)
- [Jordy Woodroffe](https://github.com/jordanwoodroffe)
- [Kev Mason](https://github.com/Evzy)

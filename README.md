# IOT Assignment 2
Private repo for Assignment 2 PIoT - Car Share Application

## About the project
![App screenshot](https://github.com/jordanwoodroffe/IOTA2/blob/develop/wiki/app%20screen_shoot.png)
This is an university project attempting to develop a Internet of Things application for a cer booking service. The development team have 4 members, the project lasts 8 weeks in totals.

### Built with
- [Flask](https://palletsprojects.com/p/flask/)
- [Jinja](https://jinja.palletsprojects.com/en/2.11.x/)
- [Google Cloud Platform](https://cloud.google.com/)
- [Bootstrap](https://getbootstrap.com/)
- [OpenCV Face Recognition](https://pypi.org/project/opencv-python/)
- [Pip FaceRecognition](https://pypi.org/project/face-recognition/)
- [Mockaroo](https://mockaroo.com/)

## Setup
- update variables inside .env file:   
  - DB_NAME: name of your database in Google Cloud SQL instance
  - DB_USER: user name for Google Cloud SQL instance (default is root)
  - DB_PASS: user password for Google Cloud SQL instance
  - LOCAL_IP: IP of device - web-app accessible over local network

- setup port-forwarding on master network if operating across multiple networks

- setup google cloud proxy for development environemnt

## How to start
- To start the server, run:

```sh
$ cd IOTA2
$ flask run
```
The website will run at ***LOCAL_IP:5000***

In order to enable Google Calendar for private IP addresses, access site though ***LOCAL_IP.xip.io:5000***
> xip.io is a magic domain name that provides wildcard DNS for any IP address.

## How to use
- populate the database with data if empty:
  - ```/populate``` endpoint provides auto-load function for sample data [```test_data/*.csv```](https://github.com/jordanwoodroffe/IOTA2/test_data)
- the master pi web app is used to register, and once logged in a user can book vehicles, cancel bookings, search cars, view locations, and register for facial unlock of vehicles
- the agent console app is used to authenticate users, where they can login with credentials or by face, and then unlock or return a vehicle

## Requirements
- You need at least 2 x Raspberry Pi 3 Model B
  - 1 agent: client.py
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

## Reference
- [Flask documentation](https://flask.palletsprojects.com/en/1.1.x/)
- [Connect to Google CLoud SQL from external application](https://cloud.google.com/sql/docs/mysql/connect-external-app)
- [Google Calendar API Python Quickstart](https://developers.google.com/calendar/quickstart/python)

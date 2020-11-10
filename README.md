## Table of contents
1. [About](#about-the-project)
2. [Build](#built-with)
3. [Setup](#setup)
4. [How to start](#how-to-start)
5. [How to use: Employee](#how-to-use-employee-app-assignment-3)
6. [How to use: Customer](#how-to-use-customer-app-assignment-2)
7. [Requirements](#requirements)
8. [Reference](#reference)
9. [Trello and Github Usage](#trello-and-github-usage)


## About the project
This is a project attempting to develop a Internet of Things application for a car booking service.

![Customer App screenshot](https://github.com/jordanwoodroffe/IOTA2/blob/a3-mp-app/wiki/customer.png)

The application allows users to book vehicles, each vehicle being linked to a Raspberry Pi. Users can browse the car's 
location and optionally register for facial recognition unlock of a booked vehicle. Users can also log into a web app
in order to manage bookings.

The employee side of the application allows for three types of employees: Admin, Engineer, and Company Manager.

![Admin App screenshot](https://github.com/jordanwoodroffe/IOTA2/blob/a3-mp-app/wiki/admin.png)

Admin staff can log into a web application to view and manage users, employees, and vehicles. Admin staff may also log
repair requests, and notify the engineering team of any requested repairs. 

![Engineer App screenshot](https://github.com/jordanwoodroffe/IOTA2/blob/a3-mp-app/wiki/engineer.png)

Engineers are responsible for carrying out repair requests, and can log into a web app to view the locations of cars 
that require repairs. 

![Manager App screenshot](https://github.com/jordanwoodroffe/IOTA2/blob/a3-mp-app/wiki/manager.png)

Company managers can log in to a web application in order to view business metrics and analyse company performance

### Built with
- [Flask](https://palletsprojects.com/p/flask/)
- [Jinja](https://jinja.palletsprojects.com/en/2.11.x/)
- [Google Cloud Platform](https://cloud.google.com/)
- [Google Maps Javascript API](https://developers.google.com/maps/documentation/javascript/)
- [Bootstrap](https://getbootstrap.com/)
- [OpenCV](https://pypi.org/project/opencv-python/)
- [Pip FaceRecognition](https://pypi.org/project/face-recognition/)
- [Mockaroo](https://mockaroo.com/)

## Setup
- update variables inside .env file:   
  - DB_NAME: name of your database in Google Cloud SQL instance
  - DB_USER: user name for Google Cloud SQL instance (default is root)
  - DB_PASS: user password for Google Cloud SQL instance
  - DB_IP: IP of database instance - web-app accessible over local network
  - PORT_NUMBER: port to connect to
  - USER_PW: convenience/testing value for default user/employee password
  - PUSH_BULLET_TOKEN: Access token for pushbullet account, required for notifications
  - GOOGLE_MAPS_KEY: Google Maps Javascript API key

- setup port-forwarding on master network if operating across multiple networks

- setup google cloud proxy for development environment

## Testing
- Some of the unit tests

<img src="https://github.com/jordanwoodroffe/IOTA2/blob/master/wiki/test_website.png" width="300"><img src="https://github.com/jordanwoodroffe/IOTA2/blob/master/wiki/test_app.png" width="300"><img src="https://github.com/jordanwoodroffe/IOTA2/blob/master/wiki/test_api.png" width="300">




## How to start
- To start the server, run:

```sh
$ cd IOTA2
$ flask run
```
The website will run at ***127.0.0.0:5000***

In order to enable Google Calendar for private IP addresses, access site though ***LOCAL_IP.xip.io:5000***
> xip.io is a magic domain name that provides wildcard DNS for any IP address.

populate the database with data if empty:
```/populate``` endpoint provides auto-load function for sample data [```test_data/*.csv```](https://github.com/jordanwoodroffe/IOTA2/test_data)


## How to use: Employee App (Assignment 3)
directory: [```employee_app```](https://github.com/jordanwoodroffe/IOTA2/employee_app)
- the employee master pi web app is accessible only by employees. Engineers may login to view repair requests and locations, Managers may log in to view an analytics dashbaord, and 
Admin staff may log in to view/manage/update users employees and cars, and to file repair requests for vehicles.
- the employee agent pi app is used by engineers to login to vehicles and perform repairs. it includes object recognition to retrieve an employees details via a QR code, along with automatic bluetooth recognition for convenient vehicle unlocking.

Admin Details:
- username: donalduren 
- password: 123Qwe!

Engineer Details:
- username jwoodroffe 
- password 123Qwe!

Manager Details:
- username: johnsmith 
- password: 123Qwe!

## How to use: Customer App (Assignment 2)
directory: [```customer_app```](https://github.com/jordanwoodroffe/IOTA2/customer_app)
- the customer master pi web app is used to register, and once logged in a user can book vehicles, cancel bookings, search cars, view locations, and register for facial unlock of vehicles
- the customer agent console app is used to authenticate users, where they can login with credentials or by face, and then unlock or return a vehicle

Customer Details:
- username: dandandao
- password: 123Qwe!

## Requirements
- You need at least 2 x Raspberry Pi 3 Model B
  - 1 agent: client.py
  - 1 master: server.py, app.py
- You need Python3 and Pip
- To install dependencies, run:
```sh
pip install -r requirements.txt
```

## Reference
- [Flask documentation](https://flask.palletsprojects.com/en/1.1.x/)
- [Connect to Google CLoud SQL from external application](https://cloud.google.com/sql/docs/mysql/connect-external-app)
- [Google Calendar API Python Quickstart](https://developers.google.com/calendar/quickstart/python)

## Trello and Github Usage

[Assignment 3 Trello Board](https://trello.com/b/vUtlSkvC/iot-a3)

![Example branches](https://github.com/jordanwoodroffe/IOTA2/blob/a3-mp-app/wiki/branches.png)

![Trello board](https://github.com/jordanwoodroffe/IOTA2/blob/a3-mp-app/wiki/trello1.png)

![Example Trello card](https://github.com/jordanwoodroffe/IOTA2/blob/a3-mp-app/wiki/trello2.png)

![Database design](https://github.com/jordanwoodroffe/IOTA2/blob/a3-mp-app/wiki/database.png)


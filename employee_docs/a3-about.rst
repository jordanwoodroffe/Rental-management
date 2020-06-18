####################
About Application
####################

Employee CarShare Application is a python based IoT application allowing employees to monitor and repair vehicles/users.
It uses Raspberry Pi's to locate and record Vehicles, along with a central Master Pi to perform updates to the Google
Cloud Database and to hose a web-based application for users. Additional functionality includes QR object recognition
and Bluetooth recognition for engineers to unlock vehicles, along with voice search functionality when admin staff are
browsing vehicles.

Employees fall into one of three categories:

- Admin:
    - can updated/modify users, employees and vehicle data
    - can also raise and report repair requests
- Engineer:
    - responsible for repairing vehicles
    - Can log in to MP app to view a map of repairs, and can complete repairs from the AP application
- Company Manager: can view an analytics/visualisation dashboard showing business performance:
    - view a daily graph of current month's revenue
    - view a chart indicating proportion of vehicle fleet that are currently in repair
    - view a chart indicating the daily number of new users
    - view various revenue and month performance comparison metrics

Group Members
-------------
Đào Việt Quang
^^^^^^^^^^^^^^
Student number: S3687103

Github: `dandandao <https://github.com/DanDanDao>`_

Donald U'Ren
^^^^^^^^^^^^
Student number: S3686963

Github: `donald-uren <https://github.com/donald-uren>`_

Evan Mason
^^^^^^^^^^
Student number: S3688949

Github: `Evzy <https://github.com/Evzy>`_

Jordy Woodroffe
^^^^^^^^^^^^^^^
Student number: S3751435

Github: `jordanwoodroffe <https://github.com/jordanwoodroffe>`_

Contributions
-------------

Part A: Employee Web Application/Database API (55%)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Employee Login - :ref:`Đào Việt Quang`, :ref:`Donald U'Ren`

Admin app (View/edit cars and users, raise reports) - :ref:`Đào Việt Quang`, :ref:`Donald U'Ren`

Input validation  - :ref:`Đào Việt Quang`, :ref:`Donald U'Ren`

Database API & Design - :ref:`Đào Việt Quang`, :ref:`Donald U'Ren`

Visualisation report - :ref:`Đào Việt Quang`, :ref:`Donald U'Ren`

Notifications and Google Maps - :ref:`Đào Việt Quang`, :ref:`Donald U'Ren`

Sphinx documentation - :ref:`Đào Việt Quang`, :ref:`Donald U'Ren`

Github/Trello - :ref:`Đào Việt Quang`, :ref:`Donald U'Ren`

Part B: Voice Recognition and Bluetooth Recognition (25%)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Bluetooth identification - :ref:`Jordy Woodroffe`

Voice search - :ref:`Jordy Woodroffe`

Sphinx/Trello/Github - :ref:`Jordy Woodroffe`

Part C: QR/Object Recognition (10%)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

QR/Object Recognition - :ref:`Evan Mason`

Sphinx/Trello/Github - :ref:`Evan Mason`

Part D: Unit Tests (10%)
^^^^^^^^^^^^^^^^^^^^^^^^

Part A unit tests - :ref:`Đào Việt Quang`, :ref:`Donald U'Ren`

Part B unit tests - :ref:`Jordy Woodroffe`

Part C unit tests  - :ref:`Evan Mason`

# ImmerVerloren Box Service
## Object Oriented Programming & Database Systems
## Final Exam Project

Developed by:
- Samuel Marcellino Setiawan (202000202)
- Jastin Suriono (202000162)

## Requirements:
### Programming languages and libraries used:
- Python is the main programming language for the development of this program

* Python 3.9 and above installed on your machine
* Arduino IDE 1.8.16

### Libraries:
* smtplib -- used to send email to clients
* kink -- provides dependency injection
* pyfirmata -- provides control to an Arduino microcontroller from Python code
* matplotlib -- displays graphs and plots
* numpy -- helps process data for plots and graphs
* abc -- define abstract base classes
* datetime -- compute datetime object arithmetic
* sqlite3 -- commit changes to database and query data from database

### Materials used:
* Arduino microcontroller
* Bread board
* 4 servos
* Jumper cables
* Pre-made locker boxes made from acrylic

## Run the program
You can run this program with three options:
1. Run the program with a brand new and empty database
```python
python -m locker dbinit=True
```

2. Run the program with previously loaded database
```python
python -m locker dbinit=False
```

3. Run the program with pre-loaded data to showcase several functionalities of the program.
Such as displaying plots from pre-loaded data
```python
python -m locker dbinit=Demo
```

## Run tests
You can run tests made for this project by simply typing
```pytest```
in the command line of the project directory.

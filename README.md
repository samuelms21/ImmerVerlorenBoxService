# Python Locker Service
## Object Oriented Programming & Database Systems Final Exam Project

Developed by:
- Samuel Marcellino Setiawan (202000202)  
  [github.com/samuelms21](https://github.com/samuelms21)
- Jastin Suriono (202000162)  
  [github.com/tintin1100](https://github.com/tintin1100)

## Requirements:
### Programming languages and libraries used:
- Python is the main programming language for the development of this program

* Python 3.9 and above installed on your machine
* Arduino IDE 1.8.16

### Libraries:
* smtplib     
* kink
* pyfirmata  
* matplotlib
* numpy       
* abc
* datetime    
* sqlite3
* tkinter     
* pytest

### How to install libraries
```python
pip install pytest
pip install numpy
pip install matplotlib
pip install kink
pip install pyfirmata
```

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

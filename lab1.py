#HOME
print("Hello, World!")

#GET STARTED
import sys

print(sys.version)

#SYNTAX
if 5 > 2:
  print("Five is greater than two!")

#COMMENTS
#print("Hello, World!")
print("Cheers, Mate!")

#VARIABLES
x = 5
y = "John"
print(type(x))
print(type(y))

#VARIABLE NAMES
myvar = "John"
my_var = "John"
_my_var = "John"
myVar = "John"
MYVAR = "John"
myvar2 = "John"

#ASSIGN MULTIPLE VALUES
x, y, z = "Orange", "Banana", "Cherry"
print(x)
print(y)
print(z)

#OUTPUT VARIABLES
x = "Python"
y = "is"
z = "awesome"
print(x, y, z)

#GLOBAL VARIABLES
x = "awesome"

def myfunc():
  print("Python is " + x)

myfunc()

#DATA TYPES
x = ["apple", "banana", "cherry"]

#display x:
print(x)

#display the data type of x:
print(type(x)) 

#NUMBERS
x = 35e3
y = 12E4
z = -87.7e100

print(type(x))
print(type(y))
print(type(z))

#CASTING 
x = int(1)   # x will be 1
y = int(2.8) # y will be 2
z = int("3") # z will be 3
print(x)
print(y)
print(z)

#PYTHON STRINGS
print("It's alright")
print("He is called 'Johnny'")
print('He is called "Johnny"')

#SLICING STRING
b = "Hello, World!"
print(b[:5])

#MODIFY STRINGS
a = "Hello, World!"
print(a.lower())

#CONCATENATE STRINGS
a = "Hello"
b = "World"
c = a + b
print(c)

#FORMAT STRINGS
age = 36
txt = f"My name is John, I am {age}"
print(txt)

#ESCAPE CHARACTERS
txt = "We are the so-called \"Vikings\" from the north."
print(txt)


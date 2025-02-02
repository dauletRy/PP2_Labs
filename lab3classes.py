#task1
class StringS:
    def __init__(self):
        self.my_string = ""

    def getString(self):
        self.my_string = input()

    def printString(self):
        print(self.my_string.upper())
if __name__ == "__main__":
    asl = StringS()
    asl.getString()
    asl.printString()

#task2
class ShapeS:
    def area(self):
        print(0)

class SquareS(ShapeS):
    def __init__(self, length):
        self.length = length

    def area(self):
        print("Area:", self.length ** 2)
if __name__ == "__main__":
    shape = ShapeS()
    shape.area()
    square = SquareS(4)
    square.area()

#task3
class ShapeS:
    def area(self):
        print(0)

class RectangleS(ShapeS):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        print("Area:", self.length * self.width)
if __name__ == "__main__":
    shape = ShapeS()
    shape.area()
    rectangle = RectangleS(2,3)
    rectangle.area()

#task4
import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def getCoordinates(self):
        print(self.x, self.y)

    def moveCoordinates(self, x, y):
        self.x += x
        self.y += y        

    def distance(self, point):
        return math.sqrt((self.x - point.x) **2 + (self.y - point.y) **2)
    
p1 = Point(1, 2)
p2 = Point(3, 4)
p1.getCoordinates()
p2.getCoordinates()
print(p1.distance(p2))
p1.moveCoordinates(2, 2)
p1.getCoordinates()

#task5
class Account():
    def __init__(self, owner):
        self.owner = owner
        self.balance = 0
    
    def checkB(self):
        print(f"Balance is {self.balance}")

    def deposit(self, amount):
        self.balance += amount
        print(f"{amount} has been deposited")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Not enough money on balance")
        else:
            self.balance -= amount
            print(f"{amount} has been withdrawn from deposit")

own = Account("Daulet")
own.checkB()
own.deposit(3000)
own.checkB()
own.withdraw(1000)
own.checkB()

#task6
def isPrime(a):
    if a < 2:
        return False
    for i in range(2, int(a ** 0.5) + 1):
        if a % i == 0:
            return False
    return True

numbers = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 17, 19, 20, 23, 29, 30, 33, 35]
primenumbers = list(filter(lambda x: isPrime(x), numbers))
print("Prime numbers in the list:", primenumbers)


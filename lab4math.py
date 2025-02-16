import math
#task1
degree = float(input("Input degree: "))
radian = degree * (math.pi / 180)
print(f"Output radian: {radian:.6f}")

#task2
h=float(input("Height: "))
b1=float(input("Base, first value: "))
b2=float(input("Base, second value: "))
A=(b1+b2)*h*0.5
print(f"Output: {A}")

#task3
n=float(input("Input number of sides: "))
l=float(input("Input the length of a side: "))
a=(l/(2*(math.tan((math.pi)/n))))
A=int(((n*l)*a)/2)
print(f"The area of the polygon is: {A}")

#task4
length = float(input("Length of base: "))
height = float(input("Height of parallelogram: "))
area = float(length * height)
print(f"Output: {area}")

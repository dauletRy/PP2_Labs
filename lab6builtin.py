#task1
import math

def multiply_list(numbers):
    return math.prod(numbers)

my_list = [2, 3, 5, 7, 8, 9]
print(multiply_list(my_list))

#task2

def count_case_letters(s):
    upper = sum(1 for c in s if c.isupper())
    lower = sum(1 for c in s if c.islower())
    return upper, lower

string = "Hi My NaMe IS DaULet!"
upper, lower = count_case_letters(string)
print(f"Uppercase: {upper}, Lowercase: {lower}")

#task3

def is_palindrome(s):
    return s == s[::-1]

print(is_palindrome("mom"))
print(is_palindrome("mother"))

#task4

import time 
num = int(input())
milsec = int(input())
sec = milsec/1000
time.sleep(sec)
sqrt = num ** 0.5
txt = 'Square root of {fnum} after {fsec} is {fsqrt}'.format(fnum = num, fsec = milsec, fsqrt = sqrt)
print(txt)

#task5

mytup = (True, True, False)
mytup2 = (True, True, True)
print(all(mytup))
print(all(mytup2))
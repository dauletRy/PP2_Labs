#task1
def squares(n):
    for i in range(1, n + 1):
        yield i * i
n = int(input())
for square in squares(n):
    print(square)

#task2
def even_numbers(n):
    for i in range(0, n + 1, 2):
        yield i
n = int(input())
even_numbers_list = list(even_numbers(n))
print(','.join(map(str, even_numbers_list)))
#task3
def divisible_by_3_and_4(n):
    for i in range(0, n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i
n = int(input())
for number in divisible_by_3_and_4(n):
    print(number)

#task4
def squares(a, b):
    for i in range(a, b + 1):
        yield i * i
a = int(input())
b = int(input())
for square in squares(a, b):
    print(square)

#task5
def countdown(n):
    for i in range(n, -1, -1):
        yield i
n = int(input())
for number in countdown(n):
    print(number)


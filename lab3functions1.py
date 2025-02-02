#task1
def ounces(gram):
    print(gram*28.3495231)
ounces(int(input()))

#task2
def temperature(fahrenheit):
    print((5/9)*(fahrenheit-32))
temperature(int(input()))

#task3
def solve(numheads, numlegs):
    rabbits=(numlegs-(2*numheads))//2
    chickens=numheads-rabbits
    print("Chickens:",chickens)
    print("Rabbits:",rabbits)
solve(35, 94)

#task4
def is_prime(a):
    if a < 2:
        return False
    for i in range(2, int(a ** 0.5) + 1):
        if a % i == 0:
            return False
    return True

def filter_prime(numbers):
    return [num for num in numbers if is_prime(num)]

input_numbers = input()
number_list = list(map(int, input_numbers.split()))

prime_numbers = filter_prime(number_list)
print(prime_numbers)

#task5
def permute(s, answer=""):
    if len(s) == 0:
        print(answer)
        return

    for i in range(len(s)):
        ch = s[i]
        left_substr = s[:i]
        right_substr = s[i+1:]
        rest = left_substr + right_substr

        permute(rest, answer + ch)

word = input()
permute(word)

#task6
def reverse_words(sentence):
    words = sentence.split()
    words.reverse()
    return ' '.join(words)

sentence = input()
print(reverse_words(sentence))

#task7
def has_33(nums):
    for i in range(len(nums) - 1):
        if nums[i] == 3 and nums[i + 1] == 3:
            return True
    return False

print(has_33([1, 3, 3]))
print(has_33([1, 3, 1, 3]))
print(has_33([3, 1, 3]))

#task8
def spy_game(nums):
    for i in range(len(nums) - 2):
        if nums[i] == 0 and nums[i + 1] == 0 and nums[i + 2] == 7:
            return True
        elif nums[i] == 0 and nums[i + 1] != 0:
            return False
        elif nums[i] == 0 and nums[i + 1] == 0 and nums[i + 2] != 7:
            return False

print(spy_game([1,2,4,0,0,7,5])) 
print(spy_game([1,0,2,4,0,5,7])) 
print(spy_game([1,7,2,0,4,5,0])) 

#task9
def sphereVol(rad):
    vol = lambda r: (4/3) * 3.14 * pow(r, 3)
    print(vol(rad))

rad = int(input())
sphereVol(rad)

#task10
def unique_elements(nums):
    unique_list = []
    for num in nums:
        if num not in unique_list:
            unique_list.append(num)
    return unique_list

nums = [1, 2, 2, 3, 4, 4, 5]
print(unique_elements(nums))

#task11
def isPal(word):
    if word == word[::-1]:
        return True
    else:
        return False

word = input()
print(isPal(word))

#task12
def histogram(nums):
    curr = '*'
    for val in nums:
        if val != 0:
            curr = curr * val
        else:
            curr = ''
        print(curr)
        curr = '*'

histogram([4, 9, 7])

#task13
import random

def game():
    name = input("Hello! What is your name? \n")
    guess = 0
    num = 0
    gnum = random.randint(1, 20)
    print("Well, {fname}, I am thinking of a number between 1 and 20.\nTake a guess.".format(fname=name))
    while num != gnum and guess < 3:
        num = int(input())
        if num < gnum:
            guess += 1
            print("Your guess is too low.\nTake a guess.")
        elif num > gnum:
            guess += 1
            print("Your guess is too high.\nTake a guess.")
        else:
            guess += 1
            print("Good job, {fname}! You guessed my number in {fguess} guesses!".format(fname=name, fguess=guess))
            break
    if guess == 3 and num != gnum:
        print("You're out of guesses, try again.")

game()



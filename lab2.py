#PYTHON BOOLEAN

x = 200
print(isinstance(x, int))

#PYTHON OPERATORS

print(100 + 5 * 3)

#PYTHON SETS

thisset = {"apple", "banana", "cherry"}
print(thisset)

#PYTHON ACCESS SET ITEMS

thisset = {"apple", "banana", "cherry"}

print("banana" in thisset)

#PYTHON ADD SET ITEMS

thisset = {"apple", "banana", "cherry"}
tropical = {"pineapple", "mango", "papaya"}

thisset.update(tropical)

print(thisset)

#PYTHON REMOVE SET ITEMS

thisset = {"apple", "banana", "cherry"}

thisset.discard("banana")

print(thisset)

#PYTHON LOOP SETS

thisset = {"apple", "banana", "cherry"}

for x in thisset:
  print(x)

#PYTHON JOIN SETS

set1 = {"a", "b", "c"}
set2 = {1, 2, 3}

set3 = set1.union(set2)
print(set3)

#PYTHON DICTIONARIES

thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
print(thisdict)

#PYTHON ACCESS ITEMS

car = {
"brand": "Ford",
"model": "Mustang",
"year": 1964
}

x = car.keys()

print(x) #before the change

car["color"] = "white"

print(x) #after the change

#PYTHON CHANGE ITEMS

thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
thisdict.update({"year": 2020})
print(thisdict)

#PYTHON ADD ITEMS

thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
thisdict.update({"color": "red"})

print(thisdict)

#PYTHON REMOVE ITEMS

thisdict =	{
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
thisdict.popitem()
print(thisdict)

#PYTHON LOOP DICTIONARIES

thisdict =	{
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
for x in thisdict:
  print(thisdict[x])

#PYTHON COPY DICTIONARIES

thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
mydict = thisdict.copy()
print(mydict)

#PYTHON NESTED DICTIONARIES

myfamily = {
  "child1" : {
    "name" : "Emil",
    "year" : 2004
  },
  "child2" : {
    "name" : "Tobias",
    "year" : 2007
  },
  "child3" : {
    "name" : "Linus",
    "year" : 2011
  }
}

print(myfamily)

#PYTHON IF ... ELSE

a = 33
b = 200

if b > a:
  print("b is greater than a")

#PYTHON WHILE LOOPS

i = 1
while i < 6:
  print(i)
  if (i == 3):
    break
  i += 1

#PYTHON FOR LOOPS

for x in "banana":
  print(x)

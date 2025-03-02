import os
#task1

location1 = r'C:\Users\daule\Desktop\work\pp2'
print([name for name in os.listdir(location1)]) #everything
print([name for name in os.listdir(location1) if os.path.isdir(os.path.join(location1, name))]) #only directories
print([name for name in os.listdir(location1) if not os.path.isdir(os.path.join(location1, name))]) #only files

#task2

print('Path exists:', os.access(r'C:\Users\daule\Desktop\work\pp2', os.F_OK))
print('Path readable:', os.access(r'C:\Users\daule\Desktop\work\pp2', os.R_OK))
print('Path writable:', os.access(r'C:\Users\daule\Desktop\work\pp2', os.W_OK))
print('Path executable:', os.access(r'C:\Users\daule\Desktop\work\pp2', os.X_OK))

#task3

path = input('Insert path \n')
path_bool = os.access(path, os.F_OK)
if path_bool == False:
    print("Path does not exist")
elif path_bool == True:
    print("Directories:", ', '.join([name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]))
    print("Files:", ', '.join([name for name in os.listdir(path) if not os.path.isdir(os.path.join(path, name))]))

#task4

with open(r'C:\Users\daule\Desktop\work\pp2\New Text Document.txt', 'r') as file:
    x = len(file.readlines())
    print("Number of lines:", x)

#task5

mylist = ['A', 'B', 'C', 'D', 'E', 'F']
with open(r'C:\Users\daule\Desktop\work\pp2\New Text Document.txt', 'w') as file:
    for i in mylist:
        file.write(i + '\n')
file.close()

#task6

target_dir = r"C:\Users\daule\Desktop\asd"

for letter_code in range(65, 91):
    filename = f"{chr(letter_code)}.txt"
    file_path = os.path.join(target_dir, filename)
    
    with open(file_path, 'w') as f:
        f.write(f"This is {filename} in {target_dir}")

print(f"26 files created in {target_dir}")

#task7

def copy_file(source, destination):
    with open(source, 'r') as src, open(destination, 'w') as dest:
        dest.write(src.read())

copy_file(r"C:\Users\daule\Desktop\asdad.txt", r"C:\Users\daule\Desktop\asfafs.txt")

#task8

def safe_delete(path):
    if os.path.exists(path) and os.access(path, os.W_OK):
        os.remove(path)
        print(f"{path} deleted successfully")
    else:
        print("Deletion failed: File doesn't exist or isn't writable")

safe_delete(r"C:\Users\daule\Desktop\New Text Document.txt")


import psycopg2 as ps
import csv
from config import host, database, user, password

# подключаю базу данных
conn = ps.connect(
    host=host,
    user=user,
    password=password,
    database=database
)
cur = conn.cursor()

# создаю таблицу с нужными данными
cur.execute("""
CREATE TABLE IF NOT EXISTS phone_book (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone_number VARCHAR(255) NOT NULL UNIQUE
);
""")

# методы вставления
def insert_from_csv():
    """метод 1 цсв"""
    with open("input.csv", "r") as f:
        data = csv.reader(f, delimiter=',')
        next(data)  # Skip header row
        for row in data:
            try:
                cur.execute("""
                    INSERT INTO phone_book (first_name, last_name, phone_number)
                    VALUES (%s, %s, %s)
                """, (row[0], row[1], row[2]))
            except ps.IntegrityError:
                print(f"Skipped duplicate phone number: {row[2]}")
    conn.commit()
                
               

def insert_from_console():
    """метод 2- вставление данных с консоли"""
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    phone = input("Enter phone number: ")
    
    try:
        cur.execute("""
            INSERT INTO phone_book (first_name, last_name, phone_number)
            VALUES (%s, %s, %s)
        """, (first_name, last_name, phone))
        conn.commit()
    except ps.IntegrityError:
        print("This phone number already exists!")

# обновление данных
def update_record():
    id = input("Enter record ID to update: ")
    field = input("Update first name (1) or phone (2) or last name(3)")
    
    if field == '1':
        new_name = input("New first name: ")
        cur.execute("""
            UPDATE phone_book 
            SET first_name = %s 
            WHERE id = %s
        """, (new_name, id))
    elif field == '2':
        new_phone = input("New phone number: ")
        cur.execute("""
            UPDATE phone_book 
            SET phone_number = %s 
            WHERE id = %s
        """, (new_phone, id))
    elif field == '3':
        new_lname = input("New last name: ")
        cur.execute("""
            UPDATE phone_book 
            SET last_name = %s 
            WHERE id = %s
        """, (new_lname, id))
    conn.commit()

# найти
def query_records():
    filter_type = input("Filter by: all (1), name (2), phone (3), id (4): ")
    
    if filter_type == '1':
        cur.execute("SELECT * FROM phone_book")
    elif filter_type == '2':
        name = input("Enter first name: ")
        cur.execute("""
            SELECT * FROM phone_book 
            WHERE first_name ILIKE %s
        """, (f'%{name}%',))
    elif filter_type == '3':
        phone = input("Enter phone number: ")
        cur.execute("""
            SELECT * FROM phone_book 
            WHERE phone_number = %s
        """, (phone,))
    elif filter_type == '4':
        id = input("Enter ID: ")
        cur.execute("SELECT * FROM phone_book WHERE id = %s", (id,))
    
    results = cur.fetchall()
    for row in results:
        print(f"ID: {row[0]}, Name: {row[1]} {row[2]}, Phone: {row[3]}")

# удаление
def delete_record():
    target = input("Delete by: name (1) or phone (2) or id(3) ")
    
    if target == '1':
        name = input("Enter first name: ")
        cur.execute("""
            DELETE FROM phone_book 
            WHERE first_name = %s
        """, (name,))
    elif target == '2':
        phone = input("Enter phone number: ")
        cur.execute("""
            DELETE FROM phone_book 
            WHERE phone_number = %s
        """, (phone,))
    elif target == '3':
        id = input("Enter id: ")
        cur.execute("""
            DELETE FROM phone_book 
            WHERE id = %s
        """, (id,))
    
    print(f"Deleted {cur.rowcount} records")
    conn.commit()

# главное меню
if __name__ == "__main__":
    try:
        while True:
            print("\nPhone Book Manager")
            print("1. Add from CSV\n2. Add from console\n3. Update\n4. Search\n5. Delete\n6. Exit")
            choice = input("Select operation: ")
            
            if choice == '1':
                insert_from_csv()
            elif choice == '2':
                insert_from_console()
            elif choice == '3':
                update_record()
            elif choice == '4':
                query_records()
            elif choice == '5':
                delete_record()
            elif choice == '6':
                break
                
    finally:
        cur.close()
        conn.close()
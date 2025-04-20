import psycopg2 as ps
import csv
from config import host, database, user, password
'''
-- Удаляем все старые функции и процедуры (если существуют)
DROP FUNCTION IF EXISTS find_by_pattern(TEXT);
DROP FUNCTION IF EXISTS paginate_phone_book(INTEGER, INTEGER);
DROP PROCEDURE IF EXISTS insert_or_update_user(TEXT, TEXT, TEXT);
DROP PROCEDURE IF EXISTS insert_many_users(TEXT[][]);
DROP PROCEDURE IF EXISTS delete_by_username_or_phone(TEXT);

-- 1. Функция поиска по шаблону (name, surname, phone)
CREATE OR REPLACE FUNCTION find_by_pattern(pattern TEXT)
RETURNS TABLE(id INT, first_name VARCHAR(50), last_name VARCHAR(50), phone_number VARCHAR(255))
AS $$
BEGIN
    RETURN QUERY
    SELECT pb.id, pb.first_name, pb.last_name, pb.phone_number
    FROM phone_book pb
    WHERE pb.first_name ILIKE '%' || pattern || '%'
       OR pb.last_name ILIKE '%' || pattern || '%'
       OR pb.phone_number ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;

-- 2. Процедура вставки пользователя или обновления телефона, если он уже есть
CREATE OR REPLACE PROCEDURE insert_or_update_user(fname TEXT, lname TEXT, phone TEXT)
AS $$ 
BEGIN
    IF EXISTS (
        SELECT 1 FROM phone_book 
        WHERE first_name = fname AND last_name = lname
    ) THEN
        UPDATE phone_book 
        SET phone_number = phone
        WHERE first_name = fname AND last_name = lname;
    ELSE
        INSERT INTO phone_book(first_name, last_name, phone_number)
        VALUES (fname, lname, phone);
    END IF;
END;
$$ LANGUAGE plpgsql;

-- 3. Процедура для вставки нескольких пользователей, с проверкой формата телефона
CREATE OR REPLACE PROCEDURE insert_many_users(user_data TEXT[][])
LANGUAGE plpgsql
AS $$ 
DECLARE
    r TEXT[];
    invalid_users TEXT := '';
BEGIN
    FOREACH r SLICE 1 IN ARRAY user_data
    LOOP
        IF r[3] !~ '^\+?[0-9]{10,15}$' THEN
            invalid_users := invalid_users || format('Invalid: %s %s (%s)\n', r[1], r[2], r[3]);
            CONTINUE;
        END IF;

        BEGIN
            CALL insert_or_update_user(r[1], r[2], r[3]);
        EXCEPTION
            WHEN OTHERS THEN
                invalid_users := invalid_users || format('Error: %s %s (%s)\n', r[1], r[2], r[3]);
        END;
    END LOOP;

    RAISE NOTICE 'Invalid or failed entries: %', invalid_users;
END;
$$;

-- 4. Функция с пагинацией по limit и offset
CREATE OR REPLACE FUNCTION paginate_phone_book(limit_count INT, offset_count INT)
RETURNS TABLE(id INT, first_name VARCHAR(50), last_name VARCHAR(50), phone_number VARCHAR(255))
AS $$
BEGIN
    RETURN QUERY
    SELECT pb.id, pb.first_name, pb.last_name, pb.phone_number
    FROM phone_book pb
    ORDER BY pb.id
    LIMIT limit_count OFFSET offset_count;
END;
$$ LANGUAGE plpgsql;

-- 5. Удаление по имени или телефону
CREATE OR REPLACE PROCEDURE delete_by_username_or_phone(identifier TEXT)
AS $$ 
BEGIN
    DELETE FROM phone_book
    WHERE first_name = identifier
       OR last_name = identifier
       OR phone_number = identifier;
END;
$$ LANGUAGE plpgsql;

'''

# подключаюсь к БД
conn = ps.connect(
    host=host,
    user=user,
    password=password,
    database=database
)
cur = conn.cursor()

# создаю таблицу
cur.execute("""
CREATE TABLE IF NOT EXISTS phone_book (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone_number VARCHAR(255) NOT NULL UNIQUE
);
""")
conn.commit()

# вставка из CSV
def insert_from_csv():
    with open("input.csv", "r") as f:
        data = csv.reader(f, delimiter=',')
        next(data)  # пропускаем заголовок
        for row in data:
            try:
                cur.execute("""
                    INSERT INTO phone_book (first_name, last_name, phone_number)
                    VALUES (%s, %s, %s)
                """, (row[0], row[1], row[2]))
            except ps.IntegrityError:
                conn.rollback()
                print(f"Skipped duplicate phone number: {row[2]}")
    conn.commit()

# вставка с консоли
def insert_from_console():
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
        conn.rollback()
        print("This phone number already exists!")

# обновление
def update_record():
    id = input("Enter record ID to update: ")
    field = input("Update first name (1), last name (2), phone (3): ")

    if field == '1':
        new_name = input("New first name: ")
        cur.execute("UPDATE phone_book SET first_name = %s WHERE id = %s", (new_name, id))
    elif field == '2':
        new_lname = input("New last name: ")
        cur.execute("UPDATE phone_book SET last_name = %s WHERE id = %s", (new_lname, id))
    elif field == '3':
        new_phone = input("New phone number: ")
        cur.execute("UPDATE phone_book SET phone_number = %s WHERE id = %s", (new_phone, id))
    conn.commit()

# поиск
def query_records():
    filter_type = input("Filter by: all (1), name (2), phone (3), id (4): ")

    if filter_type == '1':
        cur.execute("SELECT * FROM phone_book")
    elif filter_type == '2':
        name = input("Enter first name: ")
        cur.execute("SELECT * FROM phone_book WHERE first_name ILIKE %s", (f'%{name}%',))
    elif filter_type == '3':
        phone = input("Enter phone number: ")
        cur.execute("SELECT * FROM phone_book WHERE phone_number = %s", (phone,))
    elif filter_type == '4':
        id = input("Enter ID: ")
        cur.execute("SELECT * FROM phone_book WHERE id = %s", (id,))
    
    results = cur.fetchall()
    for row in results:
        print(f"ID: {row[0]}, Name: {row[1]} {row[2]}, Phone: {row[3]}")

# удаление
def delete_record():
    target = input("Delete by: name (1), phone (2), id (3): ")
    if target == '1':
        name = input("Enter name: ")
        cur.execute("CALL delete_by_username_or_phone(%s)", (name,))
    elif target == '2':
        phone = input("Enter phone number: ")
        cur.execute("CALL delete_by_username_or_phone(%s)", (phone,))
    elif target == '3':
        id = input("Enter id: ")
        cur.execute("DELETE FROM phone_book WHERE id = %s", (id,))
    
    print(f"Deleted {cur.rowcount} records")
    conn.commit()

# главное меню
if __name__ == "__main__":
    try:
        while True:
            print("\nPhone Book Manager")
            print("1. Add from CSV\n2. Add from console\n3. Update\n4. Search\n5. Delete")
            print("6. Search by pattern\n7. Insert/update user\n8. Bulk insert")
            print("9. Paginated view\n10. Exit")  

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
                pattern = input("Enter pattern: ")
                cur.execute("SELECT * FROM find_by_pattern(%s)", (pattern,))
                for row in cur.fetchall():
                    print(row)
            elif choice == '7':
                fname = input("First name: ")
                lname = input("Last name: ")
                phone = input("Phone: ")
                cur.execute("CALL insert_or_update_user(%s, %s, %s)", (fname, lname, phone))
                conn.commit()
            elif choice == '8':
                # вводим двумерный массив как текст
                n = int(input("How many users to insert? "))
                user_data = []
                for _ in range(n):
                    fname = input("First name: ")
                    lname = input("Last name: ")
                    phone = input("Phone: ")
                    user_data.append([fname, lname, phone])
                cur.execute("CALL insert_many_users(%s)", (user_data,))
                conn.commit()
            elif choice == '9':
                limit = int(input("Limit: "))
                offset = int(input("Offset: "))
                cur.execute("SELECT * FROM paginate_phone_book(%s, %s)", (limit, offset))
                for row in cur.fetchall():
                    print(row)
            elif choice == '10':
                break
    finally:
        cur.close()
        conn.close()

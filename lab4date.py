#task1
from datetime import datetime, timedelta
today=datetime.now()
past_time=today-timedelta(days=5)
print(today)
print(past_time)

#task2
from datetime import datetime, timedelta
today=datetime.now()
yesterday=today-timedelta(days=1)
tomorrow=today+timedelta(days=1)
print(yesterday)
print(today)
print(tomorrow)

#task3
import datetime

today = datetime.datetime.now()

print(today.strftime('%d/%m/%Y, %H:%M:%S'))

#task4
from datetime import datetime

date_format = "%Y-%m-%d %H:%M:%S"

date1_str = input("Enter the first date (YYYY-MM-DD HH:MM:SS): ")

date2_str = input("Enter the second date (YYYY-MM-DD HH:MM:SS): ")

date1 = datetime.strptime(date1_str, date_format)

date2 = datetime.strptime(date2_str, date_format)

difference = date2 - date1

difference_in_seconds = difference.total_seconds()

print(f"The difference between the two dates is {difference_in_seconds} seconds.")

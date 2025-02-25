import sqlite3

## connect to sqlite
connection = sqlite3.connect("student1.db")
## Create table
cursor=connection.cursor()

## create table

table_info=""" Create table student1 (name varchar(255),class varchar(255),section varchar(255),marks int)
"""
cursor.execute(table_info)


#insert more records
cursor.execute('''insert into student1 values('Krish','Data Science','A',90)''')
cursor.execute('''Insert Into STUDENT1 values('John','Data Science','B',100)''')
cursor.execute('''Insert Into STUDENT1 values('Mukesh','Data Science','A',86)''')
cursor.execute('''Insert Into STUDENT1 values('Jacob','DEVOPS','A',50)''')
cursor.execute('''Insert Into STUDENT1 values('Dipesh','DEVOPS','A',35)''')

# show records
print("inserted records are")
data = cursor.execute('''select * from student1''')
for row in data:
    print(row)

# commite your changes in database
connection.commit()
connection.close()

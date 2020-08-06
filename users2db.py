import sqlite3
con=sqlite3.connect("users.db")
con.execute("create table users2(id INTEGER PRIMARY KEY AUTOINCREMENT, fullname TEXT NOT NULL, email TEXT NOT NULL, phonenumber TEXT NOT NULL, password TEXT NOT NULL,profilepic TEXT NOT NULL)")
print("Table Created Successfully")
con.close()                
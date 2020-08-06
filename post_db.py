import sqlite3
con=sqlite3.connect("users.db")
con.execute("create table posts4 (post_id INTEGER PRIMARY KEY AUTOINCREMENT,id NUMBER NOT NULL, title TEXT NOT NULL, author TEXT NOT NULL, news TEXT NOT NULL, category TEXT NOT NULL,image TEXT NOT NULL)")
print("Table Created Successfully")
con.close()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
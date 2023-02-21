import sqlite3
def create_db():
    con=sqlite3.connect(database=r'ims.db')
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS customer(custid INTEGER PRIMARY KEY AUTOINCREMENT,name text,gender text,contact text,email text,address text)")
    con.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS product(pid INTEGER PRIMARY KEY AUTOINCREMENT,name text,price text,qty text,status text)")
    con.commit()

create_db()
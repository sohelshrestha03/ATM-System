import sqlite3

conn=sqlite3.connect("atm.db")
cur=conn.cursor()
cur.execute('''
 CREATE TABLE IF NOT EXISTS user(
  account_id INTEGER PRIMARY KEY AUTOINCREMENT,
  account_no TEXT UNIQUE,
  full_name TEXT NOT NULL,
  phone_no TEXT NOT NULL,
  email TEXT NOT NULL,
  new_pin TEXT,
  confirm_pin TEXT,
  balance REAL DEFAULT 0
 );
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS transactions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_no TEXT,
    type TEXT,
    amount REAL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES user(account_id)
 );
''')

conn.commit()
conn.close()

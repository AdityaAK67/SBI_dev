import sqlite3
user_input = input("Enter username: ")
query = f"SELECT * FROM users WHERE name = '{user_input}'"
conn = sqlite3.connect("database.db")
conn.execute(query) 

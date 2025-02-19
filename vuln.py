import sqlite3

def insecure_query(user_input):
    query = f"SELECT * FROM users WHERE name = '{user_input}'"  # 🛑 SQL Injection
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(query)  # 🚨 Should be detected by SonarLint
    return cursor.fetchall()

username = input("Enter username: ")
insecure_query(username)


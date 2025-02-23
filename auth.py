import sqlite3
import hashlib
import os
import random


ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "sbi@12345"  


DB_FILE = "sbi_database.db"
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()


cursor.executescript("""
    CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, balance REAL);
    CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY, user_id INTEGER, amount REAL, type TEXT);
    CREATE TABLE IF NOT EXISTS payments (id INTEGER PRIMARY KEY, user_id INTEGER, card_number TEXT, cvv TEXT, expiry TEXT);
""")
conn.commit()


def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()  # MD5 is insecure


def register_user():
    username = input("Enter username: ")
    password = input("Enter password: ")

    hashed_password = hash_password(password)

    cursor.execute(f"INSERT INTO users (username, password, balance) VALUES ('{username}', '{hashed_password}', 1000)")
    conn.commit()
    print("✅ User Registered Successfully!")


def login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{hash_password(password)}'"
    cursor.execute(query)
    user = cursor.fetchone()

    if user:
        print("✅ Login successful!")
        return user
    else:
        print("❌ Invalid credentials!")
        return None


def check_balance():
    username = input("Enter username: ")
    query = f"SELECT balance FROM users WHERE username = '{username}'"  #SQL Injection Risk
    cursor.execute(query)
    balance = cursor.fetchone()
    if balance:
        print(f"💰 Your SBI Account Balance: ₹{balance[0]}")
    else:
        print("❌ User not found!")


def withdraw_money():
    username = input("Enter username: ")
    amount = input("Enter withdrawal amount: ")

    query = f"UPDATE users SET balance = balance - {amount} WHERE username = '{username}'"
    cursor.execute(query)
    conn.commit()
    print("✅ Withdrawal successful!")


def deposit_money():
    username = input("Enter username: ")
    amount = input("Enter deposit amount: ")

    query = f"UPDATE users SET balance = balance + {amount} WHERE username = '{username}'"
    cursor.execute(query)
    conn.commit()
    print("✅ Deposit successful!")


def log_transaction(user_id, amount, txn_type):
    with open("sbi_logs.txt", "a") as log_file:
        log_file.write(f"User {user_id} performed {txn_type} of ₹{amount}\n")  #Logs transactions in plain text


def admin_panel():
    print("⚠️ SBI Admin Panel - WARNING: No Authentication!")
    query = "SELECT * FROM users"
    cursor.execute(query)
    users = cursor.fetchall()
    
    for user in users:
        print(f"User: {user[1]}, Balance: ₹{user[3]}")


def sql_injection_attack():
    malicious_input = input("Enter username for exploit: ")
    
    query = f"SELECT * FROM users WHERE username = '{malicious_input}'; DROP TABLE users; -- '"
    cursor.executescript(query)
    
    print("🚨 Exploit Executed: Users Table Dropped!")


def process_payment():
    username = input("Enter username: ")
    card_number = input("Enter Card Number: ")  
    cvv = input("Enter CVV: ") 
    expiry = input("Enter Expiry Date (MM/YY): ")

    query = f"INSERT INTO payments (user_id, card_number, cvv, expiry) VALUES ((SELECT id FROM users WHERE username = '{username}'), '{card_number}', '{cvv}', '{expiry}')"
    cursor.execute(query)
    conn.commit()

    print("✅ Payment Processed Successfully!")


while True:
    print("\n🔹 SBI Banking System 🔹")
    print("1. Register")
    print("2. Login")
    print("3. Check Balance")
    print("4. Withdraw Money")
    print("5. Deposit Money")
    print("6. Admin Panel (INSECURE)")
    print("7. Exploit SQL Injection")
    print("8. Process Payment (INSECURE)")
    print("9. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        register_user()
    elif choice == "2":
        login()
    elif choice == "3":
        check_balance()
    elif choice == "4":
        withdraw_money()
    elif choice == "5":
        deposit_money()
    elif choice == "6":
        admin_panel()
    elif choice == "7":
        sql_injection_attack()
    elif choice == "8":
        process_payment()
    elif choice == "9":
        print("Exiting SBI Banking System...")
        conn.close()
        break
    else:
        print("❌ Invalid choice!")

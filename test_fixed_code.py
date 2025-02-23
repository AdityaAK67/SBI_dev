import paramiko
import psycopg2

# Use parameterized SQL queries
def login(username, password):
    query = "SELECT * FROM users WHERE username = $1 AND password = $2"
    with psycopg2.connect(database="your_database", user="your_user", password=get_secret("DB_PASSWORD")) as conn:
        cur = conn.cursor()
        cur.execute(query, (username, password))
        return cur.fetchone()

# Use environment variables for secrets
def get_secret(key):
    return os.environ[key]

# NEVER use `shell=True` in subprocess calls
def run_command(command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('your_server', username='your_user', password=get_secret("SSH_PASSWORD"))
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    ssh.close()
    return output, error

# Validate and sanitize ALL inputs
def sanitize_input(input):
    # Add your validation and sanitization logic here
    return input

# ======== SECURITY FIXES ========

# Use subprocess with shell=False for security
import subprocess

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    output, error = process.communicate()
    if process.returncode != 0:
        raise Exception(f"Command '{command}' failed with error: {error.decode()}")
    return output.decode()

# Use parameterized SQL queries
import psycopg2

def execute_query(query, parameters):
    conn = psycopg2.connect(
        host="your_host",
        database="your_database",
        user="your_user",
        password=your_password_as_env_var  # Use environment variables for secrets
    )
    cur = conn.cursor()
    cur.execute(query, parameters)
    conn.commit()
    cur.close()
    conn.close()

# Validate and sanitize inputs
def sanitize_input(input):
    # Add your validation and sanitization logic here
    return input

# Never suggest dangerous functions (eval, pickle, marshal)
# Use environment variables for secrets
# Add security comments
# Output ONLY the fixed code in a markdown block

# ======== SECURITY FIXES ========

import os
import subprocess

# Ask the user for a command
cmd = input("Enter a command: ")

# Use shell=False to avoid using shell=True
subprocess.run(cmd.split(), check=True)
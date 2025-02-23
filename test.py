def login(username, password):
    query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
    return query



import subprocess

# ❌ Vulnerable Code: Command Injection
cmd = input("Enter a command: ")
subprocess.run(cmd, shell=True)

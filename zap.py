# from zapv2 import ZAPv2
# import time
# import json

# # Initialize OWASP ZAP API
# zap = ZAPv2(apikey='6ik2gkjo3g2unjvnlfu72qq90s', proxies={'http': 'http://localhost:8080'})

# # Target website to scan
# target = input("Enter target URL: ")

# # Open target URL
# print(f"Accessing target: {target}")
# zap.urlopen(target)
# time.sleep(2)

# # Start Spider Scan (Crawling)
# print("Starting spider scan...")
# zap.spider.scan(target)
# while int(zap.spider.status()) < 100:
#     print(f"Spider progress: {zap.spider.status()}%")
#     time.sleep(2)

# print("Spider scan completed.")

# # Start Active Scan
# print("Starting active scan...")
# scan_id = zap.ascan.scan(target)
# while int(zap.ascan.status(scan_id)) < 100:
#     print(f"Active scan progress: {zap.ascan.status(scan_id)}%")
#     time.sleep(5)

# print("Active scan completed!")

# # Get scan results
# alerts = zap.core.alerts()
# print(f"Found {len(alerts)} vulnerabilities.")

# # Dictionary to store results
# scan_results = {}

# # Vulnerability Fix Recommendations
# fix_suggestions = {
#     "Cross Site Scripting (XSS)": {
#         "Description": "XSS allows attackers to inject malicious scripts into webpages.",
#         "Fix": [
#             "Use proper input sanitization and escaping methods.",
#             "For JavaScript: Use DOMPurify to sanitize user input.",
#             "For web frameworks: Use secure template rendering (e.g., Django's auto-escaping)."
#         ]
#     },
#     "SQL Injection": {
#         "Description": "SQL Injection occurs when attackers manipulate database queries via input fields.",
#         "Fix": [
#             "Use parameterized queries or prepared statements.",
#             "Avoid dynamic SQL string concatenation.",
#             "Use ORM frameworks like SQLAlchemy (Python) or Hibernate (Java)."
#         ]
#     },
#     "Information Disclosure": {
#         "Description": "Sensitive information such as API keys or stack traces are exposed.",
#         "Fix": [
#             "Disable detailed error messages in production.",
#             "Use HTTP headers like `X-Content-Type-Options: nosniff` and `X-Frame-Options: DENY`.",
#             "Restrict API responses to only necessary data."
#         ]
#     },
#     "Broken Authentication": {
#         "Description": "Weak authentication mechanisms allow unauthorized access.",
#         "Fix": [
#             "Use strong password hashing algorithms (e.g., bcrypt, Argon2).",
#             "Implement multi-factor authentication (MFA).",
#             "Enforce session timeout and re-authentication for sensitive actions."
#         ]
#     },
#     "Insecure Direct Object References (IDOR)": {
#         "Description": "Attackers access unauthorized resources by modifying object references (e.g., User IDs in URLs).",
#         "Fix": [
#             "Enforce server-side authorization checks for every request.",
#             "Use role-based access control (RBAC) or attribute-based access control (ABAC).",
#             "Avoid exposing internal object IDs in URLs; use UUIDs or tokens instead."
#         ]
#     },
#     "Security Misconfiguration": {
#         "Description": "Default credentials, unnecessary services, or misconfigured security settings are present.",
#         "Fix": [
#             "Disable unused services and endpoints.",
#             "Change default passwords and security settings.",
#             "Implement least privilege access for configurations."
#         ]
#     },
#     "Sensitive Data Exposure": {
#         "Description": "Sensitive data (e.g., passwords, credit card numbers) is exposed due to weak encryption or improper storage.",
#         "Fix": [
#             "Use strong encryption for data at rest and in transit (e.g., AES-256, TLS 1.2+).",
#             "Do not store sensitive data unless absolutely necessary.",
#             "Mask or tokenize sensitive information before logging."
#         ]
#     },
#     "Broken Access Control": {
#         "Description": "Users can access restricted resources or perform unauthorized actions.",
#         "Fix": [
#             "Enforce proper authorization checks on the backend.",
#             "Implement access control policies (RBAC/ABAC).",
#             "Use secure session management with proper user validation."
#         ]
#     }
# }

# # Process each alert
# for alert in alerts:
#     name = alert['name']
#     risk_level = alert['risk']
#     url = alert['url']

#     fix = fix_suggestions.get(name, {
#         "Description": "No specific details available.",
#         "Fix": ["Refer to OWASP best practices."]
#     })

#     scan_results[name] = {
#         "Risk Level": risk_level,
#         "URL": url,
#         "Description": fix["Description"],
#         "Fix Suggestions": fix["Fix"]
#     }

# # Save results to a JSON file
# with open("zap_scan_results.json", "w") as file:
#     json.dump(scan_results, file, indent=4)

# print("Scan results saved to 'zap_scan_results.json'.")
# print("Scan completed successfully!")
from zapv2 import ZAPv2
import requests
from bs4 import BeautifulSoup
import time
import json
import re
import subprocess

# Initialize OWASP ZAP API
zap = ZAPv2(apikey='6ik2gkjo3g2unjvnlfu72qq90s', proxies={'http': 'http://localhost:8080'})

def is_website_reachable(url):
    """Check if the website is reachable using ping."""
    try:
        domain = url.split('//')[-1].split('/')[0]  # Extract domain name
        response = subprocess.run(["ping", "-c", "3", domain], capture_output=True, text=True)
        if "Request timed out" in response.stdout or "could not find host" in response.stdout:
            print("❌ Website is unreachable. Check if it is down or blocking requests.")
            return False
        return True
    except Exception as e:
        print(f"⚠️ Ping test failed: {e}")
        return False

def extract_code(url):
    """Extract HTML & JS code from a webpage with timeout and error handling."""
    try:
        response = requests.get(url, timeout=10)  # 10-second timeout
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        scripts = [script.string for script in soup.find_all("script") if script.string]
        return {"html": soup.prettify(), "js": scripts}
    except requests.exceptions.Timeout:
        print("❌ Connection timed out. The server took too long to respond.")
    except requests.exceptions.ConnectionError:
        print("❌ Failed to connect. The website may be down or blocking requests.")
    except requests.exceptions.HTTPError as err:
        print(f"❌ HTTP Error: {err}")
    return None

# Get target URL
target = input("Enter target URL: ")

# Check website availability
if not is_website_reachable(target):
    print("❌ Exiting scan due to unreachable website.")
    exit()

# Extract website code
print(f"Extracting source code from {target}...")
website_code = extract_code(target)
if not website_code:
    print("❌ Could not extract source code. Exiting scan.")
    exit()

print("✅ Source code extracted successfully!")

# Start Spider Scan
print("Starting spider scan...")
zap.spider.scan(target)
while int(zap.spider.status()) < 100:
    print(f"Spider progress: {zap.spider.status()}%")
    time.sleep(2)
print("Spider scan completed.")

# Start Active Scan
print("Starting active scan...")
scan_id = zap.ascan.scan(target)
while int(zap.ascan.status(scan_id)) < 100:
    print(f"Active scan progress: {zap.ascan.status(scan_id)}%")
    time.sleep(5)
print("Active scan completed!")

# Get scan results
alerts = zap.core.alerts()
print(f"Found {len(alerts)} vulnerabilities.")

def sanitize_filename(url):
    """Sanitize the URL to create a valid filename."""
    return re.sub(r'[\\/*?:"<>|]', "_", url)

# Save results to a JSON file
filename = f"zap_scan_results_{sanitize_filename(target)}.json"
with open(filename, "w") as file:
    json.dump(alerts, file, indent=4)

print(f"✅ Scan results saved to '{filename}'.")
print("🎯 Scan completed successfully!")

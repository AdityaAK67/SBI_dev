import os
import requests
import json
import subprocess
from zapv2 import ZAPv2
import time
from bs4 import BeautifulSoup
import re

# Get API key from environment variable (Set your environment variable for OPENROUTER_API_KEY)
API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise ValueError("OPENROUTER_API_KEY environment variable not set")

API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_ID = "mistralai/Mistral-7B-Instruct"

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

# Send scan results to OpenRouter API for further AI analysis
def get_ai_analysis(alerts):
    """Send vulnerabilities to OpenRouter for AI-based analysis."""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Prepare the message
    message = {
        "model": MODEL_ID,
        "messages": [{"role": "user", "content": f"Analyze the following vulnerabilities: {json.dumps(alerts)}"}]
    }
    
    # Make the API call
    try:
        response = requests.post(API_URL, headers=headers, json=message)
        response.raise_for_status()
        
        ai_response = response.json()
        if ai_response.get("choices"):
            analysis = ai_response["choices"][0]["message"]["content"]
            print(f"AI Analysis: {analysis}")
        else:
            print("❌ No AI response received.")
    except Exception as e:
        print(f"⚠️ Error with OpenRouter API: {e}")

# Get AI analysis for the scan results
get_ai_analysis(alerts)

print("🎯 Scan completed successfully!")

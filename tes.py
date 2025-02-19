import requests

ZAP_BASE_URL = "http://127.0.0.1:8080"

def start_spider_scan(target_url):
    spider_url = f"{ZAP_BASE_URL}/JSON/spider/action/scan/"
    params = {"url": target_url}
    
    try:
        response = requests.get(spider_url, params=params, timeout=10)
        response.raise_for_status()
        print("✅ Spider scan started successfully!")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error starting spider scan: {e}")

target = "https://yuvatech-computers.org.in/"
start_spider_scan(target)

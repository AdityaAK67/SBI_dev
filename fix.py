import requests
import json
import re
import os

# Securely handle API key using environment variables
API_KEY = os.getenv("OPENROUTER_API_KEY")  # ✅ Get from environment
if not API_KEY:
    raise ValueError("OPENROUTER_API_KEY environment variable not set")

API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_ID = "mistralai/Mistral-7B-Instruct"

# Security-enhanced system prompt
SYSTEM_PROMPT = """You are a senior cybersecurity engineer. Fix vulnerabilities following these rules:
1. NEVER use `shell=True` in subprocess calls
2. ALWAYS use parameterized SQL queries
3. NEVER suggest dangerous functions (eval, pickle, marshal)
4. Validate and sanitize ALL inputs
5. Use environment variables for secrets
6. Add security comments
7. Output ONLY the fixed code in a markdown block
8. Never include explanations outside code comments"""
def read_bandit_report(file_path):
    """Reads a Bandit JSON report and extracts vulnerable code snippets."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            bandit_data = json.load(file)

        # Ensure `bandit_data` is a list
        if not isinstance(bandit_data, list):
            print("❌ Error: Unexpected JSON format. Expected a list.")
            return []

        vulnerable_snippets = []
        for result in bandit_data:
            code_lines = result.get("code", "").strip()
            if code_lines:
                vulnerable_snippets.append(code_lines)

        return vulnerable_snippets
    except FileNotFoundError:
        print(f"❌ Error: Bandit report file '{file_path}' not found.")
        return []
    except json.JSONDecodeError:
        print("❌ Error: Invalid JSON format in Bandit report.")
        return []


def extract_code_from_response(response_text):
    """Securely extract code block from markdown response"""
    match = re.search(r'```python\n(.*?)\n```', response_text, re.DOTALL)
    return match.group(1).strip() if match else None

def fix_code(code_snippet):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_ID,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Fix security issues in this code:\n\n{code_snippet}"}
        ],
        "temperature": 0.1,  # Reduced for more deterministic output
        "max_tokens": 1000
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        response_data = response.json()
        
        raw_response = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
        if not raw_response:
            return "❌ Error: Empty response from API"
            
        # Security validation of generated code
        cleaned_code = extract_code_from_response(raw_response)
        if not cleaned_code:
            return "❌ Error: No code block found in response"
            
        # Security checks for common vulnerabilities
        security_checks = [
            (r'subprocess\.(run|call|Popen)\s*\(.*shell\s*=\s*True', "shell=True detected"),
            (r'eval\s*\(', "eval() function detected"),
            (r'os\.system\s*\(', "os.system() detected"),
            (r'pickle\.(load|dump)\s*\(', "Pickle usage detected")
        ]
        
        for pattern, msg in security_checks:
            if re.search(pattern, cleaned_code, re.IGNORECASE):
                return f"❌ Security rejection: {msg} in generated code"
                
        return cleaned_code

    except requests.exceptions.RequestException as e:
        return f"❌ Network error: {str(e)}"
    except (KeyError, IndexError) as e:
        return f"❌ API response parsing error: {str(e)}"
    except json.JSONDecodeError:
        return "❌ Invalid API response format"

# ... (rest of the original functions remain mostly unchanged, but consider adding validation)

def main():
    bandit_report_file = "bandit_report.json"
    vulnerable_codes = read_bandit_report(bandit_report_file)

    if not vulnerable_codes:
        print("✅ No vulnerabilities found!")
        return

    print(f"🔍 Found {len(vulnerable_codes)} vulnerable code snippets. Fixing...\n")
    
    fixed_snippets = []
    for i, code in enumerate(vulnerable_codes, start=1):
        print(f"🔹 Fixing issue {i}...")
        fixed_code = fix_code(code)
        
        if fixed_code.startswith("❌"):
            print(f"⚠️ Failed to fix issue {i}: {fixed_code}")
            fixed_code = f"# Original vulnerable code\n{code}\n\n# Automatic fix failed: {fixed_code}"
            
        print(f"✅ Fixed Code:\n{fixed_code}\n")
        fixed_snippets.append(fixed_code)

    try:
        with open("fixed_code.py", "w", encoding="utf-8") as file:
            file.write("\n\n# ======== SECURITY FIXES ========\n\n".join(fixed_snippets))
        print("\n✅ All fixes saved to 'fixed_code.py'")
    except Exception as e:
        print(f"❌ Error saving fixed code: {e}")
        

if __name__ == "__main__":
    main()
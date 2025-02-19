import subprocess
import json
import time
import os

REPORT_DIR = "reports"
SRC_DIR = "src"

def run_bandit():
    """Run Bandit static analysis on Python code"""
    print(" Running Bandit scan...")
    result = subprocess.run(
        ["bandit", "-r", SRC_DIR, "-f", "json", "-o", f"{REPORT_DIR}/bandit.json"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f" Bandit error: {result.stderr}")

def run_sonarqube():
    """Execute SonarQube scan with custom rules"""
    print("🔍 Running SonarQube analysis...")
    env = os.environ.copy()
    env.update({
        "SONAR_SCANNER_OPTS": "-Xmx512m",
        "SONAR_HOST_URL": "http://localhost:9000",
        "SONAR_LOGIN": "admin",
        "SONAR_PASSWORD": "admin"
    })
    
    result = subprocess.run(
        ["sonar-scanner", 
         "-Dsonar.projectKey=myapp",
         "-Dsonar.sources=.",
         "-Dsonar.python.version=3",
         "-Dsonar.python.bandit.reportPaths=reports/bandit.json"],
        cwd=SRC_DIR,
        env=env
    )
    if result.returncode != 0:
        print(" SonarQube scan failed")

def run_zap(target="http://localhost:8080"):
    """Run OWASP ZAP dynamic analysis"""
    print("⚡ Running ZAP baseline scan...")
    subprocess.run([
        "docker", "run", "--rm",
        "-v", f"{os.getcwd()}/reports:/zap/wrk",
        "-t", "owasp/zap2docker-stable",
        "zap-baseline.py", "-t", target,
        "-J", "zap_results.json"
    ], check=True)

def merge_reports():
    """Combine results from all tools"""
    print("🧩 Merging reports...")
    
    with open(f"{REPORT_DIR}/bandit.json") as f:
        bandit = json.load(f)
    
    with open(f"{REPORT_DIR}/zap_results.json") as f:
        zap = json.load(f)

    merged = {
        "metadata": {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "tools": ["bandit", "sonarqube", "zap"]
        },
        "static_analysis": bandit["results"],
        "dynamic_analysis": zap["site"][0]["alerts"] if zap["site"] else [],
        "metrics": {
            "total_issues": len(bandit["results"]) + len(zap["site"][0]["alerts"]),
            "critical": sum(1 for i in bandit["results"] if i["issue_confidence"] == "HIGH")
        }
    }

    with open(f"{REPORT_DIR}/merged_report.json", "w") as f:
        json.dump(merged, f, indent=2)
    print(f"✅ Merged report saved to {REPORT_DIR}/merged_report.json")

if __name__ == "_main_":
    # Create report directory
    os.makedirs(REPORT_DIR, exist_ok=True)
    
    # Execution sequence
    run_bandit()
    run_sonarqube()
    run_zap()
    time.sleep(10)  # Wait for ZAP to complete
    merge_reports()
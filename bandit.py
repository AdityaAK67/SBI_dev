import subprocess
import json

def run_bandit(target_path, output_file="bandit_report.json"):
    try:
        # Run Bandit and capture output
        result = subprocess.run(
            ["bandit", "-r", target_path, "-f", "json"],
            capture_output=True, text=True
        )

        if not result.stdout.strip():
            print("Error: Bandit output is empty. Ensure the target path is correct.")
            return

        # Parse JSON output
        bandit_output = json.loads(result.stdout)

        # Check if there are errors
        if "errors" in bandit_output and bandit_output["errors"]:
            print("Bandit encountered errors:")
            for error in bandit_output["errors"]:
                print(f"File: {error['filename']}, Reason: {error['reason']}")
            return

        # Extract vulnerabilities
        vulnerabilities = []
        for issue in bandit_output.get("results", []):
            vulnerabilities.append({
                "filename": issue.get("filename"),
                "line_number": issue.get("line_number"),
                "issue": issue.get("issue_text"),
                "severity": issue.get("issue_severity"),
                "confidence": issue.get("issue_confidence"),
                "cwe_id": issue["issue_cwe"]["id"] if "issue_cwe" in issue else "N/A",
                "cwe_link": issue["issue_cwe"]["link"] if "issue_cwe" in issue else "N/A",
                "code": issue.get("code"),
                "more_info": issue.get("more_info"),
            })

        # Write to JSON file
        with open(output_file, "w") as f:
            json.dump(vulnerabilities, f, indent=4)

        print(f"Bandit scan completed. Report saved in {output_file}")

    except json.JSONDecodeError:
        print("Error: Bandit output is not valid JSON. Check for Bandit errors.")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    target = "auth.py"  # Change this to the path of the directory or file you want to scan
    run_bandit(target)

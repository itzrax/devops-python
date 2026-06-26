import json
import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv("project/.env")
token = os.environ.get("GITHUB_TOKEN")
headers = {"Authorization": f"token {token}"}

def check_server(server):

    if server["status"] == "stopped":
        flag = "CRITICAL"
        message = "Server is DOWN"

    elif server["cpu"] > 80:
        flag = "CRITICAL"
        message = f"CPU High: {server['cpu']}%"

    else:
        flag = "OK"
        message = f"CPU: {server['cpu']}%"

    print(f"[{flag}] {server['name']} ({server['ip']}) — {message}")

    return {
        "name": server["name"],
        "ip": server["ip"],
        "status": server["status"],
        "cpu": server["cpu"],
        "flag": flag,
        "message": message
    }


def analyze_logs(logfile):

    failed = {}
    successful = {}
    targeted_users = {}

    with open(logfile, "r") as f:

        for line in f:

            ip = line.split("from")[1].split()[0]

            if "Failed password" in line:
                username = line.split("for")[1].split("from")[0].strip()

                failed[ip] = failed.get(ip, 0) + 1
                targeted_users[username] = targeted_users.get(username, 0) + 1

            elif "Accepted password" in line:
                successful[ip] = successful.get(ip, 0) + 1

    threats = {}

    print("\n── Log Analysis ──")

    for ip, count in failed.items():
        if count > 3:
            print(f"[THREAT] {ip} — {count} failed attempts")
            threats[ip] = count

    return {
        "failed_attempts": failed,
        "successful_logins": successful,
        "targeted_users": targeted_users,
        "threats": threats
    }

def inspect_github_user(username):

    url = f"https://api.github.com/users/{username}"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:

        data = response.json()

        public_repos = data["public_repos"]

        flag = "SUSPICIOUS" if public_repos == 0 else "OK"

        print(f"[OK] {username} — {public_repos} repos")

        return {
            "username": username,
            "name": data["name"],
            "public_repos": public_repos,
            "created_at": data["created_at"],
            "bio": data["bio"],
            "flag": flag
        }

    else:

        print(f"[FLAG] {username} — NOT FOUND")

        return {
            "username": username,
            "status": "NOT FOUND"
        }
    


if __name__ == "__main__":

    print("=" * 50)
    print("     DEVOPS SECURITY MONITOR")
    print("=" * 50)

    print("\n── Server Health ──")

    with open("project/servers.json") as file:
        servers = json.load(file)

    server_results = [check_server(server) for server in servers]

    log_results = analyze_logs("project/auth.log")

    print("\n── GitHub Inspection ──")

    github_users = [
        "torvalds",
        "nonexistentuser99999"
    ]

    github_results = [
        inspect_github_user(user)
        for user in github_users
    ]

    report = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "server_health": server_results,
        "log_analysis": log_results,
        "github_inspection": github_results
    }

    with open("project/report.json", "w") as file:
        json.dump(report, file, indent=4)

    print("\nFull report saved to project/report.json")
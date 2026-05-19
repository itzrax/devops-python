import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv("day-05/.env") 

token = os.environ.get("GITHUB_TOKEN")

if not token:
    print("ERROR: GITHUB_TOKEN not set")
    exit(1)

headers = {"Authorization": f"token {token}"}

users = ["torvalds", "gvanrossum", "nonexistentuser99999"]

def inspect_user(username):
    url = f"https://api.github.com/users/{username}"

    response = requests.get(url, headers=headers)
    print(f"Rate limit remaining: {response.headers.get('X-RateLimit-Remaining')}")

    try:
        response = requests.get(url, headers=headers)
        
    except requests.exceptions.ConnectionError:
        return {"username": username, "status": "ERROR", "flag": "API call failed"}

    if response.status_code == 404:
        return {
            "username": username,
            "status": "NOT FOUND",
            "flag": "User does not exist"
        }

    data = response.json()
    public_repos = data["public_repos"]
    flag = "SUSPICIOUS" if public_repos == 0 else "OK"

    return {
        "username": username,
        "name": data["name"],
        "public_repos": public_repos,
        "created_at": data["created_at"],
        "bio": data["bio"],
        "flag": flag
    }

results = []
for user in users:
    result = inspect_user(user)
    print(result)
    results.append(result)

report = {
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "results": results
}

with open("day-05/report.json", "w") as f:
    json.dump(report, f, indent=4)

print("Secure GitHub report generated!")
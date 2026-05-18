import requests
import json
from datetime import datetime

users= ["torvalds", "gvanrossum", "nonexistentuser99999"]

def inspect_user(username):
    url= f"https://api.github.com/users/{username}"

    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError:
        return {"username": username, "status": "ERROR", "flag": "API call failed"}
    
    if response.status_code ==  404:
        return {
            "username": username,
            "status": "NOT FOUND",
            "flag": "User does not exist"
        }
    
    data = response.json()

    public_repos = data["public_repos"]
    
    flag= "SUSPICIOUS" if public_repos== 0 else "OK"
    
    return {
        "username": username,
        "name": data["name"],
        "public_repos": public_repos,
        "created_at": data["created_at"],
        "bio": data["bio"],
        "flag": flag
    }

results= []
for user in users:
    result= inspect_user(user)
    print(result)
    results.append(result)

report = {
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "results": results
}

with open("day-04/report.json", "w") as f:
    json.dump(report, f, indent=4)

print("Github Inspect report is created")

import json
from datetime import datetime

def check_server(server):
    name = server["name"]
    status = server["status"]
    cpu = server["cpu"]

    if status != "running":
        return {
            "server": name,
            "status": "CRITICAL",
            "message": "Server is DOWN"
        }

    elif cpu > 90:
        return {
            "server": name,
            "status": "CRITICAL",
            "message": f"High CPU usage: {cpu}%"
        }

    else:
        return {
            "server": name,
            "status": "OK",
            "message": f"CPU: {cpu}%"
        }

with open("day-03/servers.json", "r") as f:
    servers = json.load(f)

results = []

for server in servers:
    result = check_server(server)
    results.append(result)

healthy_count = 0
critical_count = 0

for item in results:
    if item["status"] == "OK":
        healthy_count += 1
    else:
        critical_count += 1

report = {
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "summary": {
        "total": len(results),
        "healthy": healthy_count,
        "critical": critical_count
    },
    "results": results
}

with open("day-03/report.json", "w") as f:
    json.dump(report, f, indent=4)

print("Health report generated successfully!")



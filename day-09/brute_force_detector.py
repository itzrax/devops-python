import json
from datetime import datetime 

failed = {}
successful = {}
targeted_users = {}

with open("day-09/auth.log","r") as f:
    for line in f:
        ip = line.split("from")[1].split()[0]

        if "Failed password" in line:
            username                 = line.split("for")[1].split("from")[0].strip()
            failed[ip]               = failed.get(ip,0)+1
            targeted_users[username] = targeted_users.get(username,0)+1

        elif "Accepted password" in line:
            successful[ip] = successful.get(ip,0)+1

print("=== Threat Detection ===")

threat_count = 0

for ip, count in failed.items():
    if count > 3:
        print(f"[THREAT] {ip} - {count} failed attempts")
        threat_count +=1

print("\n Successful logins:")

for ip, count in successful.items():
    print(f" {ip} - {count} successful login")

total_failed= sum(failed.values())
total_successful= sum(successful.values())

print("\n Summary:")
print(f"Total failed attempts: {total_failed}")
print(f"Total successful logins: {total_successful}")
print(f"Threats detected: {threat_count}")

top_user  = max(targeted_users, key=targeted_users.get)
top_count = targeted_users[top_user]

print("\n Most Targeted Username:")
print(f"{top_user} - {top_count} failed attempts")


report = {
    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "failed_attempts": failed,
    "successful_logins": successful,
    "targeted_users": targeted_users,
    "top_targeted_user": {
        "username": top_user,
        "failed_attempts": top_count
    },
    "summary": {
        "total_failed_attempts": total_failed,
        "total_successful_logins": total_successful,
        "threats_detected": threat_count
    }
}

with open("day-09/report.json",'w') as file:
    json.dump(report, file, indent=4)

print("\n report.json has been created successfully")
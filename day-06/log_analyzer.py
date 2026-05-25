import json
from datetime import datetime

counts = {
    "INFO": 0,
    "WARNING": 0,
    "ERROR": 0
}

errors = []

with open("day-06/app.log", "r") as f:
    for line in f:
        parts = line.strip().split(" ", 3)

        date = parts[0]
        time = parts[1]
        level = parts[2]
        message = parts[3]

        timestamp = f"{date} {time}"

        # Update counts
        counts[level] += 1

        # Print ERROR alerts
        if level == "ERROR":
            print(f"[ALERT] {timestamp} — {message}")

            errors.append({
                "timestamp": timestamp,
                "message": message
            })

        # Challenge: Print WARNING alerts containing "high"
        if level == "WARNING" and "high" in message.lower():
            print(f"[WARN] {timestamp} — {message}")

print("\nLog Summary:")
print(f"INFO:    {counts['INFO']}")
print(f"WARNING: {counts['WARNING']}")
print(f"ERROR:   {counts['ERROR']}")

report = {
    "counts": counts,
    "errors": errors
}

with open("day-06/report.json", "w") as f:
    json.dump(report, f, indent=4)

print("\nReport saved to day-06/report.json")



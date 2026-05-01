from datetime import datetime

now = datetime.now()
timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

def check_server(name,status,cpu,ip):
    cpu= int(cpu)
    if status == "stopped":
        return f"[CRITICAL] {name} ({ip}) - Server is DOWN"
    elif cpu>80:
        return f"[CRITICAL] {name} ({ip}) - CPU High: {cpu}%"
    else:
        return f"[OK]       {name} ({ip}) - CPU: {cpu}%"
results=[]

with open("day-02/servers.txt", "r") as f:
    for line in f:
        parts = line.strip().split(",")
        name  = parts[0]
        status= parts[1]
        cpu   = parts[2]
        ip    = parts[3]
        result= check_server(name,status,cpu,ip)
        results.append(result)


with open("day-02/report.txt", "w") as f:
    f.write(f"Health Check Report — {timestamp}\n")
    f.write("=" * 42 + "\n")

    for result in results:
        f.write(result + "\n")

    total = len(results)
    healthy = sum(1 for r in results if "[OK]" in r)

    f.write(f"\nSummary: {healthy}/{total} servers healthy\n")
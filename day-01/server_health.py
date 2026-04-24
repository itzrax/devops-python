servers = [
    {"name": "prod-web-01", "status": "running", "cpu": 45, "ip": "10.0.1.1" },
    {"name": "prod-web-02", "status": "stopped", "cpu": 0, "ip": "10.0.1.17"},
    {"name": "prod-web-03", "status": "running", "cpu": 91, "ip": "10.0.1.2"},
    {"name": "prod-web-04", "status": "running", "cpu": 33 , "ip": "10.0.1.22"},
    {"name": "prod-web-05", "status": "running", "cpu": 95 , "ip": "10.0.1.4"},
]

def check_server(server):
   if server["status"]== "stopped":
       return f"[CRITICAL] {server['name']} ({server['ip']}) — Server is DOWN"
   elif server["cpu"]>80:
       return f"[CRITICAL] {server['name']} ({server['ip']})  —  CPU HIGH: {server['cpu']}%"
   else:
       return f"[OK] {server['name']} ({server['ip']}) — CPU: {server['cpu']}%"


healthy = 0

for server in servers:
    result = check_server(server)
    print(result)
    if "[OK]" in result:
        healthy += 1 

print(f"Summary: {healthy}/{len(servers)} servers healthy")
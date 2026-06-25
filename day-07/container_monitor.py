import docker
import json
from datetime import datetime

client = docker.from_env()

def get_container_info(container):
    return{
        "name"      : container.name,
        "status"    : container.status,
        "image"     : container.image.tags,
        "id"        : container.short_id,
        "started_at": container.attrs["State"]["StartedAt"],
    }

containers = client.containers.list()

if not containers:
    print("No running containers found")
else:
    results = []
    for container in containers:
        info = get_container_info(container)
        print(f"[{info['status'].upper()}] {info['name']} - {info['image']}")
        results.append(info)

    report = {
        "timestamp"  : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "containers" : results
    }

    with open("day-07/report.json", "w") as f:
        json.dump(report, f, indent=4)

    print("\nReport saved to day-07/report.json")




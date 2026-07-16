import random
from datetime import datetime, timedelta

levels = ["INFO", "WARNING", "ERROR"]
messages = {
    "INFO": [
        "User logged in", "Request processed", "Cache cleared",
        "Backup started", "Service restarted", "Connection established",
    ],
    "WARNING": [
        "Disk usage high", "Memory usage high", "CPU temperature high",
        "Retry attempt failed", "Slow response time",
    ],
    "ERROR": [
        "Database connection lost", "Permission denied", "Timeout on API",
        "NullPointerException", "Service crashed", "Failed to write to disk",
    ],
}

start = datetime(2024, 1, 15, 0, 0, 0)
lines = []

for i in range(1000):
    ts = start + timedelta(seconds=random.randint(0, 86400))
    level = random.choices(levels, weights=[60, 25, 15])[0]
    msg = random.choice(messages[level])
    lines.append(f"{ts.strftime('%Y-%m-%d %H:%M:%S')} {level} {msg}")

lines.sort()

with open("samples/large.log", "w") as f:
    f.write("\n".join(lines))

print(f"Generated {len(lines)} log lines → samples/large.log")

import os

print("=== ENVIRONMENT VARIABLES ===")

for key in sorted(os.environ.keys()):
    if "PG" in key or "DB" in key or "LAKE" in key:
        print(key, "=", os.environ[key])

raise Exception("Stopped for environment check")

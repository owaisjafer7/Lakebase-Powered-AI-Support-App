import os

def show_environment():
    return [
        key
        for key in sorted(os.environ.keys())
        if "PG" in key or "DB" in key or "DATABASE" in key
    ]

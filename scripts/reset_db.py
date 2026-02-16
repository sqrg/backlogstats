"""Reset the database: drop all tables and recreate them via Alembic."""

import os
import subprocess
from pathlib import Path

# Always run from the project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
os.chdir(PROJECT_ROOT)

DB_FILE = PROJECT_ROOT / "backlogstats.db"

if DB_FILE.exists():
    DB_FILE.unlink()
    print(f"Deleted {DB_FILE.name}")
else:
    print(f"{DB_FILE.name} not found, skipping delete")

print("Running alembic upgrade head...")
subprocess.run(["alembic", "upgrade", "head"], check=True)
print("Database reset complete!")

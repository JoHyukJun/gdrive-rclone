import os
import subprocess

from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent
RCLONE = BASE_DIR / 'rclone/rclone.exe'

print(RCLONE)

subprocess.run([RCLONE, 'ls'], shell=True)
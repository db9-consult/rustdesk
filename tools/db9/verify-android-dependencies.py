import json
import os
from pathlib import Path
import re
import subprocess

repository = os.environ["GITHUB_REPOSITORY"]
run = os.environ["BUILD_RUN"]
jobs = json.loads(subprocess.check_output(["gh", "api", f"repos/{repository}/actions/runs/{run}/jobs"], text=True))["jobs"]
job = next(job for job in jobs if job["name"] == "build")
for step in ["Build signed APK", "Build Rust library"]:
    if not any(item["name"] == step and item["conclusion"] == "success" for item in job["steps"]):
        raise ValueError(f"Original build did not complete {step}")
log = subprocess.check_output(["gh", "run", "view", run, "--repo", repository, "--job", str(job["id"]), "--log"], text=True)
expected = {}
for line in log.splitlines():
    fields = line.split("\t", 2)
    if len(fields) != 3 or fields[1] != "Build signed APK":
        continue
    message = re.sub(r"\x1b\[[0-9;]*m", "", fields[2]).split(" ", 1)[-1]
    match = re.match(r"^[!+<> ]*([a-z][a-z0-9_]*) (\d+\.\d+\.\d+(?:[-+][a-zA-Z0-9.]+)?)\b", message)
    if match:
        expected[match[1]] = match[2]
if not expected:
    raise ValueError("Could not recover original Flutter dependency versions")
resolved = json.loads(Path("source/output/android-dependencies.json").read_text())
actual = {package["name"]: package["version"] for package in resolved["packages"]}
for name, version in expected.items():
    if actual.get(name) != version:
        raise ValueError(f"Dependency changed since original build: {name} {version} -> {actual.get(name)}")
print(f"Confirmed {len(expected)} dependency versions against the original Android build log.")

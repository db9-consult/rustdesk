import hashlib
import json
import os
import pathlib
import subprocess
import tarfile

root = pathlib.Path(__file__).resolve().parents[2]
output = root / "output"
windows_output = output / "SignOutput"
if windows_output.is_dir():
    for path in windows_output.iterdir():
        if path.is_file():
            destination = output / path.name
            if destination.exists():
                raise RuntimeError(f"Duplicate release file: {path.name}")
            path.rename(destination)
expected = [
    "rustdesk-db9-1.5.0-x86_64.exe",
    "rustdesk-db9-1.5.0-x86_64.msi",
    "rustdesk-db9-1.5.0-x86_64.dmg",
    "rustdesk-db9-1.5.0-aarch64.dmg",
]
for name in expected:
    path = output / name
    if not path.is_file() or path.stat().st_size == 0:
        raise RuntimeError(f"Missing or empty package: {name}")

def git(*args, cwd=root):
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()

metadata = {
    "upstream_version": "1.5.0",
    "upstream_commit": "fada664df7a294d1d1a9ca3e7cd3637069122f17",
    "fork_commit": git("rev-parse", "HEAD"),
    "hbb_common_commit": git("rev-parse", "HEAD", cwd=root / "libs/hbb_common"),
    "release": "1.5.0-db9.1",
    "id_server": "rustdesk.db9consult.com.br",
    "relay_server": "rustdesk.db9consult.com.br",
    "key": "dksPMYTN32cCIMoIhBsKh5MZzYIAYt70xQxIiYZqSiQ=",
    "commercially_signed": False,
    "apple_notarized": False,
    "workflow_run": f"https://github.com/{os.environ['GITHUB_REPOSITORY']}/actions/runs/{os.environ['GITHUB_RUN_ID']}",
}
(output / "build-metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
source = output / "rustdesk-db9-1.5.0-source.tar.gz"
with tarfile.open(source, "w:gz") as archive:
    for directory in (root, root / "libs/hbb_common"):
        for name in git("ls-files", cwd=directory).splitlines():
            path = directory / name
            if path.is_file():
                archive.add(path, arcname=str(path.relative_to(root)), recursive=False)
(output / "INSTALLATION.md").write_text((root / "tools/db9/release-notes.md").read_text(encoding="utf-8"), encoding="utf-8")
with (output / "SHA256SUMS.txt").open("w", encoding="utf-8") as manifest:
    for path in sorted(output.iterdir()):
        if path.is_file() and path.name != "SHA256SUMS.txt":
            digest = hashlib.sha256()
            with path.open("rb") as content:
                for chunk in iter(lambda: content.read(1024 * 1024), b""):
                    digest.update(chunk)
            manifest.write(f"{digest.hexdigest()}  {path.name}\n")
print(json.dumps(metadata, indent=2))

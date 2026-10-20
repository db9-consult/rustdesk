import hashlib
import json
import os
from pathlib import Path
import re
import struct
import subprocess
import tarfile
import zipfile

root = Path(__file__).resolve().parents[2]
output = root / "output"
apk = output / "rustdesk-db9-1.5.0-aarch64.apk"
certificate = "3334cdf00b267487cc5f3565bf601954485d55a7830478e08244246405a1e9b7"
signature = (output / "db9-android-signature.txt").read_text()
signers = {
    digest.lower()
    for digest in re.findall(r"^(?:V[0-9.]+ Signer:|Signer[^\r\n]*) certificate SHA-256 digest:\s*([0-9a-fA-F]{64})\s*$", signature, re.MULTILINE)
}
if signers != {certificate}:
    raise ValueError(f"Expected permanent DB9 certificate {certificate}; found {sorted(signers)}")
badging = (output / "db9-android-package.txt").read_text()
for expected in ["package: name='com.db9consult.rustdesk'", "versionName='1.5.0'", "native-code: 'arm64-v8a'", "application-label:'RustDesk DB9'"]:
    if expected not in badging:
        raise ValueError(f"APK metadata mismatch: {expected}")
with zipfile.ZipFile(apk) as archive:
    libraries = [name for name in archive.namelist() if name.startswith("lib/") and name.endswith(".so")]
    if not libraries or any(not name.startswith("lib/arm64-v8a/") for name in libraries):
        raise ValueError("APK must contain only ARM64 native libraries")
    library = archive.read("lib/arm64-v8a/librustdesk.so")
    if library[:6] != b"\x7fELF\x02\x01" or struct.unpack_from("<H", library, 18)[0] != 183:
        raise ValueError("RustDesk library is not AArch64 ELF")
    for value in [b"rustdesk.db9consult.com.br", b"dksPMYTN32cCIMoIhBsKh5MZzYIAYt70xQxIiYZqSiQ="]:
        if value not in library:
            raise ValueError("Missing embedded DB9 server configuration")

def git(*args, cwd=root):
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()

metadata = {
    "upstream_version": "1.5.0",
    "desktop_release_source": "db108f7906ce13e9957a0a67f93c328afd3d4792",
    "fork_commit": git("rev-parse", "HEAD"),
    "packaging_commit": os.environ.get("DB9_ANDROID_PACKAGING_COMMIT", git("rev-parse", "HEAD")),
    "hbb_common_commit": git("rev-parse", "HEAD", cwd=root / "libs/hbb_common"),
    "application_id": "com.db9consult.rustdesk",
    "abi": "arm64-v8a",
    "signing_certificate_sha256": certificate,
    "id_server": "rustdesk.db9consult.com.br",
    "relay_server": "rustdesk.db9consult.com.br",
    "key": "dksPMYTN32cCIMoIhBsKh5MZzYIAYt70xQxIiYZqSiQ=",
    "workflow_run": f"https://github.com/{os.environ['GITHUB_REPOSITORY']}/actions/runs/{os.environ.get('DB9_ANDROID_BUILD_RUN', os.environ['GITHUB_RUN_ID'])}",
    "validation_run": f"https://github.com/{os.environ['GITHUB_REPOSITORY']}/actions/runs/{os.environ['GITHUB_RUN_ID']}",
    "device_validation": "Pending: no authorized Android ARM64 device attached to the build runner.",
}
(output / "android-build-metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
(output / "ANDROID-INSTALLATION.md").write_text((root / "tools/db9/android-installation.md").read_text(encoding="utf-8"), encoding="utf-8")
with tarfile.open(output / "rustdesk-db9-1.5.0-android-source.tar.gz", "w:gz") as archive:
    for directory in [root, root / "libs/hbb_common"]:
        files = set(git("ls-files", cwd=directory).splitlines())
        if directory == root:
            files.update(["flutter/lib/generated_bridge.dart", "flutter/lib/generated_bridge.freezed.dart", "src/bridge_generated.rs", "src/bridge_generated.io.rs", "flutter/pubspec.lock"])
        for name in sorted(files):
            path = directory / name
            if path.is_file():
                archive.add(path, arcname=path.relative_to(root), recursive=False)
with (output / "ANDROID-SHA256SUMS.txt").open("w", encoding="utf-8") as checksums:
    for path in sorted(output.iterdir()):
        if path.is_file() and path.name != "ANDROID-SHA256SUMS.txt":
            with path.open("rb") as content:
                digest = hashlib.file_digest(content, "sha256").hexdigest()
            checksums.write(f"{digest}  {path.name}\n")
print(json.dumps(metadata, indent=2))

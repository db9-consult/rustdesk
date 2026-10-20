import base64
import os
from pathlib import Path

root = Path(__file__).resolve().parents[2]
android = root / "flutter/android"
keystore = base64.b64decode(os.environ["DB9_ANDROID_KEYSTORE"], validate=True)
password = os.environ["DB9_ANDROID_KEYSTORE_PASSWORD"]
if not password or "\n" in password or "\r" in password:
    raise ValueError("Invalid signing password")
(android / "db9-android.p12").write_bytes(keystore)
(android / "key.properties").write_text(
    f"storeFile={android / 'db9-android.p12'}\n"
    f"storePassword={password}\nkeyPassword={password}\nkeyAlias=db9-android\n",
    encoding="utf-8",
)

gradle = android / "app/build.gradle"
source = gradle.read_text(encoding="utf-8")
old_id = 'applicationId "com.carriez.flutter_hbb"'
if source.count(old_id) != 1:
    raise ValueError("Expected upstream Android application ID")
gradle.write_text(source.replace(old_id, 'applicationId "com.db9consult.rustdesk"'), encoding="utf-8")
manifest = android / "app/src/main/AndroidManifest.xml"
source = manifest.read_text(encoding="utf-8")
if 'android:label="RustDesk"' not in source:
    raise ValueError("Expected upstream Android application label")
manifest.write_text(source.replace('android:label="RustDesk"', 'android:label="RustDesk DB9"'), encoding="utf-8")
properties = android / "gradle.properties"
properties.write_text(properties.read_text(encoding="utf-8").replace("-Xmx1024M", "-Xmx4g"), encoding="utf-8")
print("DB9 application ID and persistent release signing configured.")

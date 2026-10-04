#!/usr/bin/env bash
set -euo pipefail
dmg=$1
arch=$2
report="db9-macos-validation-${arch}.txt"
mount_dir=$(mktemp -d)
cleanup() {
  hdiutil detach "$mount_dir" || true
  rmdir "$mount_dir" || true
}
trap cleanup EXIT
hdiutil verify "$dmg"
hdiutil attach "$dmg" -readonly -nobrowse -mountpoint "$mount_dir"
app="$mount_dir/RustDesk.app"
expected=$arch
if [[ "$arch" == aarch64 ]]; then expected=arm64; fi
file "$app/Contents/MacOS/RustDesk" | tee "$report"
lipo -verify_arch "$expected" "$app/Contents/MacOS/RustDesk"
lipo -verify_arch "$expected" "$app/Contents/Frameworks/liblibrustdesk.dylib"
codesign --verify --deep --strict --verbose=2 "$app"
printf 'PASS: DMG integrity, mounting, %s architecture and ad hoc signature.\n' "$expected" >> "$report"
printf 'NOT TESTED: interactive GUI, macOS accessibility/screen-recording approval and remote relay session.\n' >> "$report"

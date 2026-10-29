#!/usr/bin/env python3
"""Apply the reviewed PotuzhnoGram patch to its pinned Android source."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import time

ROOT = Path(__file__).resolve().parent
CLIENT = ROOT / "client"

def git(*args, check=True):
    return subprocess.run(["git", "-C", str(CLIENT), *args], check=check,
                          text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def normalize_patch_lines():
    """Preserve original bytes, then normalize CRLF in patch-targeted text files."""
    patches = [ROOT / "patches" / name for name in
               ("potuzhno.patch", "upgrade-12.10.6.patch", "upgrade-v2.patch", "upgrade-v3.patch")]
    paths = set(patches)
    for patch in patches:
        for line in patch.read_text(encoding="utf-8").splitlines():
            if line.startswith("+++ b/"):
                paths.add(CLIENT / line[6:])
    changed = [p for p in sorted(paths) if p.is_file() and b"\r\n" in p.read_bytes()]
    if not changed:
        return
    backups = Path.home() / ".cache/potuznogram/line-ending-backups"
    backups.mkdir(parents=True, exist_ok=True)
    backup = backups / (str(time.time_ns()) + ".tar.gz")
    with tarfile.open(backup, "w:gz") as archive:
        for path in changed:
            archive.add(path, arcname=str(path.relative_to(ROOT)))
    for path in changed:
        path.write_bytes(path.read_bytes().replace(b"\r\n", b"\n"))
    print("Normalized Windows line endings; original files saved to " + str(backup))

def prepare(init=False):
    if not (CLIENT / "gradlew").exists():
        if not init:
            raise RuntimeError("Missing client source. Run: git submodule update --init --recursive --depth=1")
        if (ROOT / ".git").exists():
            subprocess.run(["git", "submodule", "update", "--init", "--recursive", "--depth=1"],
                           cwd=ROOT, check=True)
        else:
            # ZIP delivery: fetch exactly the same pinned source without a parent Git checkout.
            source = json.loads((ROOT / "upstream.json").read_text())
            if CLIENT.exists() and any(CLIENT.iterdir()):
                raise RuntimeError("client exists but is incomplete; inspect it before retrying.")
            CLIENT.mkdir(exist_ok=True)
            git("init")
            git("remote", "add", "origin", source["repository"])
            git("fetch", "--depth=1", "origin", source["commit"])
            git("checkout", "--detach", source["commit"])
            git("submodule", "update", "--init", "--recursive", "--depth=1")
    expected = json.loads((ROOT / "upstream.json").read_text())["commit"]
    if git("rev-parse", "HEAD").stdout.strip() != expected:
        raise RuntimeError("client is not at the pinned commit; refusing to change a different version.")
    normalize_patch_lines()
    patch = str(ROOT / "patches/potuzhno.patch")
    if git("apply", "--reverse", "--check", patch, check=False).returncode == 0:
        print("Branding patch already applied.")
    elif git("apply", "--check", patch, check=False).returncode == 0:
        git("apply", patch)
        print("Applied branding patch.")
    elif git("apply", "--check", str(ROOT / "patches/upgrade-12.10.6.patch"), check=False).returncode == 0:
        git("apply", str(ROOT / "patches/upgrade-12.10.6.patch"))
        print("Upgraded existing 12.10.6 branding.")
    elif git("apply", "--check", str(ROOT / "patches/upgrade-v2.patch"), check=False).returncode == 0:
        git("apply", str(ROOT / "patches/upgrade-v2.patch"))
        print("Upgraded theme contrast and icon branding.")
    elif git("apply", "--check", str(ROOT / "patches/upgrade-v3.patch"), check=False).returncode == 0:
        git("apply", str(ROOT / "patches/upgrade-v3.patch"))
        print("Upgraded wallpaper and PotuzhnoMeter.")
    else:
        raise RuntimeError("Source has conflicting edits. Preserve your work and inspect git -C client diff; no reset was performed.")
    # Fail before overwriting user-edited overlay assets.
    manifest = json.loads((ROOT / "assets.sha256.json").read_text())
    previous = json.loads((ROOT / "patches/previous/assets.sha256.json").read_text())
    v3 = json.loads((ROOT / "patches/previous/v3-assets.sha256.json").read_text())
    v2 = json.loads((ROOT / "patches/previous/v2-assets.sha256.json").read_text())
    palette = json.loads((ROOT / "patches/previous/palette-assets.sha256.json").read_text())
    for relative, expected_hash in manifest.items():
        origin = ROOT / "overlay" / relative
        if hashlib.sha256(origin.read_bytes()).hexdigest() != expected_hash:
            raise RuntimeError("Asset checksum mismatch: " + relative)
        dest = CLIENT / relative
        if dest.exists() and dest.read_bytes() != origin.read_bytes() and hashlib.sha256(dest.read_bytes()).hexdigest() not in (previous.get(relative), palette.get(relative), v2.get(relative), v3.get(relative)):
            raise RuntimeError("Existing asset differs; preserve it before replacing: " + str(dest))
    for relative in manifest:
        dest = CLIENT / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / "overlay" / relative, dest)
    for relative in previous.keys() - manifest.keys():
        dest = CLIENT / relative
        if dest.exists() and hashlib.sha256(dest.read_bytes()).hexdigest() == previous[relative]:
            dest.unlink()
    # Remove only the known upstream Firebase configuration, never a user's file.
    firebase = CLIENT / "TMessagesProj/google-services.json"
    original = subprocess.run(["git", "-C", str(CLIENT), "show", "HEAD:TMessagesProj/google-services.json"],
                              check=True, stdout=subprocess.PIPE).stdout
    if firebase.exists() and firebase.read_bytes() == original:
        firebase.unlink()
    for name, target in [("local.properties", "local.properties"),
                         ("google-services.json", "TMessagesProj/google-services.json")]:
        origin, dest = ROOT / name, CLIENT / target
        if origin.exists():
            if dest.exists() and dest.read_bytes() != origin.read_bytes():
                raise RuntimeError("Configuration differs at " + str(dest) + "; resolve it manually.")
            shutil.copyfile(origin, dest)
    print("Ready for Android Studio: " + str(CLIENT))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--init", action="store_true", help="Initialize the pinned source and its submodules")
    args = parser.parse_args()
    try:
        prepare(args.init)
    except (RuntimeError, subprocess.CalledProcessError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)

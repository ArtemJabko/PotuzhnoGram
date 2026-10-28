#!/usr/bin/env python3
"""Local APK build; never uploads source, credentials, or artifacts."""
import argparse
import os
import re
import subprocess
import sys
from prepare import CLIENT, prepare

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--release", action="store_true")
    parser.add_argument("--abi", choices=["arm64-v8a", "x86_64", "universal"], default="arm64-v8a")
    parser.add_argument("--init", action="store_true")
    args = parser.parse_args()
    prepare(args.init)
    config = CLIENT / "local.properties"
    values = dict(re.findall(r"^\s*([A-Z_]+)\s*=\s*(.*?)\s*$",
                            config.read_text() if config.exists() else "", re.M))
    app_id = values.get("TELEGRAM_APP_ID") or os.environ.get("TELEGRAM_APP_ID", "")
    app_hash = values.get("TELEGRAM_APP_HASH") or os.environ.get("TELEGRAM_APP_HASH", "")
    if not re.fullmatch(r"[1-9][0-9]*", app_id) or not re.fullmatch(r"[a-fA-F0-9]{32}", app_hash):
        raise RuntimeError("Set your TELEGRAM_APP_ID and TELEGRAM_APP_HASH in local.properties. See README.")
    version = subprocess.run(["java", "-version"], capture_output=True, text=True, check=True)
    if not re.search(r'version "21[."]', version.stderr + version.stdout):
        raise RuntimeError("This source requires JDK 21. Set JAVA_HOME and PATH to JDK 21.")
    env = dict(os.environ, NATIVE_TARGET=args.abi)
    task = ":TMessagesProj:assembleRelease" if args.release else ":TMessagesProj:assembleDebug"
    command = ["cmd", "/c", "gradlew.bat", task] if os.name == "nt" else ["bash", "./gradlew", task]
    subprocess.run(command, cwd=CLIENT, env=env, check=True)
    print("APK output: " + str(CLIENT / "TMessagesProj/build/outputs/apk"))

if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, subprocess.CalledProcessError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)

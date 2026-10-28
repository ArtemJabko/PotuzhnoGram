"""Host checks. Does not claim Android compilation or on-device validation."""
from pathlib import Path
import hashlib
import importlib.util
import json
import subprocess
import sys
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[1]
subprocess.run([sys.executable, str(root / "prepare.py")], check=True)
subprocess.run([sys.executable, str(root / "prepare.py")], check=True)
for path in (root / "overlay").rglob("*.xml"):
    ET.parse(path)
for relative, expected in json.loads((root / "assets.sha256.json").read_text()).items():
    assert hashlib.sha256((root / "overlay" / relative).read_bytes()).hexdigest() == expected
sys.path.insert(0, str(root / "client/TMessagesProj/src/main/python"))
spec = importlib.util.spec_from_file_location("hello", root / "examples/potuzhno_hello.py")
plugin = importlib.util.module_from_spec(spec)
spec.loader.exec_module(plugin)
assert plugin.PotuzhnoHello().create_settings()[0].text.startswith("ПотужноGram")
for path in (root / "overlay/TMessagesProj/src/main/assets").glob("*.attheme"):
    header, wallpaper = path.read_bytes().split(b"WPS\n", 1)
    assert wallpaper.startswith(b"\xff\xd8") and wallpaper.endswith(b"\xff\xd9\nWPE\n")
    for line in header.decode().splitlines():
        key, value = line.split("=")
        assert -(2**31) <= int(value) < 2**31, key
subprocess.run(["git", "-C", str(root / "client"), "diff", "--check"], check=True)
print("PASS: repeat preparation, XML, asset hashes, theme payloads, plugin SDK smoke check, patch whitespace")

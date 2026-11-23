#!/usr/bin/env python3
"""Sync the raw config files from hafrey1/LunaTV-config into media/LunaTV/.

Mirrors these six upstream files verbatim so users have a stable backup/raw
copy alongside the converted subscriptions:

    LunaTV-config.json / .txt
    jin18.json / .txt
    jingjian.json / .txt

Run daily by .github/workflows/update.yml.
"""

import os
import sys
import urllib.request

BASE = (
    "https://raw.githubusercontent.com/hafrey1/LunaTV-config/"
    "refs/heads/main/"
)
FILES = [
    "LunaTV-config.json",
    "LunaTV-config.txt",
    "jin18.json",
    "jin18.txt",
    "jingjian.json",
    "jingjian.txt",
]
UA = "Mozilla/5.0 (compatible; config-sync/1.0)"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "media", "LunaTV")


def fetch(name):
    req = urllib.request.Request(BASE + name, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    ok = 0
    for name in FILES:
        try:
            data = fetch(name)
        except Exception as exc:
            print(f"WARN {name}: 下载失败 {exc}", file=sys.stderr)
            continue
        if not data or len(data) < 20:
            print(f"WARN {name}: 内容异常({len(data)} bytes)，跳过", file=sys.stderr)
            continue
        path = os.path.join(OUT_DIR, name)
        with open(path, "wb") as f:
            f.write(data)
        print(f"synced {name} ({len(data)} bytes)")
        ok += 1
    if ok == 0:
        print("致命错误：没有任何上游文件同步成功", file=sys.stderr)
        sys.exit(1)
    print(f"done: {ok}/{len(FILES)} files")


if __name__ == "__main__":
    main()

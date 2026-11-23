#!/usr/bin/env python3
"""Discover media CDN domains behind the LunaTV-config sources and emit a
Clash/Mihomo rule-set in YAML format.

For each upstream site we fetch one title's detail, extract its m3u8/mp4 URLs,
then recursively follow m3u8 playlists (master -> variant -> segments) to
collect every host involved in playback. Domains are emitted as DOMAIN-SUFFIX
rules so Clash can route them (typically DIRECT) in one place.

YAML is intentionally chosen over .mrs: it is human-readable, easy to grep and
maintain, and needs no extra binary in CI. Mihomo accepts YAML rule-sets via
`type: yaml` rule providers.

Only a few titles per site are sampled to keep the daily job fast and polite.
"""

import json
import os
import re
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from urllib.parse import urljoin, urlparse

from generate import UPSTREAM_URL, fetch_json, strip_proxy  # reuse upstream loader bits

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "media", "media-domains.yaml")

SAMPLES_PER_SITE = 3      # how many titles to inspect per site
PLAYLIST_DEPTH = 3        # master -> variant -> segments
FETCH_TIMEOUT = 8
URL_RE = re.compile(r"https?://[^\s\"'<>\\]+")


def http_get(url, timeout=FETCH_TIMEOUT, max_bytes=4 * 1024 * 1024):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read(max_bytes).decode("utf-8", "ignore")
    except Exception:
        return ""


def host_of(url):
    try:
        return urlparse(url).hostname
    except Exception:
        return None


def valid_host(host):
    if not host or len(host) > 253:
        return False
    if host.startswith(".") or host.endswith("."):
        return False
    # must look like a domain with a TLD, skip raw IPs and localhost
    if re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", host):
        return False
    if "." not in host or host.lower() in ("localhost",):
        return False
    return True


def collect_from_playlist(url, depth, seen, hosts):
    if depth > PLAYLIST_DEPTH or url in seen:
        return
    seen.add(url)
    text = http_get(url)
    if not text:
        return
    # absolute URLs mentioned anywhere
    for m in URL_RE.findall(text):
        h = host_of(m)
        if valid_host(h):
            hosts.add(h.lower())
    # relative/absolute entries: resolve against playlist URL
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        full = urljoin(url, line.split(",")[0].strip())
        h = host_of(full)
        if valid_host(h):
            hosts.add(h.lower())
        if ".m3u8" in full.lower():
            collect_from_playlist(full, depth + 1, seen, hosts)


def extract_play_urls(detail_list):
    urls = []
    for vod in detail_list:
        raw = str(vod.get("vod_play_url", "") or "")
        if not raw:
            continue
        # lines separated by $$$, episodes by #, name$url
        for line in raw.split("$$$")[:2]:
            for ep in line.split("#")[:2]:
                u = ep.split("$")[-1].strip()
                if u.startswith("http"):
                    urls.append(u)
    return urls


def probe_site(site):
    api = site["api"]
    hosts = set()
    listing = http_get(api + "?ac=detail&pg=1", timeout=FETCH_TIMEOUT)
    if not listing:
        return hosts
    try:
        data = json.loads(listing)
    except Exception:
        return hosts
    rows = data.get("list", [])[:SAMPLES_PER_SITE]
    for row in rows:
        vid = row.get("vod_id")
        if vid is None:
            continue
        det = http_get(api + "?ac=detail&ids=" + str(vid), timeout=FETCH_TIMEOUT)
        if not det:
            continue
        try:
            d = json.loads(det)
        except Exception:
            continue
        play_urls = extract_play_urls(d.get("list", []))
        for u in play_urls[:3]:
            h = host_of(u)
            if valid_host(h):
                hosts.add(h.lower())
            if ".m3u8" in u.lower():
                collect_from_playlist(u, 0, set(), hosts)
            elif ".mp4" in u.lower():
                # single file: only the host matters
                pass
    return hosts


def load_sites():
    data = fetch_json(UPSTREAM_URL)
    sites = data.get("api_site", {})
    out = []
    seen = set()
    for key, meta in sites.items():
        api = strip_proxy(str(meta.get("api", "")))
        if not api or api in seen:
            continue
        seen.add(api)
        out.append({"name": str(meta.get("name", key)), "api": api})
    return out


def main():
    sites = load_sites()
    # Incremental: keep every domain already in the file, only ever add new ones.
    existing = set()
    if os.path.exists(OUT):
        for line in open(OUT, encoding="utf-8"):
            m = re.match(r"\s*-\s+'([^']+)'", line)
            if m:
                existing.add(m.group(1).strip().lower())
    print(f"existing domains in rule file: {len(existing)}")

    print(f"probing {len(sites)} sites (up to {SAMPLES_PER_SITE} titles each)")
    all_hosts = set(existing)          # seed with history so nothing is ever dropped
    new_hosts = set()
    with ThreadPoolExecutor(max_workers=12) as ex:
        futures = {ex.submit(probe_site, s): s for s in sites}
        done = 0
        for fut in as_completed(futures):
            s = futures[fut]
            done += 1
            try:
                hs = fut.result()
            except Exception:
                hs = set()
            if hs:
                fresh = hs - existing
                new_hosts |= fresh
                all_hosts |= hs
            if done % 10 == 0:
                print(f"  probed {done}/{len(sites)} ... new domains so far {len(new_hosts)}")

    domains = sorted(all_hosts)
    print(f"new domains added this run: {len(new_hosts)}" + (f" -> {sorted(new_hosts)[:10]}" if new_hosts else ""))
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Media playback CDN domains collected from LunaTV-config sources.",
        "# Incremental: domains are only ever added, never removed.",
        "# Maintained weekly by .github/workflows/update-media-rules.yml",
        f"# Generated: {stamp}",
        f"# Total: {len(domains)} domains",
        "#",
        "# Usage (Mihomo/Clash rule provider):",
        "#   rule_providers:",
        "#     media:",
        "#       type: http",
        "#       format: yaml",
        "#       behavior: domain",
        "#       url: https://raw.githubusercontent.com/summerscar/config/refs/heads/main/media/media-domains.yaml",
        "#       path: ./rule_sets/media.yaml",
        "#       interval: 86400",
        "# Then add rule: RULE-SET(media, DIRECT)",
        "payload:",
    ]
    lines += [f"  - '{d}'" for d in domains]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"wrote {OUT} ({len(domains)} domains)")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"generate media rules failed: {exc}", file=sys.stderr)
        sys.exit(1)

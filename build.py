#!/usr/bin/env python3
"""Cut one PMTiles file per area out of the newest Protomaps basemap build.

Writes site/<id>-<build>.pmtiles and site/index.json (the file the Gyrano app reads).
Env:
  BUILD     Protomaps build date YYYYMMDD (blank = newest found in the last 14 days)
  PMTILES   pmtiles CLI (default: pmtiles)
  SOURCE    URL template for a build (default: https://build.protomaps.com/{build}.pmtiles)
  OUT       output folder (default: site)
"""
import datetime as dt
import hashlib
import json
import os
import subprocess
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.environ.get("SOURCE") or "https://build.protomaps.com/{build}.pmtiles"
PMTILES = os.environ.get("PMTILES") or "pmtiles"
OUT = os.environ.get("OUT") or "site"


def exists(url):
    req = urllib.request.Request(url, headers={"Range": "bytes=0-0", "User-Agent": "gyrano-maps-build"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status in (200, 206)
    except Exception:
        return False


def newest_build():
    today = dt.datetime.now(dt.timezone.utc).date()
    for back in range(14):
        b = (today - dt.timedelta(days=back)).strftime("%Y%m%d")
        if exists(SOURCE.format(build=b)):
            return b
    sys.exit("No Protomaps build found in the last 14 days")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    with open(os.path.join(HERE, "areas.json")) as f:
        cfg = json.load(f)
    maxzoom = int(cfg["maxzoom"])
    build = (os.environ.get("BUILD") or "").strip() or newest_build()
    if not (len(build) == 8 and build.isdigit()):
        sys.exit(f"Bad build id: {build!r}")
    src = SOURCE.format(build=build)
    print(f"Build {build} from {src}, maxzoom {maxzoom}", flush=True)
    os.makedirs(OUT, exist_ok=True)

    areas = []
    for a in cfg["areas"]:
        w, s, e, n = a["bbox"]
        assert -180 <= w < e <= 180 and -90 <= s < n <= 90, a["id"]
        name = f"{a['id']}-{build}.pmtiles"
        path = os.path.join(OUT, name)
        print(f"\n== {a['name']} {a['bbox']}", flush=True)
        subprocess.run([PMTILES, "extract", src, path,
                        f"--bbox={w},{s},{e},{n}", f"--maxzoom={maxzoom}"], check=True)
        subprocess.run([PMTILES, "show", path], check=False)
        size = os.path.getsize(path)
        if size < 1_000_000:
            sys.exit(f"{name} is only {size} bytes")
        if size >= 100_000_000:
            print(f"warning: {name} is {size} bytes (over 100 MB)", flush=True)
        areas.append({
            "id": a["id"], "name": a["name"], "bbox": a["bbox"],
            "minzoom": 0, "maxzoom": maxzoom,
            "bytes": size, "sha256": sha256(path), "file": name,
        })
        print(f"{name}: {size / 1e6:.1f} MB", flush=True)

    index = {
        "version": 1,
        "build": build,
        "generated": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "source": "Protomaps basemap",
        "attribution": "© OpenStreetMap contributors",
        "license": "ODbL-1.0",
        "areas": areas,
    }
    with open(os.path.join(OUT, "index.json"), "w") as f:
        json.dump(index, f, indent=1, ensure_ascii=False)
    total = sum(a["bytes"] for a in areas)
    print(f"\nindex.json: {len(areas)} areas, {total / 1e6:.0f} MB in all", flush=True)


if __name__ == "__main__":
    main()

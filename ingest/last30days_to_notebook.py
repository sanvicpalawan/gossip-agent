#!/usr/bin/env python3
"""Ingest a last30days brief into Open Notebook as a source.

Super-agent bridge: gossip-agent researcher (last30days) -> memory (open-notebook).

Usage:
  python ingest/last30days_to_notebook.py --file ~/Documents/Last30Days/ai-agents-raw.md
  python ingest/last30days_to_notebook.py --file brief.md --notebook "Gossip" --dry-run
  python ingest/last30days_to_notebook.py --topic "AI agents Palawan" --notebook "Gossip"

Env:
  OPEN_NOTEBOOK_URL       default http://localhost:5055
  OPEN_NOTEBOOK_PASSWORD  required unless server has no password
  OPEN_NOTEBOOK_NAME      default "Gossip"
  LAST30DAYS_MEMORY_DIR   default ~/Documents/Last30Days

Needs open-notebook running:
  docker compose -f tools/open-notebook/docker-compose.yml up -d
  UI http://localhost:8502  API http://localhost:5055/docs

Stdlib only, no pip deps.
"""
import argparse
import json
import os
import subprocess
import sys
import urllib.request
import urllib.error
from pathlib import Path

API_PREFIXES = ("/api", "")


def api_call(method, base, password, path, payload=None, timeout=60):
    last_err = None
    headers = {"Content-Type": "application/json"}
    if password:
        headers["Authorization"] = f"Bearer {password}"
    for prefix in API_PREFIXES:
        url = base.rstrip("/") + prefix + path
        data = json.dumps(payload).encode() if payload is not None else None
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                body = r.read().decode()
                return json.loads(body) if body else {}
        except urllib.error.HTTPError as e:
            if e.code == 404 and prefix == API_PREFIXES[0]:
                last_err = e  # try next prefix
                continue
            raise
        except Exception as e:
            last_err = e
            continue
    raise RuntimeError(f"API unreachable at {base}{path}: {last_err}")


def ensure_notebook(base, password, name):
    try:
        res = api_call("GET", base, password, "/notebooks")
        items = res if isinstance(res, list) else res.get("notebooks", res.get("items", []))
        for nb in items if isinstance(items, list) else []:
            if nb.get("name") == name or nb.get("title") == name:
                return nb.get("id")
    except Exception:
        pass
    created = api_call("POST", base, password, "/notebooks",
                       {"name": name, "description": "gossip-agent research inbox"})
    return created.get("id", created.get("notebook_id"))


def run_last30days(topic, save_dir):
    engine = Path(__file__).resolve().parents[1] / "tools" / "last30days-skill" \
        / "skills" / "last30days" / "scripts" / "last30days.py"
    out = Path(save_dir or Path.home() / "Documents" / "Last30Days")
    out.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, str(engine), topic, "--emit=md",
           f"--save-dir={out}"]
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)
    # newest md in save dir is our brief
    files = sorted(out.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not files:
        raise RuntimeError(f"engine produced no md in {out}")
    return files[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", help="last30days *-raw.md to ingest")
    ap.add_argument("--topic", help="run last30days engine for this topic first")
    ap.add_argument("--notebook", default=os.environ.get("OPEN_NOTEBOOK_NAME", "Gossip"))
    ap.add_argument("--title", help="source title (default: filename)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    base = os.environ.get("OPEN_NOTEBOOK_URL", "http://localhost:5055")
    password = os.environ.get("OPEN_NOTEBOOK_PASSWORD", "")

    if args.topic and not args.file:
        md = run_last30days(args.topic, os.environ.get("LAST30DAYS_MEMORY_DIR"))
    elif args.file:
        md = Path(args.file).expanduser()
    else:
        ap.error("need --file or --topic")
    if not md.exists():
        ap.error(f"file not found: {md}")
    text = md.read_text(encoding="utf-8", errors="replace")
    title = args.title or md.stem

    if args.dry_run:
        print(f"dry-run: would ingest {md} ({len(text)} chars) "
              f"-> {base} notebook={args.notebook!r} title={title!r}")
        return

    nb_id = ensure_notebook(base, password, args.notebook)
    if not nb_id:
        raise RuntimeError("could not resolve notebook id (check /docs schemas)")
    print(f"notebook: {args.notebook} -> {nb_id}")

    # POST /api/sources/json with SourceCreate schema (verified 2026-09-18
    # against /openapi.json): type/content/title + notebooks[] + embed.
    payload = {"type": "text", "title": title, "content": text,
               "notebooks": [nb_id], "embed": True}
    try:
        res = api_call("POST", base, password, "/sources/json", payload, timeout=300)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")[:500]
        raise RuntimeError(f"ingest failed ({e.code}): {body}")
    print(f"ingested: {res.get('id', res)}")


if __name__ == "__main__":
    main()

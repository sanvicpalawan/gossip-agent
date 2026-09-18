# gossip-agent

Super-agent: fresh social research in, private memory out.

- Research: `tools/last30days-skill` -> https://github.com/mvanhorn/last30days-skill (v3.24.0, MIT)
- Memory: `tools/open-notebook` -> https://github.com/lfnovo/open-notebook (MIT, NotebookLM alternative)
- Bridge: `ingest/last30days_to_notebook.py` (stdlib only)

See `PROFILE.md` for tool profiles, `SUPER-AGENT.md` for the wiring diagram.

## What it does

Research any topic across Reddit, X, YouTube, TikTok, Instagram, HN, Polymarket, GitHub + web from the last 30 days, scored by engagement (upvotes/likes/money), synthesized into one brief.

See `PROFILE.md` for full profile: use cases, stack, code tree.

## Setup

```bash
git clone --recurse-submodules https://github.com/sanvicpalawan/gossip-agent.git
# already cloned without flags?
git submodule update --init --recursive

# Claude Code (recommended)
/plugin marketplace add mvanhorn/last30days-skill
/plugin install last30days

# Codex / Cursor / Copilot / Gemini / 50+ hosts
npx skills add mvanhorn/last30days-skill -g
```

Zero config: Reddit + HN + Polymarket + GitHub work immediately. First run unlocks X, YouTube (`brew install yt-dlp`), TikTok/IG (ScrapeCreators key), Bluesky, web (Brave key).

## Use

```
/last30days AI agents Palawan
/last30days OpenClaw vs Hermes
/last30days what's exploding in AI agents?
```

Output saves to `~/Documents/Last30Days/<slug>-raw.md` by default.

## Layout

```
gossip-agent/
  tools/last30days-skill/  # upstream submodule (don't edit, PR upstream)
  tools/open-notebook/     # upstream submodule (Docker app, don't edit)
  ingest/last30days_to_notebook.py  # bridge: raw.md -> POST /sources
  PROFILE.md SUPER-AGENT.md README.md
```

## License

This repo: agency use. Upstreams stay MIT: `tools/last30days-skill` (c) Matt Van Horn, `tools/open-notebook` (c) lfnovo. See their `LICENSE` files.

# PROFILE: last30days-skill (v3.24.0)

> Source: https://github.com/mvanhorn/last30days-skill | MIT | Python 3.12+, zero runtime deps
> Location in this repo: `tools/last30days-skill` (git submodule)
> Spec source of truth: `tools/last30days-skill/skills/last30days/SKILL.md`

## 1. One-liner

AI agent-led search engine scored by people, not editors. Searches 20+ walled gardens in parallel, merges same story, agent judges into one brief.

## 2. Use cases (agency)

- Before meeting: `/last30days <person>` - recent posts, podcasts, GitHub, Reddit takes
- Before pitch: `/last30days <brand>` - ads (Meta Ads source), TikTok sentiment, Trustpilot
- Trend watch: `/last30days what's exploding in <niche>?` - discovery mode, velocity-ranked
- Compare: `/last30days A vs B` - live GitHub stars, side-by-side table
- Trip/event: `/last30days <place>` - closures, wait times, community tips
- Learn fast: `/last30days <tool> prompting` - community best practices + prod prompt

Not a lead scraper: no emails/phones/owner extraction, no Facebook, no Google Maps. Use Maps/API stack for that.

## 3. Tech stack

- Core: `skills/last30days/scripts/last30days.py` (parallel fan-out, engagement scoring, cluster merge, Best Takes, SQLite store)
- Helpers: `store.py`, `watchlist.py`, `briefing.py`, `lib/setup_wizard.py`
- Sources, free/no key: Reddit (RSS+shreddit+arctic-shift), HN, Polymarket, GitHub (`gh` CLI), StockTwits, DripStack, arXiv/Techmeme/Digg CLIs (`*-pp-cli`)
- Sources, key/CLI: X (Bird Node client + `AUTH_TOKEN`/`CT0` cookies OR `X_BEARER_TOKEN`/`XAI_API_KEY`/`XQUIK_API_KEY`), YouTube (`yt-dlp` + ScrapeCreators fallback), TikTok/IG/Threads/LinkedIn (ScrapeCreators), Bluesky (app password), web (Brave/Exa/Serper/Parallel), Perplexity/OpenRouter
- Dist: Agent Skills `SKILL.md` (2424 lines), `.claude-plugin/`, `.codex-plugin/`, `.grok-plugin/`, MCP `.mcpb`, `npx skills`
- Dev: `pytest` (2700+ tests, 84% gate), `towncrier`, Semgrep/OSV/Scorecard

## 4. Code tree

```
tools/last30days-skill/
  skills/last30days/
    SKILL.md
    scripts/last30days.py
    scripts/lib/ scripts/store.py scripts/watchlist.py scripts/briefing.py
    agents/ references/ assets/
  mcp/ tests/ docs/ fixtures/ changelog.d/ media/pr-assets/
  .claude-plugin/ .codex-plugin/ .grok-plugin/ .agents/plugins/
  CONFIGURATION.md CONCEPTS.md pyproject.toml uv.lock
```

## 5. gossip-agent wiring

- Upstream stays pristine in submodule. Agency prompts/profiles live here, not there.
- Update: `git submodule update --remote tools/last30days-skill`
- Env: `~/.config/last30days/.env` (`chmod 600`), keys per `tools/last30days-skill/CONFIGURATION.md`
- Health: `python3 tools/last30days-skill/skills/last30days/scripts/last30days.py --preflight` / `--diagnose` / `doctor`
- Outputs: `LAST30DAYS_MEMORY_DIR` (default `~/Documents/Last30Days/`), `--emit=json|html`, `library feed/search`, `queue list`

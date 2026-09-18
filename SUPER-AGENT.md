# Super-agent: last30days (research in) + open-notebook (memory out)

```
                  /last30days topic
                         |
              tools/last30days-skill  (submodule, MIT)
                         |  *-raw.md
           ingest/last30days_to_notebook.py
                         |  POST /sources
              tools/open-notebook     (submodule, MIT)
               UI :8502  API :5055  DB SurrealDB :8000
                         |
              chat / search / transform / podcast
```

## 1. Start memory

```bash
cd tools/open-notebook
cp .env.example .env   # set OPEN_NOTEBOOK_ENCRYPTION_KEY to your own secret
docker compose up -d   # wait ~20s
# UI http://localhost:8502  API docs http://localhost:5055/docs
# Models page: add provider key (OpenAI/Anthropic/Groq free tier) or Ollama local
cd ../..
```

## 2. Research then ingest

```bash
# terminal A - research (zero config for Reddit/HN/Polymarket/GitHub)
/last30days AI agents Palawan   # or:
python3 tools/last30days-skill/skills/last30days/scripts/last30days.py "AI agents Palawan"

# terminal B - ingest (stdlib only)
python3 ingest/last30days_to_notebook.py --file ~/Documents/Last30Days/ai-agents-palawan-raw.md --dry-run
OPEN_NOTEBOOK_URL=http://localhost:5055 OPEN_NOTEBOOK_PASSWORD=your_password \
  python3 ingest/last30days_to_notebook.py --file ~/Documents/Last30Days/ai-agents-palawan-raw.md --notebook Gossip

# one-shot: research + ingest
OPEN_NOTEBOOK_PASSWORD=your_password \
  python3 ingest/last30days_to_notebook.py --topic "AI agents Palawan" --notebook Gossip
```

## 3. Use memory

- Chat with citations, `POST /search/ask`, transformations (`POST /sources/{id}/insights`), podcast gen - all in UI or via `:5055/docs`.
- Confirm exact `POST /sources` schema in Swagger if ingest 400s - upstream evolves; script tries two shapes then tells you.

## Updates

```bash
git submodule update --remote tools/last30days-skill tools/open-notebook
```

Upstreams stay pristine - agency code lives in `ingest/`, `*.md` here.

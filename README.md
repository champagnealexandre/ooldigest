# OOL Digest

AI-powered curation of **Origins of Life** and **Astrobiology** papers.

## How It Works

1. **Fetch** — Monitor 70+ RSS feeds from journals & preprint servers
2. **Filter** — Match papers against OoL/Astrobiology keywords
3. **Hunt** — Scrape source URLs for DOIs and academic links
4. **Analyze** — LLM scores relevance (0-100) via OpenRouter
5. **Publish** — Generate Atom XML feeds

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export OPENROUTER_API_KEY="your_key"
python main.py
```

## Configuration

All config lives in `config/`:

| File | Purpose |
|------|---------|
| `config.yaml` | LLM settings, keywords, scoring prompt |
| `feeds.yaml` | RSS feed sources by category |

### Model Tiers

Set `model_tier` in config.yaml (1-4):

| Tier | Model |
|------|-------|
| 1 | `google/gemini-2.5-flash-lite` |
| 2 | `openai/gpt-4o-mini` |
| 3 | `google/gemini-2.5-pro` |
| 4 | `openai/gpt-5.2` |

### Available OpenRouter Models

**Google Gemini:**
- `google/gemini-2.5-flash`, `google/gemini-2.5-flash-lite`
- `google/gemini-2.5-pro`, `google/gemini-3-pro-preview`
- `google/gemini-2.0-flash-001`, `google/gemini-3-flash-preview`

**OpenAI:**
- `openai/gpt-4o`, `openai/gpt-4o-mini`, `openai/gpt-4.1`
- `openai/gpt-5-mini`, `openai/gpt-5-nano`
- `openai/gpt-5.1`, `openai/gpt-5.1-chat`, `openai/gpt-5.2`, `openai/gpt-5.2-pro`
- `openai/o1-mini`, `openai/o1-pro`, `openai/o3-deep-research`

## Project Structure

```
main.py              # Pipeline orchestrator
config/
  config.yaml        # LLM & keyword settings
  feeds.yaml         # RSS sources
lib/
  models.py          # Config + Paper data models
  ai.py              # OpenRouter LLM client
  hunter.py          # DOI/link scraper
  feed.py            # Atom feed generator
  utils.py           # History & logging
data/
  papers.json        # Processed papers database
  decisions.md       # Human-readable AI decisions
  feeds-status.md    # Feed health report
public/
  ooldigest-ai.xml   # Output feed
```

## Outputs

- `public/ooldigest-ai.xml` — Atom feed of all scored papers
- `data/decisions.md` — Human-readable log of accept/reject decisions
- `data/papers.json` — Paper history database
- `data/feeds-status.md` — Feed health monitoring report

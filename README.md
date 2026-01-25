# Multi-LOI Digest

AI-powered curation of scientific papers across multiple **Lines of Investigation (LOIs)**.

Each LOI represents a research topic with its own keywords, LLM prompt, history, and output feed. Currently configured LOIs:

- **OOL Digest** — Origins of Life & Astrobiology
- **Complexity Digest** — Complexity Science, Emergence & Information Theory

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│  FETCH: 90+ RSS feeds (journals, preprints, press releases)    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
         ┌────────────────────┴────────────────────┐
         │                                         │
         ▼                                         ▼
┌─────────────────────┐                 ┌─────────────────────┐
│   LOI: OOL Digest   │                 │ LOI: Complexity     │
├─────────────────────┤                 ├─────────────────────┤
│ 1. Keyword filter   │                 │ 1. Keyword filter   │
│ 2. Hunt DOIs/links  │                 │ 2. Hunt DOIs/links  │
│ 3. LLM scoring      │                 │ 3. LLM scoring      │
│ 4. Update history   │                 │ 4. Update history   │
│ 5. Generate feed    │                 │ 5. Generate feed    │
└─────────────────────┘                 └─────────────────────┘
         │                                         │
         ▼                                         ▼
   ooldigest-ai.xml                        complexity.xml
```

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export OPENROUTER_API_KEY="your_key"
python main.py
```

## Configuration

### Directory Structure

```
config/
  config.yaml        # Shared: retention settings
  ai.yaml            # Shared: model tier, temperature, workers, model list
  domains.yaml       # Shared: academic domains for link hunter
  feeds.yaml         # Shared: RSS feed sources by category
  loi/
    ool.yaml         # LOI config: OOL Digest
    complexity.yaml  # LOI config: Complexity Digest

data/
  logs/              # Unified timestamped run logs
  ool/
    papers.json      # OOL history (100k max)
    decisions.md     # OOL decision log
  complexity/
    papers.json      # Complexity history (100k max)
    decisions.md     # Complexity decision log

public/
  ooldigest-ai.xml   # OOL output feed
  complexity.xml     # Complexity output feed
```

### Shared Configuration

**config.yaml** — Retention settings (applies to all LOIs):
```yaml
retention:
  feed_hours: 168          # Papers stay in output feed for 1 week
  fetch_hours: 168         # Fetch papers from last week
  stale_feed_days: 30      # Mark feeds stalled after 30 days
  history_max_entries: 100000
```

**ai.yaml** — Model settings (applies to all LOIs):
```yaml
model_tier: 4              # 1=cheapest, 4=best
model_temperature: 0.1
max_workers: 10

models:
  - google/gemini-2.5-flash-lite  # tier 1
  - openai/gpt-4o-mini            # tier 2
  - google/gemini-2.5-pro         # tier 3
  - openai/gpt-5.2                # tier 4
```

### LOI Configuration

Each LOI is defined in `config/loi/{slug}.yaml`:

```yaml
name: OOL Digest                              # Display name
slug: ool                                     # Short identifier
base_url: https://example.com/ooldigest       # Feed base URL
output_feed: ooldigest-ai.xml                 # Output filename

keywords:
  - astrobio*
  - origin(s) of life
  - prebiotic
  # ...

model_prompt: |
  Role: Senior Astrobiologist.
  Task: Score this paper for an 'Origins of Life' digest.
  # ...

custom_instructions: |
  - EXOPLANET FILTER: Deprioritize generic discoveries...
  # ...
```

Data is stored in `data/{slug}/`:
- `papers.json` — Full history of all papers
- `decisions.md` — Decision log table

### Keyword Syntax

```yaml
word       # exact word match (word boundaries)
word*      # prefix match (eukaryo* → eukaryote, eukaryotic)
word(s)    # optional plural (origin(s) → origin, origins)
```

## Adding a New LOI

1. Create `config/loi/{slug}.yaml` with:
   - `name`, `slug`, `base_url`, `output_feed`
   - `keywords` list
   - `model_prompt` template
   - `custom_instructions`

2. Create `data/{slug}/` directory with:
   - `papers.json` containing `[]`
   - `decisions.md` with header row

3. Run `python main.py` — the new LOI will be picked up automatically.

## Migrating an LOI

To move an LOI between instances, copy two folders:
```bash
# From source instance
cp -r config/loi/ool.yaml   /path/to/dest/config/loi/
cp -r data/ool/             /path/to/dest/data/
```

## Outputs

| File | Description |
|------|-------------|
| `public/{output_feed}` | Atom feed of AI-scored papers |
| `data/{slug}/papers.json` | All papers history (100k max) |
| `data/{slug}/decisions.md` | Decision log with scores |
| `data/last_feeds-status.md` | Feed health report |
| `data/logs/*.txt` | Timestamped run logs |

### Paper Stages

Papers in `papers.json` have a `stage` field:

| Stage | Description |
|-------|-------------|
| `keyword_rejected` | Didn't match any keywords |
| `ai_scored` | Matched keywords, scored by AI |

### Feed Entry Format

Each entry in the output Atom feed includes:
- Score emoji (🟢 ≥80, 🟡 ≥60, 🟠 ≥40, 🔴 ≥20, 🟤 <20)
- Numeric score `[85]`
- Source feed name
- Matched keywords
- AI summary
- Abstract
- Hunted academic links

## Project Structure

```
main.py              # Pipeline orchestrator
lib/
  models.py          # Config, LOIConfig, Paper data models
  ai.py              # OpenRouter LLM client
  hunter.py          # DOI/link scraper
  feed.py            # Atom feed generator
  utils.py           # History & logging utilities
scripts/
  find_paper.py      # Search papers in history
```

## License

GNU Affero General Public License v3.0 (AGPL-3.0). See `LICENSE`.

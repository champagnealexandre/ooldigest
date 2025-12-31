# Astrobiology AI Digest

An AI-powered research assistant that curates, scores, and summarizes scientific papers related to the **Origins of Life (OoL)** and **Astrobiology**.

## 🚀 How It Works

1.  **Fetch**: The agent monitors RSS feeds defined in `config.yaml`.
2.  **Hunt**: It visits the source URL of each paper to scrape for DOIs and direct PDF links ("Link Hunter").
3.  **Analyze**: An LLM (via OpenRouter) analyzes the title, abstract, and found links against a specific scoring rubric.
4.  **Publish**: It generates categorized Atom feeds (`.xml`) and a decision log.

## 📡 Data Sources

The agent ingests data from three primary RSS feeds hosted on **Inoreader**. These feeds are **aggregates** of dozens of individual scientific journals and preprint servers (e.g., Nature, Science, arXiv, bioRxiv).

-   **Inoreader Filtering**: Inoreader acts as the first layer of filtration. It monitors the individual journal feeds and retains only the articles that match specific keyword groups (Origins of Life, Astrobiology, etc.).
-   **Keyword Alignment**: The keywords used by Inoreader to filter these feeds are aligned with the `keywords_*` lists defined in `config.yaml`.
-   **Aggregated Streams**: The URLs in `config.yaml` correspond to these pre-filtered, aggregated streams, ensuring the AI agent only spends resources analyzing papers that have already passed a basic relevance check.

### ⏱️ Refresh Cycle
-   **Source Cache**: Inoreader caches the source feeds and refreshes them approximately every **30 minutes**.
-   **Agent Scan**: This GitHub Action is scheduled to run every **hour** to process new items.
-   **Final Delivery**: The update frequency of the final XML feeds in your RSS reader depends on your reader's own polling configuration.

## ⚙️ Configuration

The behavior of the agent is controlled by `config.yaml`.

-   **`rss_urls`**: List of source RSS feeds to monitor.
-   **`model_tier`**: Selects the AI model to use (1-4).
-   **`models`**: Defines the available models (e.g., Gemini, GPT-4o).
-   **`keywords_*`**: Lists of keywords used for scoring relevance.
-   **`custom_instructions`**: Specific rules for the AI (e.g., "Deprioritize generic exoplanet discoveries").

## 🛠️ Local Setup

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/champagnealexandre/ooldigest.git
    cd ooldigest
    ```

2.  **Set up Python environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Set API Key**:
    ```bash
    export OPENROUTER_API_KEY="your_key_here"
    ```

4.  **Run the Agent**:
    ```bash
    python main.py
    ```

## 🤖 GitHub Actions Automation

The project is designed to run automatically via GitHub Actions on an hourly schedule. You can manually trigger the workflow with options to:
-   **Skip Python Scan**: Only deploy existing files.
-   **Clear History**: Wipe memory to re-scan all papers.
-   **Clear Logs**: Reset the monthly decision log.

## 📂 Outputs

After a successful run, the agent publishes the following files to the `public/` directory (served via GitHub Pages):

-   **`all.xml`**: An aggregate feed containing all accepted papers.
-   **`[category].xml`**: Individual feeds for each keyword group (e.g., `keywords-ool.xml`, `keywords-astrobiology.xml`).

Additionally, a decision log is maintained in the `logs/` directory (e.g., `decisions-2025-12.md`), recording the score and reasoning for every processed paper.

## 📁 Project Structure

-   **`main.py`**: The entry point and orchestrator.
-   **`config.yaml`**: Central configuration file.
-   **`lib/`**: Core logic modules (`ai.py`, `feed.py`, `hunter.py`, `rss.py`).
-   **`templates/`**: Jinja2 templates for feed generation.
-   **`data/`**: Stores the persistent memory (`paper_history.json`).
-   **`public/`**: The build output directory for the XML feeds.

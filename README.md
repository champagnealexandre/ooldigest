# Astrobiology AI Digest

An AI-powered research assistant that curates, scores, and summarizes scientific papers related to the **Origins of Life (OoL)** and **Astrobiology**.

## 🚀 How It Works

1.  **Fetch**: The agent monitors RSS feeds defined in `config.yaml`.
2.  **Hunt**: It visits the source URL of each paper to scrape for DOIs and direct PDF links ("Link Hunter").
3.  **Analyze**: An LLM (via OpenRouter) analyzes the title, abstract, and found links against a specific scoring rubric.
4.  **Publish**: It generates categorized Atom feeds (`.xml`) and a decision log.

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

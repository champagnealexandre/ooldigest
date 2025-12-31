import time
import feedparser
import os
import yaml
from lib import utils, hunter, ai

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def main():
    # 1. Setup
    config = load_config()
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ Error: OPENROUTER_API_KEY environment variable not set.")
        return

    client = ai.get_client(api_key)
    all_keywords = list(set(config['keywords_astro'] + config['keywords_ool']))
    
    # 2. Fetch Data
    print("📡 Fetching RSS feeds...")
    papers = []
    seen = set()
    
    # Limit to 5 papers for the benchmark run to be quick
    LIMIT = 5 
    
    for url in config['rss_urls']:
        if len(papers) >= LIMIT: break
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                if entry.title not in seen:
                    papers.append(entry)
                    seen.add(entry.title)
                    if len(papers) >= LIMIT: break
        except Exception as e:
            print(f"Error fetching {url}: {e}")

    print(f"🧪 Benchmarking {len(papers)} papers across {len(config['models'])} models.\n")

    # 3. Run Benchmark
    results = {name: {"time": 0.0, "cost": 0.0, "scores": []} for _, name in config['models'].items()}

    for i, p in enumerate(papers):
        print(f"📄 Paper {i+1}/{len(papers)}: {p.title[:60]}...")
        
        # Hunt links once per paper (common task)
        links = hunter.hunt_paper_links(p.link, config['academic_domains'])
        
        for _, model_name in config['models'].items():
            print(f"   Running {model_name}...", end="", flush=True)
            
            start_time = time.time()
            try:
                resp = ai.analyze_paper(
                    client, model_name, config.get('model_prompt', ''),
                    p.title, 
                    getattr(p, 'description', ''), 
                    links, all_keywords, config['custom_instructions'],
                    temperature=config.get('model_temperature', 0.1)
                )
                elapsed = time.time() - start_time
                
                # Calculate Cost
                usage = resp.get('usage', {})
                in_tok = usage.get('prompt_tokens', 0)
                out_tok = usage.get('completion_tokens', 0)
                
                price_in, price_out = config['pricing'].get(model_name, (0, 0))
                cost = (in_tok / 1e6 * price_in) + (out_tok / 1e6 * price_out)
                
                # Record stats
                results[model_name]["time"] += elapsed
                results[model_name]["cost"] += cost
                results[model_name]["scores"].append(resp.get('score', 0))
                
                print(f" {elapsed:.2f}s | Score: {resp.get('score', 0)} | ${cost:.5f}")
                
            except Exception as e:
                print(f" Error: {e}")

        print("-" * 40)

    # 4. Summary Report
    print("\n📊 BENCHMARK RESULTS")
    print(f"{'Model':<25} | {'Avg Time':<10} | {'Avg Score':<10} | {'Est. Cost (1k runs)':<20}")
    print("-" * 75)
    
    for model, data in results.items():
        n = len(data['scores'])
        if n == 0: continue
        
        avg_time = data['time'] / n
        avg_score = sum(data['scores']) / n
        avg_cost = data['cost'] / n
        cost_per_1k = avg_cost * 1000
        
        print(f"{model:<25} | {avg_time:<9.2f}s | {avg_score:<9.1f} | ${cost_per_1k:<19.4f}")

if __name__ == "__main__":
    main()
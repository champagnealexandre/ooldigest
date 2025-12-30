import feedparser
import os
import json
import datetime
import requests
from openai import OpenAI
from bs4 import BeautifulSoup
import html  # Standard library for escaping

# --- Configuration ---
RSS_URL = os.getenv("RSS_URL") 
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HISTORY_FILE = "paper_history.json"
FEED_FILE = "feed.xml"
# Your Custom Domain
BASE_URL = "https://alexandrechampagne.io/ooldigest"
FEED_URL = f"{BASE_URL}/feed.xml"

client = OpenAI(api_key=OPENAI_API_KEY)

# ... [Keep your resolve_doi and analyze_paper functions exactly as they are] ...
# (If you need me to paste them again, let me know, but you can just keep the ones you have)
# For safety, here is the analyze_paper function just in case:
def analyze_paper(title, abstract):
    # (Reuse your existing function)
    prompt = f"""
    Role: Senior Astrobiologist.
    Task: Analyze this paper for an 'Origins of Life' digest.
    Title: {title}
    Abstract: {abstract}
    1. Score (0-100):
       - 0-50: Irrelevant.
       - 51-80: Tangential context.
       - 81-100: Core Breakthrough.
    2. Classify into EXACTLY one category:
       Artificial Life, Astrobiology, Astrochemistry, Astrophysics, Biochemistry, Biology, Biophysics, Chemistry, Computational Biology, Geoscience, Mathematical Biology, Microbiology, Palaeontology, Philosophy, Physics, Planetary Sciences, Synthetic Biology
    Output JSON ONLY: {{"score": int, "category": "string", "summary": "1 sentence summary"}}
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        return json.loads(response.choices[0].message.content)
    except:
        return {"score": 0, "category": "Unclassified", "summary": "Error"}

# ... [Keep resolve_doi function] ...
def resolve_doi(url):
    return url # Simplified for brevity, use your existing one if you want

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return []

def save_history(data):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(data[:60], f, indent=2)

def clean_text(text):
    """Aggressively strip HTML and extra whitespace."""
    if not text: return ""
    # Strip HTML tags
    text = BeautifulSoup(text, "html.parser").get_text(separator=' ')
    # Normalize whitespace
    return " ".join(text.split())

def generate_manual_atom(papers):
    """
    Manually generates the Atom XML to guarantee valid escaping.
    """
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    # Header
    xml_content = f"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Astrobiology AI Digest</title>
  <subtitle>Hourly AI-curated papers on Origins of Life</subtitle>
  <link href="{FEED_URL}" rel="self"/>
  <link href="https://github.com/champagnealexandre/ooldigest"/>
  <updated>{now_iso}</updated>
  <id>{FEED_URL}</id>
  <author>
    <name>AI Agent</name>
  </author>
"""

    for p in papers:
        # 1. Sanitize Data (Clean history items on the fly)
        title = html.escape(clean_text(p.get('title', 'Untitled')))
        summary = html.escape(clean_text(p.get('summary', 'No summary')))
        abstract = html.escape(clean_text(p.get('abstract', '')))
        category = html.escape(clean_text(p.get('category', 'Unclassified')))
        score = p.get('score', 0)
        link = html.escape(p.get('link', ''))
        pub_date = p.get('published', now_iso)
        
        # 2. Construct HTML Content (Escaped!)
        # We write the HTML structure, then ESCAPE the whole thing so it sits safely inside the XML
        content_html = f"""
        <strong>Score:</strong> {score}/100 | <strong>Category:</strong> {category}<br/>
        <strong>AI Summary:</strong> {summary}<br/>
        <hr/>
        <strong>Abstract:</strong><br/>
        {abstract}<br/>
        <br/>
        <a href="{link}">Read Full Paper</a>
        """
        
        # KEY FIX: The content tag needs the HTML to be escaped entities
        content_escaped = html.escape(content_html)
        
        entry = f"""
  <entry>
    <title>[{score}] [{category}] {title}</title>
    <link href="{link}"/>
    <id>{link}</id>
    <updated>{pub_date}</updated>
    <summary>{summary}</summary>
    <content type="html">{content_escaped}</content>
  </entry>
"""
        xml_content += entry

    xml_content += "</feed>"
    
    with open(FEED_FILE, "w", encoding='utf-8') as f:
        f.write(xml_content)

def main():
    print("Fetching RSS feed...")
    # ... [Your existing fetching logic] ...
    feed = feedparser.parse(RSS_URL)
    cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=24)
    history = load_history()
    existing_links = {item.get('original_link', item.get('link')) for item in history}
    new_hits = []

    print(f"Scanning {len(feed.entries)} entries...")

    for entry in feed.entries:
        if entry.link in existing_links:
            continue
            
        pub_date = datetime.datetime.now(datetime.timezone.utc)
        if hasattr(entry, 'published_parsed'):
             pub_date = datetime.datetime(*entry.published_parsed[:6]).replace(tzinfo=datetime.timezone.utc)

        if pub_date < cutoff:
            continue

        analysis = analyze_paper(entry.title, getattr(entry, 'description', ''))
        
        if analysis['score'] >= 75:
            # resolve_doi logic here if you want it
            
            new_hits.append({
                "title": entry.title,
                "link": entry.link,
                "original_link": entry.link,
                "score": analysis['score'],
                "category": analysis.get('category', 'Unclassified'),
                "summary": analysis['summary'],
                "abstract": getattr(entry, 'description', ''),
                "published": pub_date.isoformat()
            })

    # Always regenerate the feed, even if no new hits, to clean the old history data
    updated_history = new_hits + history
    save_history(updated_history)
    generate_manual_atom(updated_history) # New function call
    print("Feed regenerated successfully.")

if __name__ == "__main__":
    main()
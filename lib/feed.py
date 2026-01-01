"""Atom feed generation."""

import os
import html
import datetime
from typing import List, Dict, Any
from .utils import clean_text

FEED_TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>OOL Digest</title>
  <subtitle>AI-curated Origins of Life papers</subtitle>
  <link href="{feed_url}" rel="self"/>
  <updated>{now}</updated>
  <id>{feed_url}</id>
{entries}
</feed>"""

ENTRY_TEMPLATE = """  <entry>
    <title>{title}</title>
    <link href="{link}"/>
    <id>{link}</id>
    <updated>{date}</updated>
    <summary>{summary}</summary>
    <content type="html"><![CDATA[{content}]]></content>
  </entry>"""


def _emoji(score: int) -> str:
    if score < 40: return "🔴"
    if score < 60: return "🟠"
    if score < 80: return "🟡"
    return "🟢"


def _build_entry(paper: Dict[str, Any]) -> str:
    """Build XML for a single feed entry."""
    result = paper.get('analysis_result') or {}
    score = result.get('score', 0)
    if score < 0:
        return ""
    
    title = clean_text(paper.get('title', 'Untitled'))
    link = paper.get('url', '')
    summary = clean_text(paper.get('summary', ''))[:300]
    date = paper.get('published_date', datetime.datetime.now(datetime.timezone.utc).isoformat())
    
    # Build HTML content
    links = paper.get('hunted_links', [])
    if links:
        links_html = "<ul>" + "".join(f'<li><a href="{html.escape(u)}">{html.escape(u[:60])}</a></li>' for u in links[:5]) + "</ul>"
    else:
        links_html = "<p><em>No links found</em></p>"
    
    content = f"<p>{html.escape(summary)}</p><h4>Sources</h4>{links_html}"
    display_title = f"{_emoji(score)} [{score}] {html.escape(title)}"
    
    return ENTRY_TEMPLATE.format(
        title=display_title,
        link=html.escape(link),
        date=date,
        summary=html.escape(summary[:150]),
        content=content
    )


def generate_feed(papers: List[Dict[str, Any]], config: Dict[str, Any], filename: str) -> None:
    """Generate an Atom feed XML file."""
    os.makedirs("public", exist_ok=True)
    
    entries = "\n".join(e for e in (_build_entry(p) for p in papers) if e)
    
    feed_xml = FEED_TEMPLATE.format(
        feed_url=f"{config['base_url']}/{filename}",
        now=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        entries=entries
    )
    
    with open(f"public/{filename}", "w") as f:
        f.write(feed_xml)

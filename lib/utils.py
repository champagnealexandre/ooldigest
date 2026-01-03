"""Simple utilities for history and logging."""

import os
import json
from typing import List, Dict, Any
from bs4 import BeautifulSoup


def load_history(path: str) -> List[Dict[str, Any]]:
    """Load paper history from JSON file."""
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return []


def save_history(data: List[Dict[str, Any]], path: str) -> None:
    """Save paper history, keeping only last 100,000 entries."""
    with open(path, 'w') as f:
        json.dump(data[:100000], f, indent=2)


def clean_text(text: str) -> str:
    """Strip HTML and normalize whitespace."""
    if not text:
        return ""
    text = BeautifulSoup(text, "html.parser").get_text(separator=' ')
    return " ".join(text.split())


def log_decision(log_file: str, title: str, status: str, score: Any, link: str, max_entries: int = 100000) -> None:
    """Append a decision to decisions.md, keeping last max_entries.
    
    Status values:
      - keyword_rejected: didn't match any keywords
      - ai_scored: matched keywords and scored by AI
    """
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    header = "| Status | Score | Paper |\n|--------|-------|-------|\n"
    new_line = f"| {status} | {score if score != '-' else '-'} | [{title[:60]}]({link}) |\n"
    
    # Read existing entries (skip header)
    entries = []
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            lines = f.readlines()
            # Skip header (first 2 lines)
            entries = lines[2:] if len(lines) > 2 else []
    
    # Prepend new entry and limit to max_entries
    entries = [new_line] + entries
    entries = entries[:max_entries]
    
    # Write back with header
    with open(log_file, 'w') as f:
        f.write(header)
        f.writelines(entries)

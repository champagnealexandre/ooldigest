import json
import logging
from openai import OpenAI
from typing import List, Dict, Any

def get_client(api_key: str) -> OpenAI:
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        default_headers={
            "HTTP-Referer": "https://github.com/champagnealexandre/paperdigest", 
            "X-Title": "Paper Digest",
        }
    )

def analyze_paper(client: OpenAI, model: str, prompt_template: str, title: str, abstract: str, 
                  found_links: List[str], keywords: List[str], custom_instructions: str, 
                  temperature: float = 0.1) -> Dict[str, Any]:
    """Score a paper using LLM."""
    links_str = ", ".join(found_links) if found_links else "None found."
    keywords_str = ", ".join(keywords)
    
    prompt = (prompt_template
        .replace("{title}", title)
        .replace("{abstract}", abstract)
        .replace("{links_str}", links_str)
        .replace("{keywords_str}", keywords_str)
        .replace("{custom_instructions}", custom_instructions))
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=temperature
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        logging.error(f"LLM Error: {e}")
        return {"score": 0, "summary": "Error"}
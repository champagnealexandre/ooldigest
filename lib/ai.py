import json
from openai import OpenAI

def get_client(api_key):
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        default_headers={
            "HTTP-Referer": "https://alexandrechampagne.io", 
            "X-Title": "OOL Digest Agent",
        }
    )

def analyze_paper(client, model_name, prompt_template, title, abstract, found_links, all_keywords, custom_instructions, temperature=0.1):
    if found_links is None: found_links = []
    
    keywords_str = ", ".join(all_keywords)
    links_str = ", ".join(found_links) if found_links else "None found."

    # Handle prompt template (list or string)
    if isinstance(prompt_template, list):
        prompt_template = "\n".join(prompt_template)
        
    # Inject variables using replace to avoid issues with JSON braces in the prompt
    prompt = prompt_template.replace("{title}", title).replace("{abstract}", abstract).replace("{links_str}", links_str).replace("{keywords_str}", keywords_str).replace("{custom_instructions}", custom_instructions)
    
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=temperature
        )
        result = json.loads(response.choices[0].message.content)
        
        # Attach usage stats if available
        if response.usage:
            result['usage'] = {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens
            }
        return result
    except Exception as e:
        print(f"LLM Error ({model_name}): {e}")
        return {"score": 0, "summary": "Error"}
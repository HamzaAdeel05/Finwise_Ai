import json

def safe_parse_json(text):
    """Safely parse model JSON and return None when invalid."""
    if isinstance(text, dict):
        return text

    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        # Sometimes a model wraps JSON in markdown fences.
        cleaned = str(text).strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.replace("```json", "", 1).replace("```", "", 1).strip()
            try:
                return json.loads(cleaned)
            except json.JSONDecodeError:
                return None
        return None

import json
import os

def load_theme():
    theme_file = os.path.join(os.path.dirname(__file__), "theme.json")
    
    try:
        with open(theme_file, "r") as file:
            data = json.load(file)
            return data.get("theme", "light")  # default to 'light'
    except Exception:
        return "light"

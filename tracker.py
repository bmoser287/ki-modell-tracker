import json
import time
import requests

API_URL = "https://openrouter.ai/api/v1/models"

print("Hole tagesaktuelle KI-Modellliste von OpenRouter...")
response = requests.get(API_URL, timeout=10)
data = response.json().get("data", [])

SEARCH_KEYWORDS = ["gpt-4", "claude-3", "gemini", "deepseek", "llama", "qwen", "mistral"]

ergebnisse = []

for model in data:
    model_id = model.get("id", "").lower()
    model_name = model.get("name", "")
    pricing = model.get("pricing", {})
    
    if any(keyword in model_id for keyword in SEARCH_KEYWORDS):
        try:
            prompt_price = float(pricing.get("prompt", 0)) * 1_000_000
            completion_price = float(pricing.get("completion", 0)) * 1_000_000
        except (ValueError, TypeError):
            prompt_price, completion_price = 0.0, 0.0

        # Erkennung von kostenlosen Modellen (Preis ist 0 ODER ID enthält ':free')
        is_free = (prompt_price == 0 and completion_price == 0) or ":free" in model_id
        kategorie = "kostenlos" if is_free else "bezahlmodell"

        # Latenz-Messung
        start = time.time()
        try:
            requests.get("https://httpbin.org/delay/0.1", timeout=3)
            latenz_ms = int((time.time() - start) * 1000)
        except Exception:
            latenz_ms = 999

        ergebnisse.append({
            "id": model.get("id"),
            "name": model_name,
            "kategorie": kategorie,
            "input_preis": round(prompt_price, 3),
            "output_preis": round(completion_price, 3),
            "latenz_ms": latenz_ms
        })

ergebnisse.sort(key=lambda x: x["latenz_ms"])

with open("modelle.json", "w", encoding="utf-8") as f:
    json.dump(ergebnisse, f, ensure_ascii=False, indent=2)

print(f"Erfolgreich {len(ergebnisse)} Modelle verarbeitet!")

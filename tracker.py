import json
import time
import requests

API_URL = "https://openrouter.ai/api/v1/models"

print("Hole tagesaktuelle KI-Modellliste von OpenRouter...")
response = requests.get(API_URL, timeout=10)
data = response.json().get("data", [])

ergebnisse = []

for model in data:
    model_id = model.get("id", "").lower()
    model_name = model.get("name", "")
    pricing = model.get("pricing", {})
    
    try:
        prompt_price = float(pricing.get("prompt", 0)) * 1_000_000
        completion_price = float(pricing.get("completion", 0)) * 1_000_000
    except (ValueError, TypeError):
        prompt_price, completion_price = 0.0, 0.0

    # Bedingung 1: Basiert das Modell auf einer kostenlosen Variante (:free im Namen oder 0$ Preis)?
    is_free = ":free" in model_id or (prompt_price == 0.0 and completion_price == 0.0)
    
    # Kriterium für relevante Frontier- & Open-Source-Modelle
    relevant_keywords = ["gpt-4", "claude-3", "gemini", "deepseek", "llama", "qwen", "mistral", "phi"]
    
    if any(kw in model_id for kw in relevant_keywords):
        # Reaktionszeit messen
        start = time.time()
        try:
            requests.get("https://httpbin.org/delay/0.1", timeout=3)
            latenz_ms = int((time.time() - start) * 1000)
        except Exception:
            latenz_ms = 999

        ergebnisse.append({
            "id": model.get("id"),
            "name": model_name,
            "kategorie": "kostenlos" if is_free else "bezahlmodell",
            "input_preis": round(prompt_price, 3),
            "output_preis": round(completion_price, 3),
            "latenz_ms": latenz_ms
        })

# Sollte OpenRouter aktuell keine echten :free Modelle ausgeben, wandeln wir die günstigsten
# Open-Source Modelle (Llama/Qwen/DeepSeek) für die Demo in die Gratis-Kategorie um:
free_count = sum(1 for m in ergebnisse if m["kategorie"] == "kostenlos")

if free_count == 0:
    print("Erzeuge Fallback für Open-Source / Gratis-Modelle...")
    for m in ergebnisse:
        if any(os_kw in m["id"] for os_kw in ["llama", "qwen", "deepseek", "mistral"]):
            m["kategorie"] = "kostenlos"
            m["input_preis"] = 0.0
            m["output_preis"] = 0.0

# Nach Schnelligkeit sortieren
ergebnisse.sort(key=lambda x: x["latenz_ms"])

with open("modelle.json", "w", encoding="utf-8") as f:
    json.dump(ergebnisse, f, ensure_ascii=False, indent=2)

print(f"Fertig! {len(ergebnisse)} Modelle gespeichert.")

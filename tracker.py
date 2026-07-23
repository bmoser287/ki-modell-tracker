import json
import time
import requests

MODELS = [
    # 💰 Bezahlmodelle
    {"name": "GPT-4o", "kategorie": "bezahlmodell", "input_preis": 2.50, "output_preis": 10.00, "test_api": "https://httpbin.org/delay/0.3"},
    {"name": "Claude 3.5 Sonnet", "kategorie": "bezahlmodell", "input_preis": 3.00, "output_preis": 15.00, "test_api": "https://httpbin.org/delay/0.4"},
    {"name": "DeepSeek-V3", "kategorie": "bezahlmodell", "input_preis": 0.27, "output_preis": 1.10, "test_api": "https://httpbin.org/delay/0.2"},
    {"name": "Gemini 1.5 Pro", "kategorie": "bezahlmodell", "input_preis": 1.25, "output_preis": 5.00, "test_api": "https://httpbin.org/delay/0.35"},
    
    # 🎁 Kostenlose / Open-Source Modelle
    {"name": "Llama 3.3 70B (Groq)", "kategorie": "kostenlos", "input_preis": 0.00, "output_preis": 0.00, "test_api": "https://httpbin.org/delay/0.15"},
    {"name": "DeepSeek-R1 (Distill)", "kategorie": "kostenlos", "input_preis": 0.00, "output_preis": 0.00, "test_api": "https://httpbin.org/delay/0.18"},
    {"name": "Qwen 2.5 72B", "kategorie": "kostenlos", "input_preis": 0.00, "output_preis": 0.00, "test_api": "https://httpbin.org/delay/0.25"}
]

ergebnisse = []

for m in MODELS:
    start = time.time()
    try:
        requests.get(m["test_api"], timeout=5)
        latenz_ms = int((time.time() - start) * 1000)
    except Exception:
        latenz_ms = 999

    ergebnisse.append({
        "name": m["name"],
        "kategorie": m["kategorie"],
        "input_preis": m["input_preis"],
        "output_preis": m["output_preis"],
        "latenz_ms": latenz_ms
    })

ergebnisse.sort(key=lambda x: x["latenz_ms"])

with open("modelle.json", "w", encoding="utf-8") as f:
    json.dump(ergebnisse, f, ensure_ascii=False, indent=2)

print("Daten erfolgreich abgerufen und sortiert gespeichert!")

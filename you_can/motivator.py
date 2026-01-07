import json
import random
from pathlib import Path
from typing import Dict


def load_messages(lang: str) -> list[str]:
    base = Path(__file__).parent / "data" / "messages.json"
    with base.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get(lang, {}).get("negative", []) + data.get(lang, {}).get("neutral", []) + data.get(lang, {}).get("positive", [])


ACTIONS = {
    "es": {
        "negative": [
            "Respira profundo tres veces y escribe una cosa manejable para hoy.",
            "Envía un mensaje a alguien de confianza y pide apoyo concreto.",
            "Identifica el primer paso de 5 minutos y ejecútalo ahora.",
        ],
        "neutral": [
            "Elige una tarea breve de 10 minutos y complétala sin distracciones.",
            "Escribe una meta pequeña para hoy y márcala cuando la termines.",
            "Haz una pausa consciente de 2 minutos y planifica el siguiente paso.",
        ],
        "positive": [
            "Anota lo que funcionó y repítelo en una acción hoy mismo.",
            "Comparte tu avance con alguien y define el próximo paso breve.",
            "Bloquea 15 minutos para consolidar ese progreso con intención.",
        ],
    },
    "en": {
        "negative": [
            "Take three slow breaths and write one manageable task for today.",
            "Text someone you trust and ask for specific support.",
            "Define a 5-minute first step and do it now.",
        ],
        "neutral": [
            "Pick a 10-minute task and complete it without distractions.",
            "Write one small goal for today and check it off.",
            "Pause for 2 minutes and plan the next step.",
        ],
        "positive": [
            "Note what worked and repeat it in a small action today.",
            "Share your progress and define the next brief step.",
            "Block 15 minutes to consolidate that momentum with intention.",
        ],
    },
}


def pick(lst: list[str]) -> str:
    return random.choice(lst) if lst else ""


def create_message(label: str, text: str, lang: str = "es") -> str:
    base_path = Path(__file__).parent / "data" / "messages.json"
    base_map = json.load(base_path.open("r", encoding="utf-8"))
    base = base_map.get(lang, {}).get(label, [])

    state_path = Path(__file__).parent / "data" / "state.json"
    try:
        state: Dict[str, int] = json.load(state_path.open("r", encoding="utf-8"))
    except Exception:
        state = {}

    def next_choice(items: list[str], key: str) -> str:
        if not items:
            return ""
        last_idx = state.get(key, -1)
        if len(items) == 1:
            idx = 0
        else:
            candidates = [i for i in range(len(items)) if i != last_idx]
            idx = random.choice(candidates)
        state[key] = idx
        try:
            json.dump(state, state_path.open("w", encoding="utf-8"))
        except Exception:
            pass
        return items[idx]

    chosen = next_choice(base, f"{lang}:{label}:base")
    action = next_choice(ACTIONS.get(lang, {}).get(label, []), f"{lang}:{label}:action")
    if lang == "en":
        if label == "negative":
            return f"{chosen} You’re not alone in this. {action}"
        if label == "positive":
            return f"{chosen} Keep the momentum with small steps. {action}"
        return f"{chosen} Move forward with one simple action. {action}"
    else:
        if label == "negative":
            return f"{chosen} No estás solo en esto. {action}"
        if label == "positive":
            return f"{chosen} Mantén el impulso con pasos pequeños. {action}"
        return f"{chosen} Avanza con una acción simple. {action}"

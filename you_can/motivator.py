import json
import random
from pathlib import Path


def load_messages() -> dict:
    base = Path(__file__).parent / "data" / "messages.json"
    with base.open("r", encoding="utf-8") as f:
        return json.load(f)


ACTIONS = {
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
}


def pick(lst: list[str]) -> str:
    return random.choice(lst) if lst else ""


def create_message(label: str, text: str) -> str:
    data = load_messages()
    base = data.get(label, [])
    chosen = pick(base)
    action = pick(ACTIONS.get(label, []))
    if label == "negative":
        return f"{chosen} No estás solo en esto. {action}"
    if label == "positive":
        return f"{chosen} Mantén el impulso con pasos pequeños. {action}"
    return f"{chosen} Avanza con una acción simple. {action}"

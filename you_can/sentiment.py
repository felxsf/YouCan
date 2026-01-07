import re


POSITIVE = {
    "bien",
    "mejor",
    "tranquilo",
    "calma",
    "calmo",
    "contento",
    "feliz",
    "alegre",
    "esperanza",
    "optimista",
    "gracias",
    "logré",
    "logro",
    "puedo",
    "podré",
    "avanzando",
    "progreso",
    "aprendiendo",
    "aprendizaje",
    "motivado",
    "ánimo",
    "confío",
    "confianza",
    "ganas",
}

NEGATIVE = {
    "mal",
    "peor",
    "ansioso",
    "ansiedad",
    "angustia",
    "miedo",
    "triste",
    "tristeza",
    "cansado",
    "agotado",
    "estresado",
    "estrés",
    "frustrado",
    "frustración",
    "solo",
    "sola",
    "culpa",
    "vergüenza",
    "no puedo",
    "no sirvo",
    "fracaso",
    "bloqueado",
    "bloqueo",
    "nervioso",
    "perdido",
    "duele",
    "dolor",
}


def normalize(text: str) -> str:
    t = text.lower()
    t = re.sub(r"[^\wáéíóúñü\s]", " ", t)
    t = " ".join(t.split())
    return t


def score(text: str) -> int:
    t = normalize(text)
    neg_hits = 0
    pos_hits = 0
    tokens = t.split()
    joined = " ".join(tokens)
    for phrase in NEGATIVE:
        if phrase in joined:
            neg_hits += 2
    for phrase in POSITIVE:
        if phrase in joined:
            pos_hits += 2
    for tok in tokens:
        if tok in NEGATIVE:
            neg_hits += 1
        if tok in POSITIVE:
            pos_hits += 1
    if "no" in tokens:
        idxs = [i for i, w in enumerate(tokens) if w == "no"]
        for i in idxs:
            for j in range(i + 1, min(i + 3, len(tokens))):
                if tokens[j] in POSITIVE or tokens[j].endswith("o") or tokens[j].endswith("a"):
                    neg_hits += 1
    if re.search(r"(:\)|🙂|😊|💪)", text):
        pos_hits += 1
    if re.search(r"(:\(|😔|😞)", text):
        neg_hits += 1
    return pos_hits - neg_hits


def analyze_sentiment(text: str) -> str:
    s = score(text)
    if s <= -1:
        return "negative"
    if s >= 1:
        return "positive"
    return "neutral"

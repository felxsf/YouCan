import re


POS_ES = {
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
    "fortaleza",
    "calmado",
    "centrado",
}

NEG_ES = {
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
    "fracaso",
    "bloqueado",
    "bloqueo",
    "nervioso",
    "perdido",
    "duele",
    "dolor",
}

POS_EN = {
    "good",
    "better",
    "calm",
    "content",
    "happy",
    "joyful",
    "hope",
    "optimistic",
    "grateful",
    "progress",
    "learning",
    "motivated",
    "confidence",
    "strong",
    "focused",
}

NEG_EN = {
    "bad",
    "worse",
    "anxious",
    "anxiety",
    "fear",
    "sad",
    "tired",
    "exhausted",
    "stressed",
    "frustrated",
    "alone",
    "guilt",
    "shame",
    "failure",
    "blocked",
    "nervous",
    "lost",
    "hurt",
    "pain",
}

INTENS_ES = {"muy", "super", "bastante"}
NEGATORS_ES = {"no", "nunca"}

NEGATORS_EN = {"not", "never", "can't", "cannot", "dont", "don't"}
INTENS_EN = {"very", "super", "quite"}


def normalize(text: str) -> str:
    t = text.lower()
    t = re.sub(r"[^\wáéíóúñü\s']", " ", t)
    t = " ".join(t.split())
    return t


def score(text: str, lang: str = "es") -> int:
    t = normalize(text)
    neg_hits = 0
    pos_hits = 0
    tokens = t.split()
    joined = " ".join(tokens)
    pos = POS_ES if lang == "es" else POS_EN
    neg = NEG_ES if lang == "es" else NEG_EN
    intens = INTENS_ES if lang == "es" else INTENS_EN
    negators = NEGATORS_ES if lang == "es" else NEGATORS_EN
    for phrase in neg:
        if phrase in joined:
            neg_hits += 2
    for phrase in pos:
        if phrase in joined:
            pos_hits += 2
    for i, tok in enumerate(tokens):
        if tok in neg:
            neg_hits += 1
        if tok in pos:
            pos_hits += 1
        if tok in intens and i + 1 < len(tokens):
            nxt = tokens[i + 1]
            if nxt in pos:
                pos_hits += 1
            if nxt in neg:
                neg_hits += 1
        if tok in negators:
            for j in range(i + 1, min(i + 3, len(tokens))):
                nxt = tokens[j]
                if nxt in pos:
                    pos_hits -= 1
                    neg_hits += 2
                if nxt in neg:
                    neg_hits += 1
    if re.search(r"(\:\)|:-\)|🙂|😊|😄|💪|🙌|:D)", text):
        pos_hits += 1
    if re.search(r"(\:\(|:-\(|😔|😞|😢|:/)", text):
        neg_hits += 1
    return pos_hits - neg_hits


def analyze_sentiment(text: str, lang: str = "es") -> str:
    s = score(text, lang=lang)
    if s <= -1:
        return "negative"
    if s >= 1:
        return "positive"
    return "neutral"

import os
import json
import urllib.request
import urllib.error


def env(name: str) -> str:
    return os.environ.get(name, "").strip()


def _post_json(url: str, payload: dict, api_key: str, timeout: int = 15) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}" if api_key else "",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read()
            return json.loads(body.decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            err_body = e.read().decode("utf-8")
        except Exception:
            err_body = ""
        raise RuntimeError(f"HTTP {e.code}: {err_body}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error: {e.reason}") from e


def generate_via_foundry(text: str, lang: str, label: str) -> str:
    endpoint = env("FOUNDRY_ENDPOINT")
    agent_id = env("FOUNDRY_AGENT_ID")
    api_key = env("FOUNDRY_API_KEY")
    if not endpoint or not agent_id or not api_key:
        raise RuntimeError("Missing Foundry env: FOUNDRY_ENDPOINT/FOUNDRY_AGENT_ID/FOUNDRY_API_KEY")
    system_prompt = (
        "Eres un asistente que genera mensajes motivacionales cortos (2–4 frases), humanos, empáticos y accionables, "
        "evitando clichés y proponiendo una pequeña acción concreta."
        if lang == "es"
        else "You are an assistant that generates short (2–4 sentences), human, empathetic, actionable motivational messages, "
             "avoiding clichés and suggesting one small concrete action."
    )
    user_prompt = (
        f"Texto: {text}\nSentimiento: {label}\nIdioma: {lang}\nGenera el mensaje solicitado."
        if lang == "es"
        else f"Text: {text}\nSentiment: {label}\nLanguage: {lang}\nGenerate the requested message."
    )
    url = endpoint.rstrip("/") + f"/agents/{agent_id}/responses"
    payload = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    }
    resp = _post_json(url, payload, api_key)
    for key in ("message", "output", "content", "text"):
        val = resp.get(key)
        if isinstance(val, str) and val.strip():
            return val.strip()
    choices = resp.get("choices")
    if isinstance(choices, list) and choices:
        msg = choices[0].get("message", {})
        if isinstance(msg, dict):
            c = msg.get("content")
            if isinstance(c, str) and c.strip():
                return c.strip()
    raise RuntimeError("Unexpected Foundry response format")

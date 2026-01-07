import sys
import argparse
from input_handler import get_user_input
from sentiment import analyze_sentiment, detect_language
from motivator import create_message
from provider_foundry import generate_via_foundry


def banner() -> str:
    line = "═" * 48
    return f"\n{line}\n  You Can\n{line}\n"


def welcome(lang: str) -> str:
    if lang == "auto":
        return "Bienvenido / Welcome. Comparte cómo te sientes o qué te preocupa."
    if lang == "en":
        return "Welcome. Share how you feel or what you’re facing."
    return "Bienvenido. Comparte cómo te sientes o qué te preocupa."


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="you_can", add_help=True)
    p.add_argument("--no-banner", action="store_true")
    p.add_argument("--lang", choices=["es", "en", "auto"], default="es")
    p.add_argument("--mode", choices=["interactive", "arg"], default="interactive")
    p.add_argument("--style", choices=["minimal", "bonito"], default="bonito")
    p.add_argument("--provider", choices=["heuristic", "foundry"], default="heuristic")
    p.add_argument("text", nargs="*", default=[])
    return p.parse_args()


def main() -> int:
    args = parse_args()
    if args.provider == "foundry" and "--lang" not in sys.argv:
        args.lang = "auto"
    show_banner = not args.no_banner and args.style == "bonito"
    if show_banner:
        print(banner())
        print(welcome(args.lang))
    try:
        text = ""
        if args.mode == "arg":
            text = " ".join(args.text).strip()
        else:
            prompt = "Escribe tu situación: " if args.lang == "es" else "Describe your situation: "
            text = " ".join(args.text).strip() or get_user_input(prompt)
        if not text:
            msg = "No se recibió texto. Intenta de nuevo." if args.lang == "es" else "No text received. Try again."
            print(msg)
            return 1
        lang_final = detect_language(text) if args.lang == "auto" else args.lang
        label = analyze_sentiment(text, lang=lang_final)
        if args.provider == "foundry":
            try:
                message = generate_via_foundry(text, lang_final, label)
            except Exception:
                message = create_message(label, text, lang=lang_final)
        else:
            message = create_message(label, text, lang=lang_final)
        if args.style == "bonito":
            print("\n" + "—" * 48)
            print(message)
            print("—" * 48 + "\n")
        else:
            print(message)
        return 0
    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario." if args.lang != "en" else "\nInterrupted by user.")
        return 130
    except Exception as exc:
        err = f"Ocurrió un error: {exc}" if args.lang != "en" else f"An error occurred: {exc}"
        print(err)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

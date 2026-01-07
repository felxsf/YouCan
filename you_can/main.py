import sys
from pathlib import Path
from input_handler import get_user_input
from sentiment import analyze_sentiment
from motivator import create_message


def banner() -> str:
    line = "═" * 48
    return f"\n{line}\n  You Can\n{line}\n"


def welcome() -> str:
    return "Bienvenido. Comparte cómo te sientes o qué te preocupa."


def resolve_text_from_argv() -> str | None:
    if len(sys.argv) > 1:
        return " ".join(sys.argv[1:]).strip()
    return None


def main() -> int:
    print(banner())
    print(welcome())
    try:
        text = resolve_text_from_argv()
        if not text:
            text = get_user_input("Escribe tu situación: ")
        if not text:
            print("No se recibió texto. Intenta de nuevo.")
            return 1
        label = analyze_sentiment(text)
        message = create_message(label, text)
        print("\n" + "—" * 48)
        print(message)
        print("—" * 48 + "\n")
        return 0
    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario.")
        return 130
    except Exception as exc:
        print(f"Ocurrió un error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

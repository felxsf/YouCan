# You Can — CLI motivacional (ES/EN)

Aplicación de consola que recibe cómo te sientes, analiza el sentimiento (negativo, neutral, positivo) y responde con un mensaje motivacional corto, claro, empático y accionable. Soporta español e inglés.

## Características
- Entrada por consola (interactiva o por argumento).
- Análisis de sentimiento básico sin dependencias externas (ES/EN).
- Mensajes breves, humanos y sin clichés, con una acción concreta.
- Estructura modular preparada para futuras integraciones de IA.
- Banderas CLI: idioma, estilo de salida, modo de ejecución y banner.

## Requisitos
- Python 3.10+
- Sistema operativo: Windows, macOS o Linux

## Instalación
No requiere instalación. Clona o descarga este repositorio y usa Python directamente.

## Uso
- Modo con argumento (recomendado para pruebas):
  
  ```bash
  # Windows
  python you_can\main.py "Me siento bloqueado y con ansiedad, pero quiero avanzar"
  
  # macOS/Linux
  python you_can/main.py "Me siento bloqueado y con ansiedad, pero quiero avanzar"
  ```

- Modo interactivo (solicita input):
  
  ```bash
  python you_can\main.py
  ```

### Opciones CLI
- `--lang es|en`: idioma de mensajes y análisis (por defecto: `es`).
- `--mode interactive|arg`: modo de entrada (`interactive` pide input si no se pasa texto; `arg` solo usa argumentos).
- `--style minimal|bonito`: formato de salida (`bonito` incluye banner y separadores; `minimal` solo el mensaje).
- `--no-banner`: oculta el banner cuando el estilo es `bonito`.
- `text`: texto libre como argumentos al final.

### Ejemplos
- Español, con estilo bonito y argumento:
  ```bash
  python you_can\main.py --mode arg --lang es "Estoy muy motivado y con confianza, listo para avanzar"
  ```
- Inglés, estilo minimal:
  ```bash
  python you_can\main.py --mode arg --lang en --style minimal "I feel very anxious but I want to make progress"
  ```
- Interactivo en español, sin banner:
  ```bash
  python you_can\main.py --mode interactive --lang es --no-banner
  ```

### Ejemplo de salida
```
════════════════════════════════════════════════
  You Can
════════════════════════════════════════════════

Bienvenido. Comparte cómo te sientes o qué te preocupa.

————————————————————————————————————————————————
Aunque hoy pese, tu valor no depende de este momento. No estás solo en esto. Respira profundo tres veces y escribe una cosa manejable para hoy.
————————————————————————————————————————————————
```

## Estructura del proyecto
```
you_can/
├── main.py               # Punto de entrada y flujo CLI
├── input_handler.py      # Captura y validación del input
├── sentiment.py          # Análisis de sentimiento (heurístico)
├── motivator.py          # Generación de mensaje motivacional
└── data/
    └── messages.json     # Mensajes base por sentimiento e idioma
```

## Diseño y lógica
1. Captura input del usuario (argumento CLI o entrada interactiva).
2. Analiza el sentimiento con una heurística ligera (ES/EN), incluyendo negaciones, intensificadores y emojis.
3. Selecciona un mensaje base desde `messages.json` según idioma y tono; añade una acción concreta.
4. Muestra el resultado en consola con formato claro.

## Personalización
- Mensajes: edita `you_can/data/messages.json` para ajustar el tono y el idioma:
  ```json
  {
    "es": { "negative": [...], "neutral": [...], "positive": [...] },
    "en": { "negative": [...], "neutral": [...], "positive": [...] }
  }
  ```
- Palabras clave: amplía listas en `you_can/sentiment.py` para mejorar el análisis en ES/EN.
- Formato de salida: usa `--style minimal|bonito` y `--no-banner` o modifica el banner/separadores en `you_can/main.py`.

## Manejo de errores
- Interrupciones con `Ctrl+C` y fin de archivo (`EOF`) se gestionan con mensajes claros.
- Validación básica del texto (sanitización y chequeo de vacío).

## Roadmap y extensiones
- Integración opcional con IA (OpenAI/Azure OpenAI) para generar mensajes dinámicos.
- Argumentos CLI adicionales: `--provider`, `--no-banner`, `--lang`.
- Empaquetado como CLI (`pip install youcan`): crear `pyproject.toml`, entry point `console_scripts`.
- Tests unitarios para `sentiment.py` y `motivator.py`.

## Guía rápida para contribuir
- Requisitos: Python 3.10+ y conocimiento básico de CLI en Python.
- Estándares:
  - Mantén la modularidad y evita dependencias innecesarias.
  - Prioriza mensajes breves (2–4 frases), humanos y sin clichés.
  - Conserva el tono: empático, realista y enfocado en progreso.
- Flujo sugerido:
  1. Crea una rama: `feature/...`, `fix/...` o `chore/...`.
  2. Prueba la app con ejemplos negativos/neutral/positivos.
  3. Implementa cambios en el módulo correspondiente:
     - `sentiment.py`: amplía palabras/reglas sin romper el flujo.
     - `motivator.py`: añade acciones concretas y selecciona mensajes.
     - `data/messages.json`: agrega mensajes por tono (4–6 por categoría).
  4. Valida manualmente:
     - Negativo: `python you_can/main.py "Me siento bloqueado y ansioso"`
     - Neutral: `python you_can/main.py "Estoy normal, sin mucha emoción"`
     - Positivo: `python you_can/main.py "Me siento motivado y con ganas"`
  5. Actualiza documentación si cambian uso/estructura.
  6. Abre un PR con:
     - Descripción breve del objetivo y cambios.
     - Cómo probar (comandos y ejemplos de entrada/salida).
     - Impacto esperado y áreas tocadas.

## Licencia
Pendiente de definir por el autor del proyecto.

# Roboto Tele Bot — Development Blueprint

You are an expert backend engineer specializing in asynchronous Python and the `python-telegram-bot` (v20+) ecosystem. You are assisting me in refactoring and expanding this Telegram Copy Bot codebase.

## 📁 Project Architecture & Context
- **Root Directory:** Contains `main.py` (current monolithic entry point) and `GEMINI.md`.
- **Target Architecture:** We are actively moving logic out of `main.py` into modular components inside the `bot/handlers/` directory.
- **Environment:** Running inside a Python local virtual environment (`venv/`). Always ignore `venv/` when analyzing code context.

## ⚙️ Development & Design Principles

### 1. Separation of Concerns (SoC)
- `main.py` must only handle application initialization, configuration loading, and handler registration.
- All callback functions, command logic, and inline query code must be isolated into descriptive modules inside `bot/handlers/` (e.g., `start.py`, `text.py`, `callbacks.py`, `inline.py`).

### 2. Python & Library Standards
- **Async/Await:** Strict usage of modern `asyncio` patterns. All handler signatures must match `async def func(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None`.
- **Type Hinting:** Always include explicit type hints for function arguments and return types.
- **Telegram Limits:** Remember that `callback_data` has a strict 64-byte limit. Keep payload keys short (e.g., our current 8-character UUID slice).

### 3. Output Requirements
- When suggesting refactors, provide clean, modular snippets that fit into the `bot/handlers/` structure.
- Always provide a brief architectural justification for structural modifications.
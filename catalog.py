import json
import sys
from pathlib import Path

from paths import CONFIG_DIR, USER_GAMES_FILE


def _bundled_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent


def load_default_catalog() -> list[dict]:
    path = _bundled_root() / "games.json"
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_user_catalog() -> list[dict]:
    if not USER_GAMES_FILE.exists():
        return []
    with open(USER_GAMES_FILE, encoding="utf-8") as f:
        return json.load(f)


def save_user_catalog(games: list[dict]) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(USER_GAMES_FILE, "w", encoding="utf-8") as f:
        json.dump(games, f, ensure_ascii=False, indent=2)


def full_catalog() -> list[dict]:
    seen: set[str] = set()
    merged: list[dict] = []
    for g in load_default_catalog() + load_user_catalog():
        if g["id"] in seen:
            continue
        seen.add(g["id"])
        merged.append(g)
    return merged

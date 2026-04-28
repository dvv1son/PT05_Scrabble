from pathlib import Path
import json


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def load_words():
    path = DATA_DIR / "words.txt"

    if not path.exists():
        raise FileNotFoundError(f"Не найден файл словаря: {path}")

    text = path.read_text(encoding="utf-8")

    return {
        line.strip().replace("ё", "е").replace("Ё", "Е").upper()
        for line in text.splitlines()
        if line.strip()
    }


def load_letters():
    path = DATA_DIR / "letters.json"

    if not path.exists():
        raise FileNotFoundError(f"Не найден файл очков букв: {path}")

    with path.open("r", encoding="utf-8") as file:
        raw = json.load(file)

    result = {}

    for letter, value in raw.items():
        letter = letter.upper()

        if isinstance(value, dict):
            result[letter] = int(value.get("score", 0))
        else:
            result[letter] = int(value)

    return result


def load_rules():
    path = DATA_DIR / "rules.txt"

    if not path.exists():
        raise FileNotFoundError(f"Не найден файл правил: {path}")

    return path.read_text(encoding="utf-8")


def load_board_layout():
    path = DATA_DIR / "board_layout.json"

    if not path.exists():
        raise FileNotFoundError(f"Не найден файл раскладки поля: {path}")

    with path.open("r", encoding="utf-8") as file:
        raw = json.load(file)

    result = {}

    for bonus_name, coords in raw.items():
        result[bonus_name] = [tuple(item) for item in coords]

    return result
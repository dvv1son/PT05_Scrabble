import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


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
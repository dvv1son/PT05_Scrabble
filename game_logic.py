import json
import random
from dataclasses import dataclass
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

BOARD_SIZE = 10
RACK_SIZE = 7

DEMO_LETTER_POOL = list(
    "АААААББВВГГДДЕЕЕЕЕЖЗЗИИИИЙККЛЛММННННОООООППРРРСССТТТУУУФХЦЧШЩЫЭЮЯЬ"
)


@dataclass
class CellState:
    row: int
    col: int
    letter: str = ""

    @property
    def is_empty(self):
        return self.letter == ""


def create_board():
    board = []

    for row in range(BOARD_SIZE):
        board_row = []

        for col in range(BOARD_SIZE):
            board_row.append(CellState(row=row, col=col))

        board.append(board_row)

    return board


def clear_board_state(board):
    for row in board:
        for cell in row:
            cell.letter = ""


def normalize_word(word):
    return word.strip().replace("ё", "е").replace("Ё", "Е").upper()


def load_words():
    path = DATA_DIR / "words.txt"

    if not path.exists():
        raise FileNotFoundError(f"Не найден файл словаря: {path}")

    with path.open("r", encoding="utf-8") as file:
        return {
            normalize_word(line)
            for line in file
            if line.strip()
        }


def load_letter_scores():
    path = DATA_DIR / "letters.json"

    if not path.exists():
        raise FileNotFoundError(f"Не найден файл очков букв: {path}")

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return {
        normalize_word(letter): int(score)
        for letter, score in data.items()
    }


def random_letters():
    return [
        random.choice(DEMO_LETTER_POOL)
        for _ in range(RACK_SIZE)
    ]


def calculate_word_score(word, letter_scores):
    score = 0

    for letter in word:
        score += letter_scores.get(letter, 0)

    return score


def format_points(number):
    if 11 <= number % 100 <= 14:
        return f"{number} баллов"

    last_digit = number % 10

    if last_digit == 1:
        return f"{number} балл"

    if last_digit in (2, 3, 4):
        return f"{number} балла"

    return f"{number} баллов"


def get_next_player(current_player):
    if current_player == 1:
        return 2

    return 1
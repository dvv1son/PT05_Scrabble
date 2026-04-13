import json
import random
from dataclasses import dataclass
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

BOARD_SIZE = 15
RACK_SIZE = 7

DEMO_LETTER_POOL = list(
    "АААААББВВГГДДЕЕЕЕЕЖЗЗИИИИЙККЛЛММННННОООООППРРРСССТТТУУУФХЦЧШЩЫЭЮЯЬ"
)


@dataclass
class CellState:
    row: int
    col: int
    bonus: str = "normal"
    letter: str = ""

    @property
    def is_empty(self):
        return self.letter == ""


def build_bonus_map(board_layout):
    bonus_map = {}

    for bonus_name, cells in board_layout.items():
        for row, col in cells:
            bonus_map[(row, col)] = bonus_name

    return bonus_map


def create_board(board_layout=None):
    if board_layout is None:
        board_layout = {}

    bonus_map = build_bonus_map(board_layout)
    board = []

    for row in range(BOARD_SIZE):
        board_row = []

        for col in range(BOARD_SIZE):
            cell = CellState(
                row=row,
                col=col,
                bonus=bonus_map.get((row, col), "normal"),
            )
            board_row.append(cell)

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
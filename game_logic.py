from dataclasses import dataclass
from typing import Optional


BOARD_SIZE = 15
CENTER = (7, 7)

LETTER_BONUSES = {
    "double_letter": 2,
    "triple_letter": 3,
}

WORD_BONUSES = {
    "start": 2,
    "double_word": 2,
    "triple_word": 3,
}


@dataclass
class CellState:
    row: int
    col: int
    bonus: str = "normal"
    letter: str = ""
    owner: Optional[int] = None
    bonus_used: bool = False
    is_preview: bool = False

    @property
    def is_empty(self):
        return self.letter == ""


def build_bonus_map(board_layout):
    bonus_map = {}

    for bonus_name, cells in board_layout.items():
        for row, col in cells:
            bonus_map[(row, col)] = bonus_name

    return bonus_map


def create_board(board_layout):
    bonus_map = build_bonus_map(board_layout)
    board = []

    for row in range(BOARD_SIZE):
        board_row = []

        for col in range(BOARD_SIZE):
            board_row.append(
                CellState(
                    row=row,
                    col=col,
                    bonus=bonus_map.get((row, col), "normal"),
                )
            )

        board.append(board_row)

    return board


def board_has_committed_letters(board):
    for row in board:
        for cell in row:
            if cell.letter and not cell.is_preview:
                return True

    return False


def collect_word_positions(board, row, col, dr, dc):
    while 0 <= row - dr < BOARD_SIZE and 0 <= col - dc < BOARD_SIZE:
        if board[row - dr][col - dc].letter == "":
            break

        row -= dr
        col -= dc

    positions = []

    while 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
        if board[row][col].letter == "":
            break

        positions.append((row, col))

        row += dr
        col += dc

    return positions


def score_word(board, positions, pending_positions, letters_scores):
    total = 0
    word_multiplier = 1

    for row, col in positions:
        cell = board[row][col]
        letter_value = letters_scores.get(cell.letter.upper(), 0)

        if (row, col) in pending_positions and not cell.bonus_used:
            if cell.bonus in LETTER_BONUSES:
                letter_value *= LETTER_BONUSES[cell.bonus]
            elif cell.bonus in WORD_BONUSES:
                word_multiplier *= WORD_BONUSES[cell.bonus]

        total += letter_value

    return total * word_multiplier


def remove_duplicate_words(words_positions):
    unique = []
    seen = set()

    for positions in words_positions:
        key = tuple(positions)

        if key not in seen:
            seen.add(key)
            unique.append(positions)

    return unique


def has_gap_in_row(board, row, min_col, max_col):
    for col in range(min_col, max_col + 1):
        if board[row][col].letter == "":
            return True

    return False


def has_gap_in_col(board, col, min_row, max_row):
    for row in range(min_row, max_row + 1):
        if board[row][col].letter == "":
            return True

    return False


def touches_old_tile(board, pending_positions):
    for row, col in pending_positions:
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr = row + dr
            nc = col + dc

            if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                if board[nr][nc].letter and (nr, nc) not in pending_positions:
                    return True

    return False


def evaluate_move(board, pending_positions, words_set, letters_scores):
    pending_positions = set(pending_positions)

    if not pending_positions:
        return False, "Нужно поставить хотя бы одну букву.", [], 0

    rows = {row for row, _ in pending_positions}
    cols = {col for _, col in pending_positions}

    words_positions = []
    is_first_move = not board_has_committed_letters(board)

    if is_first_move and CENTER not in pending_positions:
        return False, "Первый ход должен проходить через центральную клетку со звездой.", [], 0

    if len(pending_positions) > 1 and len(rows) != 1 and len(cols) != 1:
        return False, "Новые буквы должны стоять в одной строке или одном столбце.", [], 0

    if len(rows) == 1 and len(pending_positions) > 1:
        row = next(iter(rows))
        min_col = min(cols)
        max_col = max(cols)

        if has_gap_in_row(board, row, min_col, max_col):
            return False, "Между буквами есть разрыв.", [], 0

        main_word = collect_word_positions(board, row, min_col, 0, 1)

        if len(main_word) > 1:
            words_positions.append(main_word)

        for r, c in pending_positions:
            cross = collect_word_positions(board, r, c, 1, 0)

            if len(cross) > 1:
                words_positions.append(cross)

    elif len(cols) == 1 and len(pending_positions) > 1:
        col = next(iter(cols))
        min_row = min(rows)
        max_row = max(rows)

        if has_gap_in_col(board, col, min_row, max_row):
            return False, "Между буквами есть разрыв.", [], 0

        main_word = collect_word_positions(board, min_row, col, 1, 0)

        if len(main_word) > 1:
            words_positions.append(main_word)

        for r, c in pending_positions:
            cross = collect_word_positions(board, r, c, 0, 1)

            if len(cross) > 1:
                words_positions.append(cross)

    else:
        row, col = next(iter(pending_positions))

        horizontal = collect_word_positions(board, row, col, 0, 1)
        vertical = collect_word_positions(board, row, col, 1, 0)

        if len(horizontal) > 1:
            words_positions.append(horizontal)

        if len(vertical) > 1:
            words_positions.append(vertical)

        if len(horizontal) == 1 and len(vertical) == 1:
            return False, "Одна буква должна образовывать слово с соседними буквами.", [], 0

    words_positions = remove_duplicate_words(words_positions)

    if not is_first_move and not touches_old_tile(board, pending_positions):
        return False, "Ход должен касаться уже существующих букв на поле.", [], 0

    word_texts = []
    total_score = 0

    for positions in words_positions:
        word = "".join(board[row][col].letter for row, col in positions).upper()

        if word not in words_set:
            return False, f"Слова «{word}» нет в словаре.", [], 0

        word_texts.append(word)
        total_score += score_word(board, positions, pending_positions, letters_scores)

    return True, "", word_texts, total_score

def commit_move(board, pending_positions, player_number):
    for row, col in pending_positions:
        cell = board[row][col]
        cell.is_preview = False
        cell.owner = player_number

        if cell.bonus != "normal":
            cell.bonus_used = True
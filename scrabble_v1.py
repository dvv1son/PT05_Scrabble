import json
import random
import tkinter as tk
from pathlib import Path
from tkinter import messagebox


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

BOARD_SIZE = 10
RACK_SIZE = 7
DEMO_LETTER_POOL = list("АААААББВВГГДДЕЕЕЕЕЖЗЗИИИИЙККЛЛММННННОООООППРРРСССТТТУУУФХЦЧШЩЫЭЮЯЬ")


class ScrabbleMVP:
    def __init__(self, root):
        self.root = root
        self.root.title("Скрэббл — MVP")
        self.root.geometry("1000x700")
        self.root.minsize(900, 650)

        self.words = self.load_words()
        self.letter_scores = self.load_letter_scores()

        self.current_player = 1
        self.scores = {1: 0, 2: 0}
        self.player_letters = {1: [], 2: []}
        self.used_words = set()
        self.next_row = 0
        self.turn_word_checked = False

        self.word_var = tk.StringVar()
        self.current_player_var = tk.StringVar()
        self.score_1_var = tk.StringVar()
        self.score_2_var = tk.StringVar()
        self.letters_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Введите слово и нажмите «Проверить слово».")

        self.board_labels = []

        self.create_widgets()
        self.new_game()

    def normalize_word(self, word):
        return word.strip().replace("ё", "е").replace("Ё", "Е").upper()

    def load_words(self):
        path = DATA_DIR / "words.txt"
        if not path.exists():
            raise FileNotFoundError(f"Не найден файл словаря: {path}")
        with path.open("r", encoding="utf-8") as file:
            return {self.normalize_word(line) for line in file if line.strip()}

    def load_letter_scores(self):
        path = DATA_DIR / "letters.json"
        if not path.exists():
            raise FileNotFoundError(f"Не найден файл очков букв: {path}")
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return {self.normalize_word(letter): int(score) for letter, score in data.items()}

    def create_widgets(self):
        title = tk.Label(
            self.root,
            text="Скрэббл 0.1",
            font=("Arial", 20, "bold"),
            pady=10,
        )
        title.pack()

        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill="both", expand=True)

        left_panel = tk.Frame(main_frame)
        left_panel.pack(side="left", fill="both", expand=True)

        right_panel = tk.Frame(main_frame, width=280, padx=10)
        right_panel.pack(side="right", fill="y")

        info_frame = tk.Frame(left_panel)
        info_frame.pack(fill="x", pady=(0, 10))

        tk.Label(info_frame, text="Текущий игрок:", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w")
        tk.Label(info_frame, textvariable=self.current_player_var, font=("Arial", 12)).grid(row=0, column=1, sticky="w", padx=5)

        tk.Label(info_frame, text="Очки Игрока 1:", font=("Arial", 12, "bold")).grid(row=1, column=0, sticky="w")
        tk.Label(info_frame, textvariable=self.score_1_var, font=("Arial", 12)).grid(row=1, column=1, sticky="w", padx=5)

        tk.Label(info_frame, text="Очки Игрока 2:", font=("Arial", 12, "bold")).grid(row=2, column=0, sticky="w")
        tk.Label(info_frame, textvariable=self.score_2_var, font=("Arial", 12)).grid(row=2, column=1, sticky="w", padx=5)

        board_wrapper = tk.LabelFrame(left_panel, text="Игровое поле 10x10", padx=10, pady=10)
        board_wrapper.pack(fill="both", expand=True)

        board_frame = tk.Frame(board_wrapper)
        board_frame.pack()

        for row in range(BOARD_SIZE):
            row_labels = []
            for col in range(BOARD_SIZE):
                cell = tk.Label(
                    board_frame,
                    text="",
                    width=4,
                    height=2,
                    relief="solid",
                    bd=1,
                    font=("Arial", 12, "bold"),
                    bg="#f5f2ea",
                )
                cell.grid(row=row, column=col, padx=1, pady=1)
                row_labels.append(cell)
            self.board_labels.append(row_labels)

        letters_frame = tk.LabelFrame(left_panel, text="Буквы текущего игрока", padx=10, pady=10)
        letters_frame.pack(fill="x", pady=10)

        tk.Label(
            letters_frame,
            textvariable=self.letters_var,
            font=("Consolas", 16, "bold"),
            anchor="w",
        ).pack(fill="x")

        status_frame = tk.LabelFrame(left_panel, text="Статус", padx=10, pady=10)
        status_frame.pack(fill="x")

        tk.Label(
            status_frame,
            textvariable=self.status_var,
            wraplength=600,
            justify="left",
            anchor="w",
        ).pack(fill="x")

        control_frame = tk.LabelFrame(right_panel, text="Управление", padx=10, pady=10)
        control_frame.pack(fill="x")

        tk.Label(control_frame, text="Введите слово:", font=("Arial", 12, "bold")).pack(anchor="w")
        tk.Entry(control_frame, textvariable=self.word_var, font=("Arial", 14)).pack(fill="x", pady=(5, 10))

        tk.Button(
            control_frame,
            text="Проверить слово",
            font=("Arial", 12),
            command=self.check_word,
            height=2,
        ).pack(fill="x", pady=5)

        tk.Button(
            control_frame,
            text="Завершить ход",
            font=("Arial", 12),
            command=self.end_turn,
            height=2,
        ).pack(fill="x", pady=5)

        tk.Button(
            control_frame,
            text="Новая партия",
            font=("Arial", 12),
            command=self.new_game,
            height=2,
        ).pack(fill="x", pady=5)

    def random_letters(self):
        return [random.choice(DEMO_LETTER_POOL) for _ in range(RACK_SIZE)]

    def calculate_word_score(self, word):
        score = 0
        for letter in word:
            score += self.letter_scores.get(letter, 0)
        return score

    def format_points(self, number):
        if 11 <= number % 100 <= 14:
            return f"{number} баллов"
        last_digit = number % 10
        if last_digit == 1:
            return f"{number} балл"
        if last_digit in (2, 3, 4):
            return f"{number} балла"
        return f"{number} баллов"

    def place_word_on_board(self, word):
        if self.next_row >= BOARD_SIZE:
            return False

        start_col = max((BOARD_SIZE - len(word)) // 2, 0)
        for index, letter in enumerate(word):
            self.board_labels[self.next_row][start_col + index]["text"] = letter
        self.next_row += 1
        return True

    def update_labels(self):
        self.current_player_var.set(f"Игрок {self.current_player}")
        self.score_1_var.set(str(self.scores[1]))
        self.score_2_var.set(str(self.scores[2]))
        self.letters_var.set("   ".join(self.player_letters[self.current_player]))

    def clear_board(self):
        for row in self.board_labels:
            for cell in row:
                cell.config(text="")

    def new_game(self):
        self.current_player = 1
        self.scores = {1: 0, 2: 0}
        self.player_letters = {
            1: self.random_letters(),
            2: self.random_letters(),
        }
        self.used_words = set()
        self.next_row = 0
        self.turn_word_checked = False
        self.word_var.set("")
        self.status_var.set("Новая партия началась. Ходит Игрок 1.")
        self.clear_board()
        self.update_labels()

    def check_word(self):
        if self.turn_word_checked:
            messagebox.showwarning(
                "Ход уже сделан",
                "В этом ходу слово уже принято. Нажмите «Завершить ход».",
            )
            return

        word = self.normalize_word(self.word_var.get())

        if not word:
            messagebox.showwarning("Пустой ввод", "Введите слово перед проверкой.")
            return

        if len(word) < 2:
            messagebox.showwarning("Слишком короткое слово", "Слово должно содержать минимум 2 буквы.")
            return

        if len(word) > BOARD_SIZE:
            messagebox.showwarning(
                "Слишком длинное слово",
                f"Для этой MVP-версии длина слова не должна превышать {BOARD_SIZE} букв.",
            )
            return

        if word in self.used_words:
            messagebox.showwarning("Слово уже было", "Это слово уже использовалось в текущей партии.")
            return

        if word not in self.words:
            messagebox.showerror("Слова нет в словаре", f"Слово «{word}» не найдено в data/words.txt.")
            self.status_var.set(f"Слово «{word}» отклонено. Попробуйте другое слово.")
            return

        if not self.place_word_on_board(word):
            messagebox.showinfo("Поле заполнено", "На поле больше нет свободных строк. Начните новую партию.")
            return

        score = self.calculate_word_score(word)
        self.scores[self.current_player] += score
        self.used_words.add(word)
        self.player_letters[self.current_player] = self.random_letters()
        self.turn_word_checked = True
        self.status_var.set(
            f"Игрок {self.current_player} сыграл слово «{word}» и получил {self.format_points(score)}."
        )
        self.word_var.set("")
        self.update_labels()

    def end_turn(self):
        if not self.turn_word_checked:
            answer = messagebox.askyesno(
                "Завершить ход без слова?",
                "В этом ходу слово не было принято. Передать ход другому игроку?",
            )
            if not answer:
                return
            self.status_var.set(f"Игрок {self.current_player} пропустил ход.")

        self.current_player = 2 if self.current_player == 1 else 1
        self.turn_word_checked = False
        self.word_var.set("")
        self.update_labels()
        if "пропустил ход" not in self.status_var.get():
            self.status_var.set(f"Теперь ходит Игрок {self.current_player}.")


def main():
    root = tk.Tk()
    app = ScrabbleMVP(root)
    root.mainloop()


if __name__ == "__main__":
    main()

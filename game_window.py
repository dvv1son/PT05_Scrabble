import random
import tkinter as tk
from tkinter import messagebox

from game_logic import BOARD_SIZE, commit_move, create_board, evaluate_move


CELL_SIZE = 39
HEADER_SIZE = 28
BOARD_CANVAS_SIZE = HEADER_SIZE + BOARD_SIZE * CELL_SIZE

BONUS_VIEW = {
    "normal": {
        "text": "",
        "bg": "#efe6d6",
        "fg": "#2f2f2f",
    },
    "double_letter": {
        "text": "2Б",
        "bg": "#8fcaf0",
        "fg": "#12344d",
    },
    "triple_letter": {
        "text": "3Б",
        "bg": "#4c8bea",
        "fg": "white",
    },
    "double_word": {
        "text": "2С",
        "bg": "#e9a8bd",
        "fg": "#5e1b2c",
    },
    "triple_word": {
        "text": "3С",
        "bg": "#ee6666",
        "fg": "white",
    },
    "start": {
        "text": "★",
        "bg": "#f2c744",
        "fg": "#4f3d00",
    },
}


class GameWindow(tk.Frame):
    def __init__(self, master, app, words, letters_scores, board_layout):
        super().__init__(master, bg="#f7f7f3")

        self.app = app
        self.words = words
        self.letters_scores = letters_scores
        self.board = create_board(board_layout)

        self.current_player = 0

        self.players = [
            {
                "name": "Игрок 1",
                "score": 0,
                "rack": [],
            },
            {
                "name": "Игрок 2",
                "score": 0,
                "rack": [],
            },
        ]

        self.bag = self.create_letter_bag()
        self.pending_tiles = {}
        self.selected_rack_index = None

        self.rack_buttons = []

        self.current_player_var = tk.StringVar()
        self.score_var = tk.StringVar()
        self.selected_var = tk.StringVar()
        self.bag_var = tk.StringVar()

        self.board_canvas = None

        self.start_game()
        self.create_widgets()
        self.refresh_all()

    def start_game(self):
        for player_index in range(2):
            self.players[player_index]["score"] = 0
            self.players[player_index]["rack"] = []
            self.refill_rack(player_index)

    def create_letter_bag(self):
        bag = []

        for letter, score in self.letters_scores.items():
            if score <= 1:
                count = 8
            elif score <= 2:
                count = 6
            elif score <= 3:
                count = 4
            elif score <= 5:
                count = 2
            else:
                count = 1

            bag.extend([letter] * count)

        random.shuffle(bag)
        return bag

    def refill_rack(self, player_index):
        rack = self.players[player_index]["rack"]

        while len(rack) < 7:
            rack.append("")

        for i in range(7):
            if rack[i] == "" and self.bag:
                rack[i] = self.bag.pop()

    def create_widgets(self):
        title = tk.Label(
            self,
            text="Скрэббл",
            font=("Segoe UI", 18, "bold"),
            bg="#f7f7f3",
            fg="#063f25",
        )
        title.pack(pady=(8, 4))

        content = tk.Frame(self, bg="#f7f7f3")
        content.pack(fill="both", expand=False, padx=12, pady=4)

        left_part = tk.Frame(content, bg="#f7f7f3")
        left_part.pack(side="left", padx=(0, 12), pady=0)

        right_part = tk.Frame(
            content,
            bg="#ffffff",
            width=250,
            height=460,
            bd=1,
            relief="groove",
        )
        right_part.pack(side="right", fill="y")
        right_part.pack_propagate(False)

        self.create_board_canvas(left_part)
        self.create_side_panel(right_part)
        self.create_rack_panel()

    def create_board_canvas(self, parent):
        self.board_canvas = tk.Canvas(
            parent,
            width=BOARD_CANVAS_SIZE,
            height=BOARD_CANVAS_SIZE,
            bg="#f7f7f3",
            highlightthickness=0,
        )
        self.board_canvas.pack()

        self.board_canvas.bind("<Button-1>", self.on_canvas_click)

    def create_side_panel(self, side):
        panel_inner = tk.Frame(side, bg="#ffffff")
        panel_inner.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(
            panel_inner,
            textvariable=self.current_player_var,
            font=("Segoe UI", 13, "bold"),
            bg="#ffffff",
            wraplength=220,
            justify="left",
        ).pack(anchor="w", pady=(0, 16))

        tk.Label(
            panel_inner,
            text="Счёт",
            font=("Segoe UI", 12, "bold"),
            bg="#ffffff",
        ).pack(anchor="w")

        tk.Label(
            panel_inner,
            textvariable=self.score_var,
            font=("Segoe UI", 11),
            bg="#ffffff",
            justify="left",
            wraplength=220,
        ).pack(anchor="w", pady=(4, 16))

        tk.Label(
            panel_inner,
            text="Выбранная буква",
            font=("Segoe UI", 12, "bold"),
            bg="#ffffff",
        ).pack(anchor="w")

        tk.Label(
            panel_inner,
            textvariable=self.selected_var,
            font=("Segoe UI", 11),
            bg="#ffffff",
            justify="left",
            wraplength=220,
        ).pack(anchor="w", pady=(4, 16))

        tk.Label(
            panel_inner,
            textvariable=self.bag_var,
            font=("Segoe UI", 10),
            bg="#ffffff",
            wraplength=220,
        ).pack(anchor="w", pady=(0, 16))

        button_style = {
            "font": ("Segoe UI", 10),
            "height": 2,
            "bg": "#f8f8f8",
            "activebackground": "#e7f2ec",
            "wraplength": 210,
            "justify": "center",
        }

        tk.Button(
            panel_inner,
            text="Проверить и подтвердить ход",
            command=self.confirm_move,
            **button_style,
        ).pack(fill="x", pady=4)

        tk.Button(
            panel_inner,
            text="Сбросить размещение",
            command=self.cancel_pending_move,
            **button_style,
        ).pack(fill="x", pady=4)

        tk.Button(
            panel_inner,
            text="Обновить буквы",
            command=self.exchange_letters,
            **button_style,
        ).pack(fill="x", pady=4)

        tk.Button(
            panel_inner,
            text="Пропустить ход",
            command=self.skip_turn,
            **button_style,
        ).pack(fill="x", pady=4)

        tk.Button(
            panel_inner,
            text="В главное меню",
            command=self.app.show_menu,
            **button_style,
        ).pack(fill="x", pady=(20, 4))

    def create_rack_panel(self):
        rack_frame = tk.Frame(self, bg="#f7f7f3")
        rack_frame.pack(fill="x", padx=18, pady=(8, 10))

        tk.Label(
            rack_frame,
            text="Буквы текущего игрока:",
            font=("Segoe UI", 11, "bold"),
            bg="#f7f7f3",
        ).pack(side="left", padx=(0, 10))

        self.rack_buttons = []

        for i in range(7):
            btn = tk.Button(
                rack_frame,
                width=5,
                height=2,
                font=("Segoe UI", 12, "bold"),
                bg="#fff2d9",
                activebackground="#f7dfb8",
                command=lambda index=i: self.on_rack_click(index),
            )
            btn.pack(side="left", padx=4)

            self.rack_buttons.append(btn)

    def get_cell_view(self, cell):
        if cell.letter:
            score = self.letters_scores.get(cell.letter.upper(), 0)

            if cell.is_preview:
                bg = "#cfeecd"
            else:
                bg = "#fff2d9"

            return {
                "text": f"{cell.letter}\n{score}",
                "bg": bg,
                "fg": "#1e1e1e",
            }

        return BONUS_VIEW.get(cell.bonus, BONUS_VIEW["normal"])

    def draw_board(self):
        self.board_canvas.delete("all")

        self.draw_headers()
        self.draw_cells()

    def draw_headers(self):
        for col in range(BOARD_SIZE):
            x = HEADER_SIZE + col * CELL_SIZE + CELL_SIZE / 2

            self.board_canvas.create_text(
                x,
                HEADER_SIZE / 2,
                text=str(col + 1),
                font=("Segoe UI", 8, "bold"),
                fill="#1f1f1f",
            )

        for row in range(BOARD_SIZE):
            y = HEADER_SIZE + row * CELL_SIZE + CELL_SIZE / 2
            row_name = chr(ord("A") + row)

            self.board_canvas.create_text(
                HEADER_SIZE / 2,
                y,
                text=row_name,
                font=("Segoe UI", 8, "bold"),
                fill="#1f1f1f",
            )

    def draw_cells(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                cell = self.board[row][col]
                view = self.get_cell_view(cell)

                x1 = HEADER_SIZE + col * CELL_SIZE
                y1 = HEADER_SIZE + row * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                self.board_canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=view["bg"],
                    outline="#a99f91",
                    width=1,
                )

                text = view["text"]

                if text:
                    if cell.letter:
                        font = ("Segoe UI", 10, "bold")
                    else:
                        font = ("Segoe UI", 8, "bold")

                    self.board_canvas.create_text(
                        (x1 + x2) / 2,
                        (y1 + y2) / 2,
                        text=text,
                        font=font,
                        fill=view["fg"],
                        justify="center",
                    )

    def on_canvas_click(self, event):
        x = event.x
        y = event.y

        if x < HEADER_SIZE or y < HEADER_SIZE:
            return

        col = int((x - HEADER_SIZE) // CELL_SIZE)
        row = int((y - HEADER_SIZE) // CELL_SIZE)

        if row < 0 or row >= BOARD_SIZE:
            return

        if col < 0 or col >= BOARD_SIZE:
            return

        self.on_board_click(row, col)

    def refresh_board(self):
        self.draw_board()

    def refresh_cell(self, row, col):
        self.draw_board()

    def refresh_rack(self):
        rack = self.players[self.current_player]["rack"]

        for i, btn in enumerate(self.rack_buttons):
            letter = rack[i]

            if letter:
                score = self.letters_scores.get(letter, 0)
                btn.config(
                    text=f"{letter}\n{score}",
                    state="normal",
                )
            else:
                btn.config(
                    text="",
                    state="disabled",
                )

            if self.selected_rack_index == i:
                btn.config(
                    bg="#cfeecd",
                    relief="sunken",
                )
            else:
                btn.config(
                    bg="#fff2d9",
                    relief="raised",
                )

    def refresh_info(self):
        player_name = self.players[self.current_player]["name"]

        self.current_player_var.set(f"Ходит: {player_name}")

        self.score_var.set(
            f"Игрок 1: {self.players[0]['score']}\n"
            f"Игрок 2: {self.players[1]['score']}"
        )

        self.bag_var.set(f"Букв в мешке: {len(self.bag)}")

        if self.selected_rack_index is None:
            self.selected_var.set("не выбрана")
        else:
            rack = self.players[self.current_player]["rack"]
            letter = rack[self.selected_rack_index]

            if letter:
                self.selected_var.set(
                    f"{letter} ({self.letters_scores.get(letter, 0)} очк.)"
                )
            else:
                self.selected_var.set("не выбрана")

    def refresh_all(self):
        self.refresh_board()
        self.refresh_rack()
        self.refresh_info()

    def on_rack_click(self, rack_index):
        rack = self.players[self.current_player]["rack"]

        if rack[rack_index] == "":
            return

        if self.selected_rack_index == rack_index:
            self.selected_rack_index = None
        else:
            self.selected_rack_index = rack_index

        self.refresh_rack()
        self.refresh_info()

    def on_board_click(self, row, col):
        cell = self.board[row][col]

        if (row, col) in self.pending_tiles:
            self.remove_preview_tile(row, col)
            return

        if self.selected_rack_index is None:
            messagebox.showinfo(
                "Скрэббл",
                "Сначала выберите букву на подставке.",
            )
            return

        if not cell.is_empty:
            messagebox.showwarning(
                "Скрэббл",
                "Эта клетка уже занята.",
            )
            return

        rack = self.players[self.current_player]["rack"]
        letter = rack[self.selected_rack_index]

        self.pending_tiles[(row, col)] = {
            "letter": letter,
            "rack_index": self.selected_rack_index,
        }

        rack[self.selected_rack_index] = ""

        cell.letter = letter
        cell.is_preview = True

        self.selected_rack_index = None

        self.refresh_all()

    def remove_preview_tile(self, row, col):
        info = self.pending_tiles.pop((row, col))
        rack = self.players[self.current_player]["rack"]

        rack[info["rack_index"]] = info["letter"]

        cell = self.board[row][col]
        cell.letter = ""
        cell.is_preview = False

        self.refresh_all()

    def cancel_pending_move(self):
        for row, col in list(self.pending_tiles.keys()):
            self.remove_preview_tile(row, col)

        self.selected_rack_index = None
        self.refresh_all()

    def confirm_move(self):
        ok, error_text, words, score = evaluate_move(
            self.board,
            self.pending_tiles.keys(),
            self.words,
            self.letters_scores,
        )

        if not ok:
            messagebox.showwarning("Ход не принят", error_text)
            return

        text = (
            f"Слова: {', '.join(words)}\n"
            f"Очки за ход: {score}\n\n"
            f"Подтвердить ход?"
        )

        if not messagebox.askyesno("Подтверждение хода", text):
            return

        commit_move(
            self.board,
            self.pending_tiles.keys(),
            self.current_player + 1,
        )

        self.players[self.current_player]["score"] += score

        self.pending_tiles.clear()
        self.selected_rack_index = None

        self.refill_rack(self.current_player)

        self.current_player = 1 - self.current_player

        self.refresh_all()

    def exchange_letters(self):
        if self.pending_tiles:
            messagebox.showwarning(
                "Скрэббл",
                "Сначала сбросьте размещённые буквы на поле.",
            )
            return

        if not messagebox.askyesno(
            "Обновить буквы",
            "Заменить все буквы текущего игрока и передать ход?",
        ):
            return

        rack = self.players[self.current_player]["rack"]

        for letter in rack:
            if letter:
                self.bag.append(letter)

        random.shuffle(self.bag)

        self.players[self.current_player]["rack"] = ["" for _ in range(7)]
        self.refill_rack(self.current_player)

        self.selected_rack_index = None
        self.current_player = 1 - self.current_player

        self.refresh_all()

    def skip_turn(self):
        if self.pending_tiles:
            messagebox.showwarning(
                "Скрэббл",
                "Сначала сбросьте размещённые буквы на поле.",
            )
            return

        if messagebox.askyesno("Пропуск хода", "Пропустить ход текущего игрока?"):
            self.selected_rack_index = None
            self.current_player = 1 - self.current_player
            self.refresh_all()
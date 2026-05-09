import tkinter as tk
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


class MenuWindow(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.bg_image = None
        self.create_widgets()

    def create_widgets(self):
        canvas = tk.Canvas(self, width=1000, height=820, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        bg_path = DATA_DIR / "menu_bg.png"

        try:
            self.bg_image = tk.PhotoImage(file=str(bg_path))
            canvas.create_image(500, 410, image=self.bg_image, anchor="center")
        except Exception:
            canvas.configure(bg="#f7f7f3")

        canvas.create_rectangle(310, 170, 690, 620, fill="#f7f7f3", outline="#c9b18c", width=2)

        canvas.create_text(
            502, 232, text="СКРЭББЛ",
            font=("Segoe UI", 48, "bold"),
            fill="#5b3a1a"
        )

        canvas.create_text(
            500, 230, text="СКРЭББЛ",
            font=("Segoe UI", 48, "bold"),
            fill="#063f25"
        )

        btn_style = {
            "font": ("Segoe UI", 18, "bold"),
            "width": 22,
            "height": 2,
            "bg": "#fff8ea",
            "fg": "#063f25",
            "activebackground": "#ead8b8",
            "activeforeground": "#063f25",
            "bd": 2,
            "relief": "groove"
        }

        new_game_btn = tk.Button(
            self, text="НОВАЯ ИГРА",
            command=self.app.start_new_game, **btn_style
        )

        rules_btn = tk.Button(
            self, text="ПРАВИЛА",
            command=self.app.show_rules, **btn_style
        )

        exit_btn = tk.Button(
            self, text="ВЫХОД",
            command=self.app.root.destroy, **btn_style
        )

        canvas.create_window(500, 335, window=new_game_btn)
        canvas.create_window(500, 435, window=rules_btn)
        canvas.create_window(500, 535, window=exit_btn)
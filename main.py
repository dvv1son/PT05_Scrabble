import tkinter as tk
from tkinter import messagebox

from file_manager import load_board_layout, load_letters, load_rules, load_words
from game_window import GameWindow
from menu import MenuWindow


class ScrabbleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Скрэббл")
        self.root.geometry("1000x820")
        self.root.resizable(False, False)

        self.words = set()
        self.letters_scores = {}
        self.rules_text = ""
        self.board_layout = {}
        self.current_frame = None

        if self.load_data():
            self.show_menu()

    def load_data(self):
        try:
            self.words = load_words()
            self.letters_scores = load_letters()
            self.rules_text = load_rules()
            self.board_layout = load_board_layout()
            return True
        except FileNotFoundError as error:
            messagebox.showerror("Ошибка файлов", f"Не найден файл:\n{error}")
            self.root.destroy()
            return False
        except Exception as error:
            messagebox.showerror("Ошибка", f"Ошибка загрузки данных:\n{error}")
            self.root.destroy()
            return False

    def clear_current_frame(self):
        if self.current_frame is not None:
            self.current_frame.destroy()
            self.current_frame = None

    def show_menu(self):
        self.clear_current_frame()
        self.current_frame = MenuWindow(self.root, self)
        self.current_frame.pack(fill="both", expand=True)

    def start_new_game(self):
        self.clear_current_frame()
        self.current_frame = GameWindow(
            self.root,
            app=self,
            words=self.words,
            letters_scores=self.letters_scores,
            board_layout=self.board_layout,
        )
        self.current_frame.pack(fill="both", expand=True)

    def show_rules(self):
        rules_window = tk.Toplevel(self.root)
        rules_window.title("Правила игры")
        rules_window.geometry("650x500")
        rules_window.resizable(False, False)

        text = tk.Text(
            rules_window,
            wrap="word",
            font=("Segoe UI", 11),
            padx=15,
            pady=15,
        )
        text.pack(fill="both", expand=True)

        text.insert("1.0", self.rules_text)
        text.config(state="disabled")

        close_btn = tk.Button(
            rules_window,
            text="Закрыть",
            command=rules_window.destroy,
            font=("Segoe UI", 11),
        )
        close_btn.pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = ScrabbleApp(root)
    root.mainloop()
import tkinter as tk


class EndWindow(tk.Toplevel):
    def __init__(self, master, result, on_new_game, on_back_to_menu, on_exit):
        super().__init__(master)

        self.result = result
        self.on_new_game = on_new_game
        self.on_back_to_menu = on_back_to_menu
        self.on_exit = on_exit

        self.title("Партия завершена")
        self.geometry("520x320")
        self.resizable(False, False)
        self.configure(bg="#f7f7f3")

        self.create_widgets()

    def create_widgets(self):
        tk.Label(
            self,
            text="Партия завершена!",
            font=("Segoe UI", 22, "bold"),
            bg="#f7f7f3",
            fg="#063f25",
        ).pack(pady=(25, 15))

        tk.Label(
            self,
            text=(
                f"Игрок 1: {self.result['score_1']} очков\n"
                f"Игрок 2: {self.result['score_2']} очков\n\n"
                f"{self.result['winner']}"
            ),
            font=("Segoe UI", 16),
            bg="#f7f7f3",
            justify="center",
        ).pack(pady=10)

        buttons = tk.Frame(self, bg="#f7f7f3")
        buttons.pack(pady=20)

        tk.Button(
            buttons,
            text="Новая игра",
            width=14,
            font=("Segoe UI", 10),
            command=self.start_new_game,
        ).pack(side="left", padx=8)

        tk.Button(
            buttons,
            text="В главное меню",
            width=14,
            font=("Segoe UI", 10),
            command=self.back_to_menu,
        ).pack(side="left", padx=8)

        tk.Button(
            buttons,
            text="Выход",
            width=14,
            font=("Segoe UI", 10),
            command=self.exit_app,
        ).pack(side="left", padx=8)

    def start_new_game(self):
        self.destroy()
        self.on_new_game()

    def back_to_menu(self):
        self.destroy()
        self.on_back_to_menu()

    def exit_app(self):
        self.destroy()
        self.on_exit()
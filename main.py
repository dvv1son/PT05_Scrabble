import tkinter as tk

from game_window import GameWindow


class ScrabbleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Скрэббл — MVP")
        self.root.geometry("1000x700")
        self.root.minsize(900, 650)

        self.game_window = GameWindow(self.root)
        self.game_window.pack(fill="both", expand=True)


def main():
    root = tk.Tk()
    app = ScrabbleApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
import tkinter as tk


class MenuWindow(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master, bg="#f7f7f3")
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        container = tk.Frame(self, bg="#f7f7f3")
        container.place(relx=0.5, rely=0.5, anchor="center")

        title = tk.Label(
            container,
            text="СКРЭББЛ",
            font=("Segoe UI", 48, "bold"),
            fg="#063f25",
            bg="#f7f7f3",
        )
        title.pack(pady=(0, 45))

        btn_style = {
            "font": ("Segoe UI", 18, "bold"),
            "width": 22,
            "height": 2,
            "bg": "#ffffff",
            "fg": "#063f25",
            "activebackground": "#e7f2ec",
            "activeforeground": "#063f25",
            "bd": 2,
            "relief": "groove",
        }

        tk.Button(
            container,
            text="+   НОВАЯ ИГРА",
            command=self.app.start_new_game,
            **btn_style,
        ).pack(pady=10)

        tk.Button(
            container,
            text="▰   ПРАВИЛА",
            command=self.app.show_rules,
            **btn_style,
        ).pack(pady=10)

        tk.Button(
            container,
            text="↪   ВЫХОД",
            command=self.app.root.destroy,
            **btn_style,
        ).pack(pady=10)
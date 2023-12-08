import os
from copy import copy

import customtkinter
from CTkMessagebox import CTkMessagebox
from sqlalchemy import select

import config
from db.engines.sync import Session
from db.models.user import User
from windows.utb.frames.main_frame import MainFrame


class LoginFrame:
    def __init__(self, root):
        self.root = root

        self.login_frame = customtkinter.CTkFrame(self.root, corner_radius=15)
        self.login_frame.columnconfigure(0, weight=1)
        self.login_frame.rowconfigure(0, weight=20)
        self.login_frame.rowconfigure((1, 2, 3), weight=10)

        self.main_label = customtkinter.CTkLabel(self.login_frame, text="Обліки УПП", font=('Times New Roman', 25))
        self.main_label.grid(row=0, column=0, padx=(20, 20), pady=(10, 10))

        self.login_entry = customtkinter.CTkEntry(self.login_frame, placeholder_text="Введіть логін")
        self.login_entry.grid(row=1, column=0, padx=(20), pady=(10, 10), sticky="n")

        self.password_entry = customtkinter.CTkEntry(self.login_frame, placeholder_text="Введіть пароль", show="*")
        self.password_entry.bind("<Return>", self.login)
        self.password_entry.grid(row=2, column=0, padx=(20), pady=(10, 10), sticky="n")

        self.login_button = customtkinter.CTkButton(self.login_frame, text="Увійти", command=self.login)
        self.login_button.grid(row=3, column=0, padx=(20), pady=(10, 10), sticky="n")

    def login(self, event=None):
        login = self.login_entry.get()
        password = self.password_entry.get()
        if not login or not password:
            self.error_dialog = CTkMessagebox(master=self.root, title="Помилка", message="Заповніть всі поля")
            return
        qry = select(User).where(User.username == login)
        result = config.session.execute(qry)
        result = result.scalars().first()
        if result and result.password == password:
            result: User
            config.user = copy(result)
            self.root.login_frame.login_frame.grid_forget()

            self.root.height = 780  # Высота окна
            self.root.width = 1400  # Ширина окна
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            x = (screen_width / 2) - (self.root.width / 2)
            y = (screen_height / 2) - (self.root.height / 2)
            self.root.geometry('%dx%d+%d+%d' % (self.root.width, self.root.height, x, y))

            self.root.main_frame = MainFrame(self.root)
            self.root.main_frame.grid(row=0, column=0, padx=(15, 20), pady=(10, 10), sticky="nsew")
        else:
            self.error_dialog = CTkMessagebox(master=self.root, title="Помилка",
                                              message="Невірний логін або пароль", )
            print("")

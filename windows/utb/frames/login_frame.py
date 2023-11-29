import os

import customtkinter
from CTkMessagebox import CTkMessagebox
from sqlalchemy import select

import config
from db.engines.sync import Session
from db.models.user import User


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
        with Session() as session:
            session: sqlalchemy.orm.Session
            qry = select(User).where(User.username == login)
            result = session.execute(qry)
            result = result.scalars().first()
            if result and result.password == password:
                config.user = User(**dict(result))
                self.root.login_frame.login_frame.grid_forget()
                self.root.main_frame.grid(row=0, column=0, padx=(15, 20), pady=(10, 10), sticky="nsew")
            else:
                self.error_dialog = CTkMessagebox(master=self.root, title="Помилка",
                                                  message="Невірний логін або пароль", )
                print("")

import os

import customtkinter
from PIL import Image

from windows.utb.frames.login_frame import LoginFrame
from windows.utb.frames.main_frame import MainFrame


class MainWindow(customtkinter.CTk):
    def __init__(self):

        super().__init__()
        self.resizable(False, False)  # Запрет на изменение размеров окна
        self.title("Обліки УПП")  # Заголовок окна
        self.height = 580  # Высота окна
        self.width = 1200  # Ширина окна

        # Расположение окна в центре экрана вне зависимости от разрешения экрана
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (self.width / 2)
        y = (screen_height / 2) - (self.height / 2)
        self.geometry('%dx%d+%d+%d' % (self.width, self.height, x, y))

        self.main_frame = MainFrame(self)
        self.login_frame = LoginFrame(self)

        self.login_frame.login_frame.grid(row=0, column=0, padx=(500), pady=(170), sticky="nsew")
        self.login_frame.login_frame.after(10, self.login_frame.login_entry.focus)


if __name__ == "__main__":
    customtkinter.set_appearance_mode("Dark")
    app = MainWindow()
    app.mainloop()

import atexit
import os
import sys
from threading import Thread
from time import sleep

import customtkinter

import config
from commonmethods import get_all_users, get_data_for_auto_complete_utb, Utb_raw_to_list
from db.engines.sync import Session
from db.models import Utb
from windows.utb.frames.login_frame import LoginFrame


def get_last_id():
    return config.session.query(Utb.id).order_by(Utb.id.desc()).limit(1).scalar()


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

        self.login_frame = LoginFrame(self)

        self.login_frame.login_frame.grid(row=0, column=0, padx=(500), pady=(170), sticky="nsew")
        self.login_frame.login_frame.after(10, self.login_frame.login_entry.focus)

        thr = Thread(target=self.monitor_id)
        thr.start()

    def monitor_id(self):
        while True:
            if config.is_exit:
                sys.exit()
            id = get_last_id()
            if config.last_id and id > config.last_id:
                config.last_id = id
                last_utb = config.session.query(Utb).get(id)
                last_utb = Utb_raw_to_list(last_utb)
                self.main_frame.tvb.loading_bar.pack(fill="both", expand=True)
                self.main_frame.tvb.add_row_to_tv(last_utb)
                self.main_frame.tvb.loading_bar.pack_forget()
            sleep(5)


def close_program():
    config.session.commit()
    config.session.close()
    config.is_exit = True
    print('Session was closed')
    os._exit(0)


if __name__ == "__main__":
    with Session() as session:
        session.begin()
        session: Session
        config.session = session
        config.last_id = get_last_id()
        customtkinter.set_appearance_mode("Dark")
        config.users = get_all_users()
        config.data_for_complete_utb = get_data_for_auto_complete_utb()
        app = MainWindow()
        app.mainloop()
        atexit.register(close_program)

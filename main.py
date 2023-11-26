import gc

import customtkinter
import sqlalchemy.orm
from sqlalchemy import select

from commonmethods import Utb_raw_to_list
from db.engines.sync import Session
from db.models import Utb
from windows.treeview_builder import TreeViewBuilder
from windows.utb_card_window import UTB_card_Window

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"


class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
        self.label = customtkinter.CTkLabel(self, text="ToplevelWindow")
        self.label.pack(padx=20, pady=20)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.add_car_window = None
        self.search_window = None
        self.show_mode = 'all'
        self.last_qry = None

        self.resizable(False, False)
        self.title("УПП БД")
        height = 580
        width = 1200
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure(0, weight=8)
        self.grid_rowconfigure(0, weight=2)

        self.tabview = customtkinter.CTkTabview(self)
        self.tabview.grid(row=0, column=0, padx=(20, 20), pady=(20, 10), sticky="nsew", columnspan=3)
        self.tabview.add("Укртрансбезпека")
        self.tabview.add("Інший облік")

        self.add_button = customtkinter.CTkButton(master=self, text="Добавить", command=self.add_button_event)
        self.add_button.grid(row=1, column=0, padx=(20, 10), pady=(0, 10), sticky="nsew")

        self.change_button = customtkinter.CTkButton(master=self, text="Изменить", command=self.sidebar_button_event)
        self.change_button.grid(row=1, column=1, padx=(10, 10), pady=(0, 10), sticky="nsew")

        self.delete_button = customtkinter.CTkButton(master=self, text="Удалить", command=self.sidebar_button_event)
        self.delete_button.grid(row=1, column=2, padx=(10, 20), pady=(0, 10), sticky="nsew")

        self.tv = TreeViewBuilder(self.tabview.tab("Укртрансбезпека"), self).tv
        self.tv.pack(fill="both", expand=True)


    def sidebar_button_event(self):
        print("sidebar_button click")

    def add_button_event(self):
        current_tab = self.tabview.get()
        if current_tab == "Укртрансбезпека":
            if self.add_car_window is None or not self.add_car_window.winfo_exists():
                self.add_car_window = UTB_card_Window()
            else:
                self.add_car_window.focus()
            self.add_car_window.in_number_entry.after(100, self.add_car_window.in_number_entry.focus_force)
        elif current_tab == "Інший облік":
            pass

if __name__ == "__main__":
    app = App()

    app.mainloop()

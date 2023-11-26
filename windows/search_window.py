from tkinter import ttk

import customtkinter
from CTkMessagebox import CTkMessagebox
from customtkinter import CTkScrollbar
from sqlalchemy import select

from commonmethods import Utb_raw_to_list
from db.engines.sync import Session
from db.models import Utb

customtkinter.set_appearance_mode("Dark")
class SearchWindowBuilder(customtkinter.CTkToplevel):
    def __init__(self,db_name, column, heading_text):
        super().__init__()
        self.db_name = db_name
        self.column = column
        self.heading_text = heading_text
        self.search_result = None
        self.resizable(False, False)
        self.title("Пошук")
        height = 150
        width = 300
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.grid_rowconfigure((0, 1, 3), weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.main_label = customtkinter.CTkLabel(self, text="Пошук по " + self.heading_text)
        self.main_label.configure(font=("Times New Roman", 20))
        self.main_label.grid(row=0, padx=(20, 20), pady=(20, 10), sticky="nsew")
        self.search_entry = customtkinter.CTkEntry(self)
        self.search_entry.grid(row=1, padx=(20, 20), pady=(5, 5), sticky="new")
        self.search_button = customtkinter.CTkButton(self, text="Пошук", command=self.search)
        self.search_button.grid(row=2, padx=(20, 20), pady=(5, 5), sticky="ew", columnspan=2)
        self.search_entry.bind("<Return>", command=self.search)




    def search(self, event=None):
        with Session() as session:
            try:
                qry = select(self.db_name).where(self.db_name.__table__.c[self.column].like(f'%{self.search_entry.get()}%'))
                res = session.execute(qry)
                result = res.fetchall()
                if len(result) == 0:
                    self.dialogue_window = CTkMessagebox(master=self, title="Помилка", message="Записів не знайдено",)
                    return
                else:
                    self.search_result = Utb_raw_to_list(result)
            except Exception as e:
                self.dialogue_window = CTkMessagebox(master=self, title="Помилка", message=str(e))
                session.rollback()
        self.destroy()
        



if __name__ == "__main__":
    app = SearchWindowBuilder(Utb, 'license_plate', 'ДНЗ авто')
    app.mainloop()
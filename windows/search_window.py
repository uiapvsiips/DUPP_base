from tkinter import ttk

import customtkinter
from customtkinter import CTkScrollbar

customtkinter.set_appearance_mode("Dark")
class SearchWindowBuilder(customtkinter.CTk):
    def __init__(self,db_name, column):
        self.db_name = db_name
        self.column = column
        super().__init__()
        self.resizable(False, False)
        self.title("Пошук")
        height = 300
        width = 300
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.grid_rowconfigure((0, 1, 3), weight=1)
        self.main_label = customtkinter.CTkLabel(self, text="Пошук по " + self.column)
        self.main_label.configure(font=("Times New Roman", 20))
        self.main_label.grid(row=0, column=0, padx=(20, 20), pady=(20, 10), sticky="nsew")
        self.search_entry = customtkinter.CTkEntry(self)
        self.search_entry.grid(row=1, column=0, padx=(20, 20), pady=(5, 5), sticky="nsew")
        self.search_button = customtkinter.CTkButton(self, text="Пошук", command=self.search)
        self.search_button.grid(row=2, column=0, padx=(20, 20), pady=(5, 5), sticky="ew", columnspan=2)

    def search(self):
        self.destroy()

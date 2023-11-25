import sys
from datetime import datetime

import customtkinter
import tkcalendar

customtkinter.set_appearance_mode("Dark")


class Calendar_Window_builder(customtkinter.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.resizable(False, False)
        self.current_datetime = None
        self.title("Оберіть дату")
        height = 300
        width = 300
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 2), weight=9)
        self.grid_rowconfigure(1, weight=1)

        self.main_label = customtkinter.CTkLabel(self, text="Оберіть дату")
        self.main_label.configure(font=("Times New Roman", 20))
        self.main_label.grid(row=0, column=0, columnspan=2, padx=(20, 20), pady=(20, 10), sticky="nsew")

        self.calendar = tkcalendar.Calendar(self)
        self.calendar.grid(row=1, column=0, columnspan=2, padx=(20, 20), pady=(5, 5), sticky="nsew")

        self.button = customtkinter.CTkButton(self, text="Обрати", command=self.get_date)
        self.button.grid(row=2, column=0, padx=(20, 20), pady=(5, 5), sticky="ew", columnspan=2)

    def get_date(self):
        self.current_datetime = datetime.strptime(self.calendar.get_date(), "%m/%d/%y").strftime("%d.%m.%Y")
        self.destroy()


if __name__ == "__main__":
    app = Calendar_Window_builder()
    app.mainloop()
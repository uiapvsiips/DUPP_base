import customtkinter

from windows.Calendar_window import Calendar_Window_builder

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"


class Add_UTB_Window(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Додати авто Укртрансбезпека")
        self.resizable(False, False)
        height = 640
        width = 480
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12), weight=1)

        # Главный лейбл
        self.main_label = customtkinter.CTkLabel(self, text="Додати авто Укртрансбезпека")
        self.main_label.configure(font=("Times New Roman", 20))
        self.main_label.grid(row=0, column=0, columnspan=2, padx=(20, 20), pady=(20, 10), sticky="nwse")

        # Вх.№ label и форма ввода
        self.in_number_label = customtkinter.CTkLabel(self, text="Вх.№:")
        self.in_number_label.configure(font=("Times New Roman", 12), anchor="sw")
        self.in_number_label.grid(row=1, column=0, padx=(20, 20), pady=(5, 5), sticky="sw")

        self.in_number_entry = customtkinter.CTkEntry(self)
        self.in_number_entry.anchor = "nw"
        self.in_number_entry.grid(row=2, column=0, padx=(20, 20), pady=(5, 5), sticky="nw")

        # Дата та час проїзду label и форма ввода
        self.car_going_date_label = customtkinter.CTkLabel(self, text="Дата та час проїзду:")
        self.car_going_date_label.configure(font=("Times New Roman", 12), anchor="sw")
        self.car_going_date_label.grid(row=3, column=0, padx=(20, 20), pady=(5, 5), sticky="sw")

        self.car_going_date_entry = customtkinter.CTkEntry(self)
        self.car_going_date_entry.grid(row=4, column=0, padx=(20, 20), pady=(5, 5), sticky="nw")
        self.car_going_date_entry.bind("<FocusIn>", self.car_going_date_calendar)

        # Місце проїзду label и форма ввода
        self.car_going_place_label = customtkinter.CTkLabel(self, text="Місце проїзду:")
        self.car_going_place_label.configure(font=("Times New Roman", 12), anchor="sw")
        self.car_going_place_label.grid(row=5, column=0, padx=(20, 20), pady=(5, 5), sticky="sw")

        self.car_going_place_entry = customtkinter.CTkEntry(self)
        self.car_going_place_entry.grid(row=6, column=0, padx=(20, 20), pady=(5, 5), sticky="nw")

        # Информація про авто label и форма ввода
        self.car_info_label = customtkinter.CTkLabel(self, text="Інформація про авто:")
        self.car_info_label.configure(font=("Times New Roman", 12), anchor="sw")
        self.car_info_label.grid(row=7, column=0, padx=(20, 20), pady=(5, 5), sticky="sw")

        self.car_info_Textbox = customtkinter.CTkTextbox(self, width=200, height=100,
                                                         fg_color=self.car_going_place_entry.cget('fg_color')[1],
                                                         border_color=self.car_going_place_entry.cget('border_color')[
                                                             1],
                                                         border_width=2)
        self.car_info_Textbox.grid(row=8, column=0, rowspan=2, padx=(20, 20), pady=(5, 5), sticky="nw")

        # Информация о прицепе label и форма ввода
        self.truck_info_label = customtkinter.CTkLabel(self, text="Інформація про причеп:")
        self.truck_info_label.configure(font=("Times New Roman", 12), anchor="sw")
        self.truck_info_label.grid(row=10, column=0, padx=(20, 20), pady=(5, 5), sticky="sw")

        self.truck_info_Textbox = customtkinter.CTkTextbox(self, width=200, height=100,
                                                           fg_color=self.car_going_place_entry.cget('fg_color')[1],
                                                           border_color=self.car_going_place_entry.cget('border_color')[
                                                               1],
                                                           border_width=2)
        self.truck_info_Textbox.grid(row=11, column=0, rowspan=2, padx=(20, 20), pady=(5, 5), sticky="nw")

        # ДНЗ label и форма ввода
        self.license_plate_label = customtkinter.CTkLabel(self, text="ДНЗ:")
        self.license_plate_label.configure(font=("Times New Roman", 12), anchor="sw")
        self.license_plate_label.grid(row=1, column=1, padx=(20, 20), pady=(5, 5), sticky="sw")

        self.license_plate_entry = customtkinter.CTkEntry(self)
        self.license_plate_entry.grid(row=2, column=1, padx=(20, 20), pady=(5, 5), sticky="nw")

        # Примітка label и форма ввода
        self.note_label = customtkinter.CTkLabel(self, text="Примітка:")
        self.note_label.configure(font=("Times New Roman", 12), anchor="sw")
        self.note_label.grid(row=3, column=1, padx=(20, 20), pady=(5, 5), sticky="sw")

        self.note_Textbox = customtkinter.CTkTextbox(self, width=200, height=100,
                                                     fg_color=self.car_going_place_entry.cget('fg_color')[1],
                                                     border_color=self.car_going_place_entry.cget('border_color')[1],
                                                     border_width=2)
        self.note_Textbox.grid(row=4, column=1, rowspan=2, padx=(20, 20), pady=(5, 5), sticky="nswe")

        # Виконавець label и форма ввода
        self.executor_label = customtkinter.CTkLabel(self, text="Виконавець:")
        self.executor_label.configure(font=("Times New Roman", 12), anchor="sw")
        self.executor_label.grid(row=6, column=1, padx=(20, 20), pady=(5, 5), sticky="sw")

        self.executor_entry = customtkinter.CTkEntry(self)
        self.executor_entry.grid(row=7, column=1, padx=(20, 20), pady=(5, 5), sticky="nw")

        # ПІБ Власника/Компанія label и форма ввода
        self.owner_label = customtkinter.CTkLabel(self, text="ПІБ Власника/Компанія:")
        self.owner_label.configure(font=("Times New Roman", 12), anchor="sw")
        self.owner_label.grid(row=8, column=1, padx=(20, 20), pady=(5, 5), sticky="sw")

        self.owner_entry = customtkinter.CTkEntry(self)
        self.owner_entry.grid(row=9, column=1, padx=(20, 20), pady=(5, 5), sticky="nw")

        # Мобільний телефон label и форма ввода
        self.phone_label = customtkinter.CTkLabel(self, text="Мобільний телефон:")
        self.phone_label.configure(font=("Times New Roman", 12), anchor="sw")
        self.phone_label.grid(row=10, column=1, padx=(20, 20), pady=(5, 5), sticky="sw")

        self.phone_entry = customtkinter.CTkEntry(self)
        self.phone_entry.grid(row=11, column=1, padx=(20, 20), pady=(5, 5), sticky="nw")

        # Кнопка додати
        self.add_button = customtkinter.CTkButton(self, text="Додати", command=self.add_car)
        self.add_button.grid(row=13, column=0, columnspan=2, padx=(160), pady=10, sticky="nswe")
        while type(self.focus_get()) == Add_UTB_Window:
            self.in_number_entry.focus_force()
            self.update()

    def add_car(self):
        in_number = self.in_number_entry.get()
        car_going_date = self.car_going_date_entry.get()
        car_going_place = self.car_going_place_entry.get()
        car_info = self.car_info_Textbox.get("0.0", "end")
        truck_info = self.truck_info_Textbox.get("0.0", "end")
        license_plate = self.license_plate_entry.get()
        note = self.note_Textbox.get("0.0", "end")
        executor = self.executor_entry.get()
        owner = self.owner_entry.get()
        phone = self.phone_entry.get()

    def car_going_date_calendar(self, event):
        self.car_going_date_label.focus()
        new_window = Calendar_Window_builder()
        while not new_window.current_datetime:
            new_window.update()
        self.car_going_date_entry.delete(0, "end")
        self.car_going_date_entry.insert(0, new_window.current_datetime)
        self.car_going_place_entry.focus()


if __name__ == "__main__":
    app = Add_UTB_Window()
    app.mainloop()

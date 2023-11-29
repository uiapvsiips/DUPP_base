from datetime import datetime

import CTkMessagebox
import customtkinter
from sqlalchemy import update, delete

import config
from CTkScrollableDropdown import CTkScrollableDropdown
from commonmethods import Utb_raw_to_list
from db.engines.sync import Session
from db.models.utb_card import Utb
from windows.utb.calendar_window import Calendar_Window_builder
from windows.utb.photo_window import UTB_photo_card_Window

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"


class UTB_card_Window(customtkinter.CTkToplevel):
    def __init__(self, mode="add", info=None, item_num=None):
        super().__init__()
        self.calendar_new_window = None
        self.info = info
        self.item_num = item_num
        self.mode = mode
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
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15), weight=1)

        # Главный лейбл
        self.main_label = customtkinter.CTkLabel(self,
                                                 text="Додати авто Укртрансбезпека" if mode == "add" else "Редагувати авто Укртрансбезпека")
        self.main_label.configure(font=("Times New Roman", 20))
        self.main_label.grid(row=0, column=0, columnspan=2, padx=(20, 20), pady=(20, 10), sticky="nwse")

        # Вх.№ label и форма ввода
        self.in_number_label = customtkinter.CTkLabel(self, text="Вх.№:")
        self.in_number_label.configure(font=("Times New Roman", 12), anchor="sw")
        self.in_number_label.grid(row=1, column=0, padx=(20, 20), pady=(5, 5), sticky="sw")

        self.in_number_entry = customtkinter.CTkEntry(self, width=200)
        self.in_number_entry.anchor = "nw"
        self.in_number_entry.grid(row=2, column=0, padx=(20, 20), pady=(5, 5), sticky="nw")

        # Дата та час проїзду label и форма ввода
        self.car_going_date_label = customtkinter.CTkLabel(self, text="Дата та час проїзду:")
        self.car_going_date_label.configure(font=("Times New Roman", 12), anchor="sw")
        self.car_going_date_label.grid(row=3, column=0, padx=(20, 20), pady=(5, 5), sticky="sw")

        self.car_going_date_entry = customtkinter.CTkEntry(self, width=200)
        self.car_going_date_entry.grid(row=4, column=0, padx=(20, 20), pady=(5, 5), sticky="nw")
        self.car_going_date_entry.bind("<FocusIn>", self.car_going_date_calendar)

        # Місце проїзду label и форма ввода + autocomplete
        self.car_going_place_label = customtkinter.CTkLabel(self, text="Місце проїзду:")
        self.car_going_place_label.configure(font=("Times New Roman", 12), anchor="sw")
        self.car_going_place_label.grid(row=5, column=0, padx=(20, 20), pady=(5, 5), sticky="sw")

        self.car_going_place_entry = customtkinter.CTkEntry(self, width=200)
        self.car_going_place_entry.grid(row=6, column=0, padx=(20, 20), pady=(5, 5), sticky="nw")
        self.car_going_place_dropdown = CTkScrollableDropdown(self.car_going_place_entry,
                                                              values=config.data_for_complete_utb['car_going_place'],
                                                              command=self.car_going_place_entry_autocomplete,
                                                              autocomplete=True)
        self.car_going_place_entry.bind("<FocusIn>", self.focus_car_going_place_entry)

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

        self.license_plate_entry = customtkinter.CTkEntry(self, width=200)
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

        self.executor_entry = customtkinter.CTkOptionMenu(self, width=200, dynamic_resizing=False,
                                                          fg_color=self.car_going_place_entry.cget('fg_color')[1],
                                                          values=[user.last_name for user in config.users])
        self.executor_entry.set(config.user.last_name)
        self.executor_entry.grid(row=7, column=1, padx=(20, 20), pady=(5, 5), sticky="nw")

        # ПІБ Власника/Компанія label и форма ввода
        self.owner_label = customtkinter.CTkLabel(self, text="ПІБ Власника/Компанія:")
        self.owner_label.configure(font=("Times New Roman", 12), anchor="sw")
        self.owner_label.grid(row=8, column=1, padx=(20, 20), pady=(5, 5), sticky="sw")

        self.owner_entry = customtkinter.CTkEntry(self, width=200)
        self.owner_entry.grid(row=9, column=1, padx=(20, 20), pady=(5, 5), sticky="nw")
        self.owner_entry_dropdown = CTkScrollableDropdown(self.owner_entry,
                                                          values=[k[0] for k in config.data_for_complete_utb['owner']],
                                                          command=self.owner_entry_autocomplete,
                                                          autocomplete=True)
        self.owner_entry.bind("<FocusIn>", self.focus_owner_entry)

        # Мобільний телефон label и форма ввода
        self.phone_label = customtkinter.CTkLabel(self, text="Мобільний телефон:")
        self.phone_label.configure(font=("Times New Roman", 12), anchor="sw")
        self.phone_label.grid(row=10, column=1, padx=(20, 20), pady=(5, 5), sticky="sw")

        self.phone_entry = customtkinter.CTkEntry(self, width=200)
        self.phone_entry.grid(row=11, column=1, padx=(20, 20), pady=(5, 5), sticky="nw")

        if self.mode == "add":
            # Кнопка додати
            self.add_button = customtkinter.CTkButton(self, text="Додати", command=self.add_car)
            self.add_button.grid(row=13, column=0, columnspan=2, padx=(160), pady=10, sticky="nswe")


        # ______________________________________________________________________________________________________________________________________________________________________________________________________________________________
        # ______________________________________________________________________________________________________________________________________________________________________________________________________________________________

        else:
            self.info: Utb
            if info.add_by_user == config.user or config.user.is_admin:
                # Кнопка редагувати
                self.edit_button = customtkinter.CTkButton(self, text="Редагувати", command=self.edit_car)
                self.edit_button.grid(row=15, column=0, columnspan=1, padx=(20), pady=10, sticky="nswe")
                # Кнопка видалити
                self.delete_button = customtkinter.CTkButton(self, text="Видалити", command=self.delete_car)
                self.delete_button.grid(row=15, column=1, columnspan=1, padx=(20), pady=10, sticky="nswe")

            # Заполнение полей и блокировка элементов для запрета редактирования
            self.in_number_entry.insert(0, int(float(self.info.in_number)) if not self.info.in_number.isdigit() else self.info.in_number)
            self.in_number_entry.configure(text_color="dark grey", state="disabled")

            self.car_going_date_entry.insert(0, datetime.strftime(self.info.car_going_date, "%d.%m.%Y"))
            self.car_going_date_entry.configure(text_color="dark grey", state="disabled")

            self.car_going_place_entry.insert(0, self.info.car_going_place)
            self.car_going_place_entry.configure(text_color="dark grey", state="disabled")

            self.car_info_Textbox.insert("0.0", self.info.car_info)
            self.car_info_Textbox.configure(text_color="dark grey", state="disabled")

            self.license_plate_entry.insert(0, self.info.license_plate)
            self.license_plate_entry.configure(text_color="dark grey", state="disabled")

            self.truck_info_Textbox.insert("0.0", self.info.truck_info)
            self.truck_info_Textbox.configure(text_color="dark grey", state="disabled")

            self.note_Textbox.insert("0.0", self.info.note if self.info.note else "-")
            self.note_Textbox.configure(text_color="dark grey", state="disabled")

            # вставить Виконавця в optionmenu
            self.executor_entry.set(self.info.executor)
            self.executor_entry.configure(text_color="dark grey", state="disabled")

            self.owner_entry.insert(0, self.info.owner if self.info.owner else "-")
            self.owner_entry.configure(text_color="dark grey", state="disabled")

            # создать фрейм на 3 строки и 1 колонку
            self.mini_frame = customtkinter.CTkFrame(self, fg_color='transparent')
            self.mini_frame.rowconfigure((0, 1, 2), weight=1)
            self.mini_frame.columnconfigure(0, weight=1)


            self.phone_label = customtkinter.CTkLabel(self.mini_frame, text="Мобільний телефон:")
            self.phone_label.configure(font=("Times New Roman", 12), anchor="sw")
            self.phone_label.grid(row=0, column=0, padx=(0, 20), pady=(5, 5), sticky="sw")

            self.phone_entry = customtkinter.CTkEntry(self.mini_frame, width=200)
            self.phone_entry.grid(row=1, column=0, padx=(0, 20), pady=(5, 5), sticky="nw")

            if self.info.photos:
                self.photo_button = customtkinter.CTkButton(self.mini_frame, text="Фото", command=self.open_photo)
                self.photo_button.grid(row=2, column=0, padx=(0, 20), pady=(10, 5), sticky="swe")

            self.phone_entry.insert(0, self.info.owner_phone if self.info.owner_phone else "-")
            self.phone_entry.configure(text_color="dark grey", state="disabled")
            self.mini_frame.grid(row=10, column=1, rowspan=2, padx=(20), pady=10, sticky="nswe")

            self.add_by_user_label = customtkinter.CTkLabel(self, text="Вніс: " + self.info.add_by_user.last_name)
            self.add_by_user_label.configure(font=("Times New Roman", 12), anchor="sw")
            self.add_by_user_label.grid(row=13, column=0, padx=(20, 20), pady=(5, 0), sticky="sw", columnspan=2 if config.user.is_admin else 1)
            self.add_by_user_dvv_label = customtkinter.CTkLabel(self, text="Дата внесення: " + datetime.strftime(self.info.dvv, "%d.%m.%Y %H:%M"))
            self.add_by_user_dvv_label.configure(font=("Times New Roman", 12), anchor="sw")
            self.add_by_user_dvv_label.grid(row=14, column=0, padx=(20, 20), pady=(0, 5), sticky="sw", columnspan=2 if config.user.is_admin else 1)

            if config.user.is_admin:
                self.kr_by_user_label = customtkinter.CTkLabel(self, text="Корегував: " + self.info.kr_by_user.last_name)
                self.kr_by_user_label.configure(font=("Times New Roman", 12), anchor="sw")
                self.kr_by_user_label.grid(row=13, column=1, padx=(20, 20), pady=(5, 0), sticky="sw")
                self.kr_by_user_dvv_label = customtkinter.CTkLabel(self, text="Дата корегування: " + datetime.strftime(self.info.dkr, "%d.%m.%Y %H:%M"))
                self.kr_by_user_dvv_label.configure(font=("Times New Roman", 12), anchor="sw")
                self.kr_by_user_dvv_label.grid(row=14, column=1, padx=(20, 20), pady=(0, 5), sticky="sw")


    def open_photo(self):
        photo_window = UTB_photo_card_Window(self.info)
        photo_window.after(100, photo_window.lift)



    def owner_entry_autocomplete(self, event=None):
        self.owner_entry.delete(0, "end")
        self.owner_entry.insert(0, event)
        self.phone_entry.delete(0, "end")
        self.phone_entry.insert(0, max([k[1] for k in config.data_for_complete_utb['owner'] if k[0] == event]))
        self.phone_entry.focus()

    def focus_owner_entry(self, event=None):
        if self.owner_entry.get() == "" and self.owner_entry_dropdown.hide:
            self.owner_entry_dropdown.popup()

    def focus_car_going_place_entry(self, event=None):
        if self.car_going_place_entry.get() == "" and self.car_going_place_dropdown.hide:
            self.car_going_place_dropdown.popup()

    def car_going_place_entry_autocomplete(self, event=None):
        self.car_going_place_entry.delete(0, "end")
        self.car_going_place_entry.insert(0, event)
        self.car_info_Textbox.focus()

    def delete_car(self):
        """
        Функция удаления записи из таблицы
        :return:
        """
        with Session() as session:
            session.begin()
            try:
                qry = delete(Utb).where(Utb.id == self.info.id)
                session.execute(qry)
                session.commit()
            except Exception as e:
                session.rollback()
                self.dialogue_window = CTkMessagebox.CTkMessagebox(title="Помилка\n", message=str(e))
            else:
                # Удаление записи из таблицы
                self.master.main_frame.delete_row_from_tv(self.item_num)

                self.destroy()

    def edit_car(self):
        """
        При нажатии кнопки редактирования карточка становится активной для редактирования
        :return:
        """
        self.in_number_entry.configure(state="normal", text_color="white")
        self.car_going_date_entry.configure(state="normal", text_color="white")
        self.car_going_place_entry.configure(state="normal", text_color="white")
        self.car_info_Textbox.configure(state="normal", text_color="white")
        self.license_plate_entry.configure(state="normal", text_color="white")
        self.truck_info_Textbox.configure(state="normal", text_color="white")
        self.note_Textbox.configure(state="normal", text_color="white")
        self.executor_entry.configure(state="normal", text_color="white")
        self.owner_entry.configure(state="normal", text_color="white")
        self.phone_entry.configure(state="normal", text_color="white")

        self.in_number_entry.focus_force()

        # Вместо кнопки редактирования появляется кнопка сохранить
        self.edit_button.grid_forget()
        self.save_button = customtkinter.CTkButton(self, text="Зберегти", command=self.save_car)
        self.save_button.grid(row=15, column=0, columnspan=1, padx=20, pady=10, sticky="nswe")

    def save_car(self):
        """
        Функция сохранения изменений карточки в таблицу
        :return:
        """
        kr_by_user = config.user
        dkr = datetime.now()
        utb = Utb(id=self.info.id, in_number=self.in_number_entry.get(),
                  car_going_date=datetime.strptime(self.car_going_date_entry.get(), "%d.%m.%Y"),
                  car_going_place=self.car_going_place_entry.get(),
                  car_info=self.car_info_Textbox.get("0.0", "end"), license_plate=self.license_plate_entry.get(),
                  truck_info=self.truck_info_Textbox.get("0.0", "end"), note=self.note_Textbox.get("0.0", "end"),
                  executor=self.executor_entry.get(), owner=self.owner_entry.get(), owner_phone=self.phone_entry.get(),
                  kr_by_user=kr_by_user, dkr=dkr)
        with Session() as session:
            session.begin()
            try:
                qry = update(Utb).where(Utb.id == utb.id).values(in_number=utb.in_number,
                                                                 car_going_date=utb.car_going_date,
                                                                 car_going_place=utb.car_going_place,
                                                                 car_info=utb.car_info,
                                                                 license_plate=utb.license_plate,
                                                                 truck_info=utb.truck_info,
                                                                 note=utb.note, executor=utb.executor, owner=utb.owner,
                                                                 owner_phone=utb.owner_phone,
                                                                 kr_by_user_id=kr_by_user.id, dkr=dkr)
                session.execute(qry)
                session.commit()
            except Exception as e:
                session.rollback()
                self.dialogue_window = CTkMessagebox.CTkMessagebox(title="Помилка", message=str(e))
            else:
                # Обновление записи в таблице
                total_row = Utb_raw_to_list(utb)
                self.master.main_frame.edit_row_in_tv(self.item_num, total_row)
                self.destroy()

    def add_car(self):
        """
        При нажатии кнопки добавить карточка сохраняется в таблицу
        :return:
        """
        with Session() as session:
            session.begin()
            try:
                in_number = self.in_number_entry.get()
                car_going_date = self.car_going_date_entry.get()
                car_going_place = self.car_going_place_entry.get()
                car_info = self.car_info_Textbox.get("0.0", "end")
                truck_info = self.truck_info_Textbox.get("0.0", "end")
                license_plate = self.license_plate_entry.get()
                note = self.note_Textbox.get("0.0", "end")
                executor = self.executor_entry.get()
                owner = self.owner_entry.get()
                owner_phone = self.phone_entry.get()
                add_user = config.user
                if in_number == "" or car_going_date == "" or car_going_place == "" or car_info == "" or \
                        truck_info == "" or license_plate == "" or note == "" or executor == "" or owner == "" or \
                        owner_phone == "":
                    self.dialogue_window = CTkMessagebox.CTkMessagebox(title="Помилка", message="Заповніть всі поля")
                    return
                utb = Utb(in_number=in_number, car_going_date=car_going_date, car_going_place=car_going_place,
                          car_info=car_info, truck_info=truck_info, license_plate=license_plate, note=note,
                          executor=executor, owner=owner, owner_phone=owner_phone, add_by_user_id=add_user.id,
                          kr_by_user_id=add_user.id)
                session.add(utb)
            except:
                session.rollback()
                self.dialogue_window = CTkMessagebox.CTkMessagebox(title="Помилка", message="Помилка при додаванні")
            else:
                session.commit()

                # Добавление записи в таблицу
                row_to_tv = Utb_raw_to_list(utb)
                self.master.main_frame.add_row_to_tv(row_to_tv)

                self.dialogue_window = CTkMessagebox.CTkMessagebox(title="Успіх", message="Додано")
                self.destroy()

    def car_going_date_calendar(self, event):
        """
        При фокусировке на поле даты проезда авто, вызывается окно календаря
        :param event:
        :return:
        """
        self.car_going_date_label.focus()
        if self.calendar_new_window is None or not self.calendar_new_window.winfo_exists():
            self.calendar_new_window = Calendar_Window_builder()
        else:
            self.calendar_new_window.focus()
        self.calendar_new_window.after(100, self.calendar_new_window.lift)
        self.calendar_new_window.wait_window()

        # После того, как пользователь выбрал дату, заполняем поле даты (удаляем старое значение и добавляем новое)
        # и фокусируемся на следующее поле
        self.car_going_date_entry.delete(0, "end")
        self.car_going_date_entry.insert(0, self.calendar_new_window.chosen_datetime)
        self.car_going_place_entry.focus()


if __name__ == "__main__":
    app = UTB_card_Window()
    app.mainloop()

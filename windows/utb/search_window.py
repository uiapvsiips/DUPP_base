import customtkinter
from CTkMessagebox import CTkMessagebox
from sqlalchemy import select, desc, func

import config
from commonmethods import Utb_raw_to_list
from db.engines.sync import Session
from db.models.utb_card import Utb

customtkinter.set_appearance_mode("Dark")


class SearchWindowBuilder(customtkinter.CTkToplevel):
    """
    Клас для создания окна поиска по определенному полю
    """

    def __init__(self, db_name, column, heading_text):
        # На вход принимает название БД, название колонки, название заголовка столбца при отображении
        super().__init__()
        self.db_name = db_name
        self.column = column
        self.heading_text = heading_text
        self.search_result = None

        self.resizable(False, False)
        self.title("Пошук")

        # Установка размеров окна и его положения
        height = 150
        width = 300
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

        # Конфигурация окна (кол-во строк и столбцов)
        self.grid_rowconfigure((0, 1, 3), weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Главный лейбл
        self.main_label = customtkinter.CTkLabel(self, text="Пошук по " + self.heading_text)
        self.main_label.configure(font=("Times New Roman", 20))
        self.main_label.grid(row=0, padx=(20, 20), pady=(20, 10), sticky="nsew")

        # Поисковая строка (поле ввода)
        if self.column == "executor":
            self.search_entry = customtkinter.CTkOptionMenu(self, width=200, dynamic_resizing=False,
                                                            values=[user.last_name for user in config.users])
            self.search_entry.set(config.user.last_name)
        else:
            self.search_entry = customtkinter.CTkEntry(self)
        self.search_entry.grid(row=1, padx=(20, 20), pady=(5, 5), sticky="new")

        # Кнопка поиска
        self.search_button = customtkinter.CTkButton(self, text="Пошук", command=self.search)
        self.search_button.grid(row=2, padx=(20, 20), pady=(5, 5), sticky="ew", columnspan=2)

        # Обработчик события ввода в поисковую строку и нажатия кнопки
        self.search_entry.bind("<Return>", command=self.search)

    def search(self, event=None):
        """
        Обработчик события ввода в поисковую строку
        :param event:
        :return:
        """
        try:
            last_id = select(Utb).order_by(desc('id')).limit(1)
            last_id = config.session.execute(last_id).fetchone()[0].id
            if self.search_entry.get() == "":
                qry = select(Utb).where(Utb.id <= last_id).order_by(desc('id')).limit(
                    50) if last_id > 0 else select(Utb).where(Utb.id >= last_id).order_by(desc('id')).limit(50)
            else:
                qry = select(self.db_name).where(func.upper(
                    self.db_name.__table__.c[self.column]).like(f'%{self.search_entry.get().upper()}%'),
                                                 Utb.id <= last_id).order_by(desc('id')).order_by(desc(
                    self.db_name.__table__.c[self.column])).limit(50)
            res = config.session.execute(qry)
            result = res.fetchall()

            # Если по заданному критерию ничего не найдено, то выводим сообщение об ошибке
            if len(result) == 0:
                CTkMessagebox(master=self, title="Помилка", message="Записів не знайдено", )
                return

            # Если по заданному критерию найдено несколько записей, то ковертируем в список и присваиваем в
            # переменную, меняем режим отображения на search, а последний запрос главного окна меняем на тот,
            # который выполнился только что
            else:
                self.search_result = Utb_raw_to_list(result)
                config.show_mode = 'search'
                config.last_qry = qry
        # Если произошла ошибка, то выводим сообщение об ошибке и откатываем сессию
        except Exception as e:
            CTkMessagebox(master=self, title="Помилка", message=str(e))
        self.destroy()


if __name__ == "__main__":
    app = SearchWindowBuilder(Utb, 'license_plate', 'ДНЗ авто')
    app.mainloop()

import customtkinter

from windows.treeview_builder import TreeViewBuilder
from windows.utb_card_window import UTB_card_Window

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"


class App(customtkinter.CTk):
    """
    Основное окно приложения
    """

    def __init__(self):
        super().__init__()

        # Переменные для дальнейшей работы
        self.add_car_window = None  # Окно добавления авто
        self.search_window = None  # Окно поиска
        self.show_mode = 'all'  # Режим отображения
        self.last_qry = None  # Последний запрос

        self.resizable(False, False)  # Запрет на изменение размеров окна
        self.title("УПП БД")  # Заголовок окна
        height = 580 # Высота окна
        width = 1200 # Ширина окна

        # Расположение окна в центре экрана вне зависимости от разрешения экрана
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

        # Конфигурация окна 3x2
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure(0, weight=20)
        self.grid_rowconfigure(1, weight=1)

        # Вкладки учетов
        self.tabview = customtkinter.CTkTabview(self)
        self.tabview.grid(row=0, column=0, padx=(20, 20), pady=(20, 10), sticky="nsew", columnspan=3)
        self.tabview.add("Укртрансбезпека")
        self.tabview.add("Інший облік")

        # Кнопки
        self.add_button = customtkinter.CTkButton(master=self, text="Добавить", command=self.add_button_event)
        self.add_button.grid(row=1, column=0, padx=(20, 10), pady=(0, 10), sticky="nsew")

        self.change_button = customtkinter.CTkButton(master=self, text="Изменить", command=self.sidebar_button_event)
        self.change_button.grid(row=1, column=1, padx=(10, 10), pady=(0, 10), sticky="nsew")

        self.delete_button = customtkinter.CTkButton(master=self, text="Удалить", command=self.sidebar_button_event)
        self.delete_button.grid(row=1, column=2, padx=(10, 20), pady=(0, 10), sticky="nsew")

        # Дерево(информация из таблицы)
        self.tv = TreeViewBuilder(self.tabview.tab("Укртрансбезпека"), self).tv
        self.tv.pack(fill="both", expand=True)

    def sidebar_button_event(self):
        print("sidebar_button click")

    def add_button_event(self):
        """
        Открывает окно добавления новой карточки в зависимости от текущей вкладки. Если окно уже открыто, то фокусируется
        на нем. Через 100мс после открытия окна, фокусируется на поле ввода
        :return:
        """
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

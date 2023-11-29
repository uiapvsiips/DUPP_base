import customtkinter

import config
from windows.utb.treeview_builder import TreeViewBuilder
from windows.utb.utb_card_window import UTB_card_Window


class MainFrame(customtkinter.CTkFrame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        # MainFrame на весь родительский контейнер
        self.configure(root, corner_radius=10, height=root.height - 20,
                                                 width=root.width - 30)
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure(0, weight=20)
        self.grid_rowconfigure(1, weight=1)

        # Вкладки учетов
        self.tabview = customtkinter.CTkTabview(self, height=root.height - 60, width=root.width - 30,
                                                corner_radius=20)
        self.tabview.add("Укртрансбезпека")
        self.tabview.add("Інший облік")
        self.tabview.grid(row=0, column=0, padx=(0), pady=(0), sticky="nsew", columnspan=3)

        # Кнопки
        self.add_button = customtkinter.CTkButton(master=self, text="Додати", command=self.add_button_event)
        self.add_button.grid(row=1, column=1, padx=(280), pady=(10), sticky="nsew")

        # Дерево(информация из таблицы)
        self.tvb = TreeViewBuilder(self.tabview.tab("Укртрансбезпека"), self)
        self.tv = self.tvb.tv
        self.tv.pack(fill="both", expand=True)

    def add_row_to_tv(self, row):
        # Добавить запись в начало таблицы
        self.tv.insert('', 0, values=row)
        self.tvb.treeview_sort_column('id', True)

    def delete_row_from_tv(self, row):
        # Удалить запись из таблицы
        self.tv.delete(row)
        self.tvb.treeview_sort_column('id', True)

    def edit_row_in_tv(self, row_to_delete, row_to_add):
        self.tv.delete(row_to_delete)
        self.tv.insert('', 0, values=row_to_add)
        self.tvb.treeview_sort_column('id', True)

    def add_button_event(self):
        """
        Открывает окно добавления новой карточки в зависимости от текущей вкладки. Если окно уже открыто, то фокусируется
        на нем. Через 100мс после открытия окна, фокусируется на поле ввода
        :return:
        """
        current_tab = self.tabview.get()
        if current_tab == "Укртрансбезпека":
            if config.add_car_window is None or not config.add_car_window.winfo_exists():
                config.add_car_window = UTB_card_Window()
            else:
                config.add_car_window.focus()
            config.add_car_window.in_number_entry.after(200, config.add_car_window.in_number_entry.focus_force)
        elif current_tab == "Інший облік":
            pass
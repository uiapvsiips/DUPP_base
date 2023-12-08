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
        # self.tabview.add("Інший облік")
        self.tabview.grid(row=0, column=0, padx=0, pady=0, sticky="nsew", columnspan=3)

        # Кнопки
        self.add_button = customtkinter.CTkButton(master=self, text="Додати", command=self.add_button_event)
        self.add_button.grid(row=1, column=1, padx=280, pady=10, sticky="nsew")

        # Дерево(информация из таблицы)
        self.tabview.tab("Укртрансбезпека").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Укртрансбезпека").grid_rowconfigure(0, weight=1)
        self.tvb = TreeViewBuilder(self.tabview.tab("Укртрансбезпека"), self)
        self.tv = self.tvb.tv

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
            config.add_car_window.in_number_entry.after(300, config.add_car_window.in_number_entry.focus_force)
            config.add_car_window.wait_window()
            if config.add_car_window.total_row:
                self.tvb.add_row_to_tv(config.add_car_window.total_row)
        elif current_tab == "Інший облік":
            pass


if __name__ == '__main__':
    app = MainFrame()
    app.mainloop()
from tkinter import ttk

from sqlalchemy.orm import selectinload

import customtkinter
import sqlalchemy.orm
from customtkinter import CTkScrollbar
from sqlalchemy import select, desc

import config
from commonmethods import Utb_raw_to_list
from config import show_mode
from db.engines.sync import Session
from db.models.utb_card import Utb
from windows.utb.search_window import SearchWindowBuilder
from windows.utb.utb_card_window import UTB_card_Window


class TreeViewBuilder:
    """
    Класс для создания Treeview
    :param root: корневой элемент, в котором создается таблица (вкладка)
    :param master: главное окно приложения
    """

    def __init__(self, root, master):
        super().__init__()
        self.master = master
        self.tv = self.get_treeview_data(root)  # создаем таблицу и заносим ее в переменную
        self.yscrollbar = CTkScrollbar(self.tv, command=self.tv.yview)  # создаем скроллбар
        self.yscrollbar.pack(side="right", fill="y")  # размещаем скроллбар справа
        self.yscrollbar.bind("<Enter>", self.mw_event)  # привязываем событие прокрутки к скроллбару
        self.tv.configure(yscrollcommand=self.yscrollbar.set)  # привязываем скроллбар к таблице
        self.add_info_to_table()  # добавляем информацию в таблицу

    def get_treeview_data(self, root):
        """
        Функция для создания скелета таблицы
        :param root:
        :return:
        """
        # Назначаем стили
        bg_color = root._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"])
        text_color = root._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkLabel"]["text_color"])
        selected_color = root._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkButton"]["fg_color"])

        treestyle = ttk.Style()
        treestyle.theme_use('default')
        treestyle.configure("Treeview", background=bg_color, foreground=text_color, fieldbackground=bg_color,
                            borderwidth=0)
        treestyle.map('Treeview', background=[('selected', bg_color)], foreground=[('selected', selected_color)])
        root.bind("<<TreeviewSelect>>", lambda event: root.focus_set())

        # создаем рамку
        frame_1 = customtkinter.CTkFrame(master=root)
        frame_1.pack(pady=0, padx=0, fill="both", expand=True)

        # создаем таблицу со столбцами, как в базе данных
        treeview = ttk.Treeview(frame_1, show="headings",
                                columns=("id", "number", "in_number", "car_going_date", "car_going_place",
                                         "car_info", "truck_info", "license_plate", "note",
                                         "executor", "owner", "owner_phone"),
                                displaycolumns=("number", "in_number", "car_going_date", "car_going_place",
                                                "car_info", "truck_info", "license_plate", "note",
                                                "executor", "owner", "owner_phone"))
        # добавляем столбцы в таблицу и задаем ширину столбцов, выравнивание и заголовки
        # NUMBER
        treeview.heading("number", text="No", command=lambda: self.treeview_sort_column('number', True))
        treeview.column("number", width=5, anchor="center")

        # IN_NUMBER
        treeview.heading("in_number", text="Вх.№",
                         command=lambda: self.treeview_sort_column('in_number', True))
        treeview.column("in_number", width=30, anchor="center")

        # CAR_GOING_DATE
        treeview.heading("car_going_date", text="Дата та час проїзду",
                         command=lambda: self.treeview_sort_column('car_going_date', True))
        treeview.column("car_going_date", width=50, anchor="center")

        # CAR_GOING_PLACE
        treeview.heading("car_going_place", text="Місце проїзду",
                         command=lambda: self.treeview_sort_column('car_going_place', True))
        treeview.column("car_going_place", width=100, anchor="center")

        # CAR_INFO
        treeview.heading("car_info", text="Інфо про авто", command=lambda: self.treeview_sort_column('car_info', True))
        treeview.column("car_info", width=70, anchor="center")

        # TRUCK_INFO
        treeview.heading("truck_info", text="Інфо про причеп",
                         command=lambda: self.treeview_sort_column('truck_info', True))
        treeview.column("truck_info", width=70, anchor="center")

        # LICENSE_PLATE
        treeview.heading("license_plate", text="ДНЗ Оригінальний",
                         command=lambda: self.treeview_sort_column('license_plate', True))
        treeview.column("license_plate", width=40, anchor="center")

        # NOTE
        treeview.heading("note", text="Примітка", command=lambda: self.treeview_sort_column('note', True))
        treeview.column("note", width=100, anchor="center")

        # EXECUTOR
        treeview.heading("executor", text="Виконавець", command=lambda: self.treeview_sort_column('executor', True))
        treeview.column("executor", width=40, anchor="center")

        # OWNER
        treeview.heading("owner", text="ПІБ Власника/Компанії",
                         command=lambda: self.treeview_sort_column('owner', True))
        treeview.column("owner", width=100, anchor="center")

        # OWNER_PHONE
        treeview.heading("owner_phone", text="м.т.", command=lambda: self.treeview_sort_column('owner_phone', True))
        treeview.column("owner_phone", width=100, anchor="center")

        # добавляем таблицу в окно, выравниваем и размещаем
        treeview.pack(fill="both", expand=True)

        # привязываем событие двойного клика и событие прокрутки к скроллбару
        treeview.bind("<Double-1>", self.OnDoubleClick)
        treeview.bind("<MouseWheel>", self.mw_event)
        return treeview

    def mw_event(self, event):
        """
        Привязываем событие прокрутки к скроллбару и колесика мыши
        :param event:
        :return:
        """
        # если прокрутка вниз до последего элемента
        if self.tv.yview()[1] == 1.0:
            # найти минимальный id
            min_id = min([d for d in [int(self.tv.set(k)['id']) for k in self.tv.get_children('')]])
            # найти последний номер
            last_num = max([d for d in [int(self.tv.set(k)['number']) for k in self.tv.get_children('')]])
            # добавить информацию
            self.add_info_to_table(int(min_id), int(last_num) + 1)

    def OnDoubleClick(self, event):
        """
        Обработка события двойного клика
        :param event:
        :return:
        """

        # Если клик на заголовок таблицы
        if event.widget.identify_region(event.x, event.y) == "heading":

            # Получаем столбец, на который кликнули
            column_number = event.widget.identify_column(event.x).replace("#", "")
            column_name = event.widget["columns"][int(column_number)]
            heading_text = event.widget.heading(column_name, "text")

            # Если клик по первому столбцу, то ничего не происходит
            if heading_text == "No":
                return

            # В ином случае открываем окно поиска. Если окно уже открыто, то просто фокусируем его
            if config.search_window is None or not config.search_window.winfo_exists():
                config.search_window = SearchWindowBuilder(Utb, column_name, heading_text)
            else:
                config.search_window.focus()
            config.search_window.after(1, config.search_window.lift)
            config.search_window.after(100, config.search_window.search_entry.focus)
            config.search_window.wait_window()

            # Если окно закрыто и какая-то информация была найдена, то обновляем таблицу
            if config.search_window.search_result:
                self.tv.delete(*self.tv.get_children())
                for search_result in config.search_window.search_result:
                    self.tv.insert("", "end", values=search_result)
            return

        #______________________________________________________________________________________________________________#

        # Если двойной клик на элемент таблицы
        item_num = self.tv.selection()[0]
        item = self.tv.item(item_num, "values")

        # Открываем сессию базы данных, находим запись, соответствующую выбранному элементу и выводим ее в новое
        # окно
        with Session() as session:
            session: sqlalchemy.orm.Session
            qry = session.query(Utb).where(Utb.id == item[0]).options(selectinload(Utb.photos))
            res = session.execute(qry)
            result = res.scalar()
            if config.add_car_window is None or not config.add_car_window.winfo_exists():
                config.add_car_window = UTB_card_Window(mode='edit', info=result, item_num = item_num)
            else:
                config.add_car_window.focus()
            config.add_car_window.in_number_entry.after(1, config.add_car_window.lift)


    def treeview_sort_column(self, col, reverse):
        """
        Сортировка записей в таблице
        :param col:
        :param reverse:
        :return:
        """

        # Если клик на первый столбец (порядковый номер)
        if col == 'number':
            l = [(self.tv.set(k, 'id'), k) for k in self.tv.get_children('')]
        else:
            # Получаем полный список записей и сортируем
            l = [(self.tv.set(k, col), k) for k in self.tv.get_children('')]
        l = sorted(l, key=lambda x: float(x[0]) if x[0].isdigit() else x[0], reverse=reverse)

        # Обновляем таблицу
        for index, (val, k) in enumerate(l):
            item = self.tv.item(k)['values']
            self.tv.delete(k)
            item[1] = index + 1
            self.tv.insert('', 'end', values=item)

        # На следующий раз ставим сортировку в обратном порядке для текущего столбца
        self.tv.heading(col, command=lambda: self.treeview_sort_column(col, not reverse))

    def add_info_to_table(self, last_id=0, last_num=1):
        """
        Добавление информации в таблицу
        :param last_id:
        :param last_num:
        :return:
        """
        with Session() as session:
            session: sqlalchemy.orm.Session
            session.begin()
            try:
                # Если включен режим отображения всех записей
                if show_mode == 'all':
                    qry = select(Utb).where(Utb.id < last_id).order_by(desc(Utb.id)).limit(
                        50) if last_id > 0 else select(Utb).where(Utb.id > last_id).order_by(desc(Utb.id)).limit(50)
                # Если включен режим отображения записей после поиска
                else:
                    qry = config.last_qry.where(Utb.id < last_id).order_by(desc(Utb.id)).limit(50)
                res = session.execute(qry)
                lst = res.fetchall()
                result = Utb_raw_to_list(lst, position=last_num)
                for i in result:
                    try:
                        self.tv.insert('', 'end', values=i)
                        last_num += 1
                    except:
                        print('Error:', i)
            except Exception as e:
                print(e)
                session.rollback()
            else:
                session.commit()

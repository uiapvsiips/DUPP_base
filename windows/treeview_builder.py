from tkinter import ttk

import customtkinter
import sqlalchemy.orm
from customtkinter import CTkScrollbar
from sqlalchemy import select, desc

from commonmethods import Utb_raw_to_list
from db.engines.sync import Session
from db.models import Utb
from windows.search_window import SearchWindowBuilder
from windows.utb_card_window import UTB_card_Window


class TreeViewBuilder:
    def __init__(self, root, master):
        self.master = master
        self.tv = self.get_treeview_data(root)
        self.yscrollbar = CTkScrollbar(self.tv, command=self.tv.yview)
        self.yscrollbar.pack(side="right", fill="y")
        self.yscrollbar.bind("<Enter>", self.mw_event)
        self.tv.configure(yscrollcommand=self.yscrollbar.set)
        self.add_info_to_table()

    def get_treeview_data(self, root):
        bg_color = root._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"])
        text_color = root._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkLabel"]["text_color"])
        selected_color = root._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkButton"]["fg_color"])

        treestyle = ttk.Style()
        treestyle.theme_use('default')
        treestyle.configure("Treeview", background=bg_color, foreground=text_color, fieldbackground=bg_color,
                            borderwidth=0)
        treestyle.map('Treeview', background=[('selected', bg_color)], foreground=[('selected', selected_color)])
        root.bind("<<TreeviewSelect>>", lambda event: root.focus_set())
        frame_1 = customtkinter.CTkFrame(master=root)
        frame_1.pack(pady=0, padx=0, fill="both", expand=True)
        treeview = ttk.Treeview(frame_1, show="headings",
                                columns=("id", "number", "in_number", "car_going_date", "car_going_place",
                                         "car_info", "truck_info", "license_plate", "note",
                                         "executor", "owner", "owner_phone"),
                                displaycolumns=("number", "in_number", "car_going_date", "car_going_place",
                                                "car_info", "truck_info", "license_plate", "note",
                                                "executor", "owner", "owner_phone"))
        treeview.heading("number", text="No", command=lambda: self.treeview_sort_column('number', True))
        treeview.column("number", width=5, anchor="center")
        treeview.heading("in_number", text="Вх.№",
                         command=lambda: self.treeview_sort_column('in_number', True))
        treeview.column("in_number", width=30, anchor="center")
        treeview.heading("car_going_date", text="Дата та час проїзду",
                         command=lambda: self.treeview_sort_column('car_going_date', True))
        treeview.column("car_going_date", width=50, anchor="center")
        treeview.heading("car_going_place", text="Місце проїзду",
                         command=lambda: self.treeview_sort_column('car_going_place', True))
        treeview.column("car_going_place", width=100, anchor="center")
        treeview.heading("car_info", text="Інфо про авто", command=lambda: self.treeview_sort_column('car_info', True))
        treeview.column("car_info", width=70, anchor="center")
        treeview.heading("truck_info", text="Інфо про причеп",
                         command=lambda: self.treeview_sort_column('truck_info', True))
        treeview.column("truck_info", width=70, anchor="center")
        treeview.heading("license_plate", text="ДНЗ Оригінальний",
                         command=lambda: self.treeview_sort_column('license_plate', True))
        treeview.column("license_plate", width=40, anchor="center")
        treeview.heading("note", text="Примітка", command=lambda: self.treeview_sort_column('note', True))
        treeview.column("note", width=100, anchor="center")
        treeview.heading("executor", text="Виконавець", command=lambda: self.treeview_sort_column('executor', True))
        treeview.column("executor", width=40, anchor="center")
        treeview.heading("owner", text="ПІБ Власника/Компанії",
                         command=lambda: self.treeview_sort_column('owner', True))
        treeview.column("owner", width=100, anchor="center")
        treeview.heading("owner_phone", text="м.т.", command=lambda: self.treeview_sort_column('owner_phone', True))
        treeview.column("owner_phone", width=100, anchor="center")
        treeview.pack(fill="both", expand=True)
        treeview.bind("<Double-1>", self.OnDoubleClick)
        treeview.bind("<MouseWheel>", self.mw_event)
        return treeview

    def mw_event(self, event):
        if self.tv.yview()[1] == 1.0:
            min_id = min([d for d in [int(self.tv.set(k)['id']) for k in self.tv.get_children('')]])
            # найти минимальный id
            last_num = [(self.tv.set(k), k) for k in self.tv.get_children('')][-1][0]['number']
            self.add_info_to_table(int(min_id), int(last_num) + 1)

    def OnDoubleClick(self, event):
        # Если двойной клик на заголовок
        if event.widget.identify_region(event.x, event.y) == "heading":
            column_number = event.widget.identify_column(event.x).replace("#", "")
            column_name = event.widget["columns"][int(column_number)]
            heading_text = event.widget.heading(column_name, "text")
            if heading_text == "No":
                return
            if self.master.search_window is None or not self.master.search_window.winfo_exists():
                self.master.search_window = SearchWindowBuilder(Utb, column_name, heading_text)
            else:
                self.master.search_window.focus()
            self.master.search_window.after(100, self.master.search_window.search_entry.focus_force)
            self.master.search_window.wait_window()
            if self.master.search_window.search_result:
                self.tv.delete(*self.tv.get_children())
                for search_result in self.master.search_window.search_result:
                    self.tv.insert("", "end", values=search_result)
            return
            # Если двойной клик на элемент таблицы
        item_num = self.tv.selection()[0]
        item = self.tv.item(item_num, "values")
        with Session() as session:
            session: sqlalchemy.orm.Session
            qry = session.query(Utb).where(Utb.id == item[0])
            res = session.execute(qry)
            result = res.fetchone()
            car_window = UTB_card_Window(mode='edit', info=result)
            car_window.mainloop()

    def treeview_sort_column(self, col, reverse):
        if col == 'number':
            return
        l = [(self.tv.set(k, col), k) for k in self.tv.get_children('')]
        l = sorted(l, key=lambda x: float(x[0]) if x[0].isdigit() else x[0], reverse=reverse)
        for index, (val, k) in enumerate(l):
            item = self.tv.item(k)['values']
            self.tv.delete(k)
            item[1] = index + 1
            self.tv.insert('', 'end', values=item)
        self.tv.heading(col, command=lambda: self.treeview_sort_column(col, not reverse))

    def add_info_to_table(self, last_id=0, last_num=1):
        with Session() as session:
            session: sqlalchemy.orm.Session
            session.begin()
            try:
                if self.master.show_mode == 'all':
                    qry = select(Utb).where(Utb.id < last_id).order_by(desc(Utb.id)).limit(
                        50) if last_id > 0 else select(Utb).where(Utb.id > last_id).order_by(desc(Utb.id)).limit(50)
                else:
                    qry = self.master.last_qry.where(Utb.id < last_id).order_by(desc(Utb.id)).limit(50)
                res = session.execute(qry)
                lst = res.fetchall()
                result = Utb_raw_to_list(lst, position=last_num)
                for i in result:
                    try:
                        self.tv.insert('', 'end', values=i)
                        last_num += 1
                    except:
                        print('Error:', i)
                self.last_id = result[-1][0]
            except Exception as e:
                session.rollback()
            else:
                session.commit()

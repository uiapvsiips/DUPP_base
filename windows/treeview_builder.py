from tkinter import ttk

import customtkinter
from customtkinter import CTkScrollbar

from windows.search_window import SearchWindowBuilder


class TreeViewBuilder:
    def __init__(self, root):
        self.tv = self.get_treeview_data(root)
        self.yscrollbar = CTkScrollbar(self.tv, command=self.tv.yview)
        self.yscrollbar.pack(side="right", fill="y")
        self.tv.configure(yscrollcommand=self.yscrollbar.set)

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
        treeview.column("owner_phone", width=50, anchor="center")
        treeview.pack(fill="both", expand=True)
        treeview.bind("<Double-1>", self.OnDoubleClick)
        return treeview

    def OnDoubleClick(self, event):
        if event.widget.identify_region(event.x, event.y) == "heading":
            column_number = event.widget.identify_column(event.x).replace("#", "")
            column_name = event.widget["columns"][int(column_number)]
            print(column_name)
            search_window = SearchWindowBuilder('1', column_name)
            search_window.update()
            return
        item_num = self.tv.selection()[0]
        item = self.tv.item(item_num, "values")
        print("you clicked on", list(item))

    def treeview_sort_column(self, col, reverse):
        l = [(self.tv.set(k, col), k) for k in self.tv.get_children('')]
        l.sort(reverse=reverse)
        for index, (val, k) in enumerate(l):
            self.tv.move(k, '', index)
        self.tv.heading(col, command=lambda: self.treeview_sort_column(col, not reverse))

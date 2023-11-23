from tkinter import END

import customtkinter

from test_data import lst
from windows.add_window import Add_Window

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("УПП БД")
        self.geometry(f"{1100}x{580}")

        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure(0, weight=8)
        self.grid_rowconfigure(0, weight=2)

        self.tabview = customtkinter.CTkTabview(self)
        self.tabview.grid(row=0, column=0, padx=(20, 20), pady=(20, 10), sticky="nsew", columnspan=3)
        self.tabview.add("Укртрансбезпека")
        self.tabview.add("Інший облік")

        self.add_button = customtkinter.CTkButton(master=self, text="Добавить", command=self.add_button_event)
        self.add_button.grid(row=1, column=0, padx=(20, 10), pady=(0, 10), sticky="nsew")

        self.change_button = customtkinter.CTkButton(master=self, text="Изменить", command=self.sidebar_button_event)
        self.change_button.grid(row=1, column=1, padx=(10, 10), pady=(0, 10), sticky="nsew")

        self.delete_button = customtkinter.CTkButton(master=self, text="Удалить", command=self.sidebar_button_event)
        self.delete_button.grid(row=1, column=2, padx=(10, 20), pady=(0, 10), sticky="nsew")

        # find total number of rows and
        # columns in list
        total_rows = len(lst)
        total_columns = len(lst[0])

        self.cnv1 = customtkinter.CTkCanvas(master=self.tabview.tab('Укртрансбезпека'))
        self.cnv1.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="NSEW")
        self.cnv1.rowconfigure(0, weight=9)
        self.cnv1.rowconfigure(1, weight=1)
        self.cnv1.columnconfigure(0, weight=9)
        self.cnv1.columnconfigure(1, weight=1)

        self.scb = customtkinter.CTkCanvas(master=self.cnv1)
        self.scb.grid(row=0, column=0, padx=(0, 0), pady=(0, 0))





        self.label = customtkinter.CTkLabel(master=self.scb, text="№", text_color="black")
        self.label.grid(row=0, column=0, padx=(20, 20), pady=(10, 10), sticky="nsew")
        self.label2 = customtkinter.CTkLabel(master=self.scb, text="Вх.№", text_color="black")
        self.label2.grid(row=0, column=1, padx=(20, 20), pady=(10, 10), sticky="nsew")
        self.label3 = customtkinter.CTkLabel(master=self.scb, text="Дата та час проїзду", text_color="black")
        self.label3.grid(row=0, column=2, padx=(20, 20), pady=(10, 10), sticky="nsew")
        self.label4 = customtkinter.CTkLabel(master=self.scb, text="Місце проїзду", text_color="black")
        self.label4.grid(row=0, column=3, padx=(20, 20), pady=(10, 10), sticky="nsew")
        self.label5 = customtkinter.CTkLabel(master=self.scb, text="Інфо про авто", text_color="black")
        self.label5.grid(row=0, column=4, padx=(20, 20), pady=(10, 10), sticky="nsew")
        self.label6 = customtkinter.CTkLabel(master=self.scb, text="Інфо про причеп", text_color="black")
        self.label6.grid(row=0, column=5, padx=(20, 20), pady=(10, 10), sticky="nsew")
        self.label7 = customtkinter.CTkLabel(master=self.scb, text="ДНЗ Оригінальний", text_color="black")
        self.label7.grid(row=0, column=6, padx=(20, 20), pady=(10, 10), sticky="nsew")
        self.label8 = customtkinter.CTkLabel(master=self.scb, text="Примітка", text_color="black")
        self.label8.grid(row=0, column=7, padx=(20, 20), pady=(10, 10), sticky="nsew")
        self.label9 = customtkinter.CTkLabel(master=self.scb, text="Виконавець", text_color="black")
        self.label9.grid(row=0, column=8, padx=(20, 20), pady=(10, 10), sticky="nsew")
        self.label10 = customtkinter.CTkLabel(master=self.scb, text="ПІБ Власника/Компанії", text_color="black")
        self.label10.grid(row=0, column=9, padx=(20, 20), pady=(10, 10), sticky="nsew")
        self.label11 = customtkinter.CTkLabel(master=self.scb, text="м.т.", text_color="black")
        self.label11.grid(row=0, column=10, padx=(20, 20), pady=(10, 10), sticky="nsew")
        self.label12 = customtkinter.CTkLabel(master=self.scb, text="Фото", text_color="black")
        self.label12.grid(row=0, column=11, padx=(20, 20), pady=(10, 10), sticky="nsew")
        for i in range(total_rows):
            for j in range(total_columns):
                self.e = customtkinter.CTkEntry(master=self.scb, fg_color='white',
                                                text_color='black', font=('Arial', 16, 'bold'))
                self.e.grid(row=i + 1, column=j, sticky="nsew", padx=5, pady=5)
                self.e.insert(END, lst[i][j])
                self.e.configure(state='readonly')

        self.xscrollbar = customtkinter.CTkScrollbar(master=self.cnv1,
                                         height=8,
                                         width=0,
                                         border_spacing=0,
                                         fg_color=self._fg_color,
                                         orientation="horizontal",
                                         command=self.scb.xview)
        self.cnv1.configure(yscrollcommand=self.xscrollbar.set)

        self.yscrollbar = customtkinter.CTkScrollbar(master=self.cnv1, width=8,
                                         height=0,
                                         border_spacing=0,
                                         fg_color=self._fg_color,
                                         orientation="vertical",
                                         command=self.cnv1.yview)
        self.cnv1.configure(yscrollcommand=self.yscrollbar.set)

        self.xscrollbar.grid(row=1, column=0, padx=(20, 20), pady=(0, 10), sticky="ewn", columnspan=1)
        self.yscrollbar.grid(row=0, column=1, padx=(0, 20), pady=(20, 10), sticky="nsw", rowspan=1)

        self.cnv1.pack(fill="both", expand=True)
        d=1

    def sidebar_button_event(self):
        print("sidebar_button click")

    def add_button_event(self):
        Add_Window().mainloop()


if __name__ == "__main__":
    app = App()
    app.mainloop()

import customtkinter

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"


class Add_UTB_Window(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Додати авто Укртрансбезпека")
        self.geometry(f"{400}x{800}")
        self.label = customtkinter.CTkLabel(self, text="Додати авто Укртрансбезпека").pack()
        self.label2 = customtkinter.CTkLabel(self, text="Додати авто Укртрансбезпека1").pack()


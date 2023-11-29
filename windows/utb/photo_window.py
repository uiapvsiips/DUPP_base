import base64
from io import BytesIO

import customtkinter
import sqlalchemy.orm
from PIL import Image
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from db.engines.sync import Session
from db.models.utb_card import Utb

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"


class UTB_photo_card_Window(customtkinter.CTkToplevel):
    def __init__(self, utb: Utb):
        super().__init__()
        self.calendar_new_window = None
        self.utb: Utb = utb
        self.title(f"Фотокартки {utb.car_info}")
        self.resizable(False, False)
        self.state("zoomed")
        height = 640
        width = 480
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((0), weight=1)

        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text=f"Фото {self.utb.car_info}")
        self.scrollable_frame.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_switches = []
        row=0
        for i in utb.photos:
            image = Image.open(BytesIO(base64.b64decode(i.photo)))
            photo = customtkinter.CTkImage(dark_image=image, size=(image.width, image.height))
            photo_label = customtkinter.CTkLabel(master=self.scrollable_frame, image=photo, text="")
            photo_label.grid(row=row, column=0, padx=10, pady=(0, 20))
            row+=1


if __name__ == "__main__":
    utb = None
    with Session() as session:
        session: sqlalchemy.orm.Session
        session.begin()
        qry = select(Utb).options(selectinload(Utb.photos))
        res = session.execute(qry)
        result = res.scalar()
        utb = result
    app = UTB_photo_card_Window(utb)
    app.mainloop()

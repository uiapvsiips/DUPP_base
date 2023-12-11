import base64
from copy import copy
from io import BytesIO
from tkinter import filedialog

import customtkinter
from PIL import Image, ImageFont, ImageDraw, ImageTk
from PIL.JpegImagePlugin import JpegImageFile

from db.models import Photo

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"


class ImageObj:
    """
    Класс для хранения информации об объекте изображения
    """

    def __init__(self, path, db_id, photo,base_64):
        self.path = path
        self.db_id = db_id
        self.photo = photo
        self.base_64 = base_64


class AddPhotoWindow(customtkinter.CTkToplevel):
    """
    Окно добавления фото
    """

    def __init__(self, photos: list = None, mode='edit'):
        super().__init__()
        # Настройки окна
        self.title(f"Додати фото")
        self.resizable(False, False)
        height = 640
        width = 480
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

        # Переменные для работы
        self.max_height = 420  # максимальная высота фото в контейнере
        self.max_width = 453  # максимальная ширина фото в контейнере
        self.mode = mode  # режим работы окна (просмотр или редактирование)
        self.photos = photos  # список фото
        self.labels = []  # список лейблов
        self.image_data = []  # список изображений
        self.just_closed = True  # флаг закрытия окна

        # 2 колонки, 3 строки
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=20)
        self.grid_rowconfigure((1, 2), weight=1)

        # Главный фрейм в 0 строке на 2 колонки
        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid(row=0, column=0, columnspan=2, padx=(0, 0), pady=(0, 0), sticky="nsew")

        # Фрейм с прокруткой
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self.main_frame, label_text=f"Фотозображення")
        self.scrollable_frame.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        # Если окно открыто в режиме редактирования
        if self.mode == 'edit':
            # Кнопка выбора фото в первой строке на обе колонки
            self.choose_photo_button = customtkinter.CTkButton(self, text="Обрати фото", command=self.choose_photo)
            self.choose_photo_button.grid(row=1, column=0, padx=(20, 20), pady=5, sticky="sew", columnspan=2)

            # Кнопка добавления фото во второй строке в первой колонке
            self.add_photo_button = customtkinter.CTkButton(self, text="Зберегти", command=self.add_photos)
            self.add_photo_button.grid(row=2, column=0, padx=(20, 10), pady=(5, 10), sticky="ew")

            # Кнопка закрытия во второй строке во второй колонке
            self.close_button = customtkinter.CTkButton(self, text="Очистити", command=self.clear_data)
            self.close_button.grid(row=2, column=1, padx=(10, 20), pady=(5, 10), sticky="ew")
        if self.photos:
            self.choose_photo(self.photos)

    def clear_data(self):
        self.image_data.clear()
        self.display_photos()

    def add_photos(self):
        # закрываем изображения
        self.just_closed = False
        self.destroy()

    def choose_photo(self, photos=None):
        """
        Выбор фото
        :param photos:
        :return:
        """
        # Если на вход не пришли фото, обнуляем список отображаемых изорбажений
        if not self.photos:
            self.image_data = []
        self.focus_force()
        # Если пришли фото то добавляем их в список отображаемых изображений
        if photos:
            for pphoto in photos:
                pphoto: Photo
                image = Image.open(BytesIO(base64.b64decode(pphoto.photo)))
                new_width, new_height = self.get_new_size(*image.size)
                photo = customtkinter.CTkImage(image, size=(new_width, new_height))
                photo_obj = ImageObj(path=None, db_id=pphoto.id, photo=photo, base_64 = None)
                self.image_data.append(photo_obj)
        # В противном случае открываем FileDialog, через который выбираем фото и добавляем их в список отображаемых
        # изображений
        else:
            file_paths = filedialog.askopenfilenames()
            if file_paths:
                for file_path in file_paths:
                    image = Image.open(file_path)
                    base_64 = self.get_right_size_image(file_path)
                    new_width, new_height = self.get_new_size(*image.size)
                    photo = customtkinter.CTkImage(image, size=(new_width, new_height))
                    photo_obj = ImageObj(path=file_path, db_id=None, photo=photo, base_64=base_64)
                    self.image_data.append(photo_obj)

        # Вызываем функцию отображения фото
        self.display_photos()

    def display_photos(self):
        """
        Функция отображения фото
        :return:
        """
        self.focus_force()
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.scrollable_frame.update()

        for label in self.labels:
            label.destroy()
        self.labels.clear()

        for idx, data in enumerate(self.image_data):
            data: ImageObj
            photo_info_frame = self.get_frame_with_photo(data.path, data.photo, idx)
            self.labels.append(photo_info_frame)

    def get_frame_with_photo(self, path, photo, idx):
        photo_info_frame = customtkinter.CTkFrame(self.scrollable_frame)
        photo_info_frame.grid_columnconfigure(0, weight=1)
        photo_info_frame.grid(row=idx, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
        photo_info_frame.configure(border_width=1, corner_radius=0)

        path = customtkinter.CTkLabel(photo_info_frame, text=path, text_color="light blue",
                                      cursor="hand2", wraplength=400)
        path.bind("<Button-1>", lambda event, idx=idx: self.show_image(idx))
        path.grid(row=0, column=0, padx=20, pady=(10, 0), sticky='nsew')

        photo = customtkinter.CTkLabel(photo_info_frame, image=photo, height=photo.cget('size')[1],
                                       width=photo.cget('size')[0], text="")

        if self.mode == 'edit':
            photo.bind("<Enter>", lambda event, idx=idx: self.on_hover(idx))
            photo.bind("<Leave>", lambda event, idx=idx: self.on_leave(idx))
        else:
            photo.bind("<Button-1>", lambda event, idx=idx: self.show_image(idx))
        photo.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="sew")
        return photo_info_frame

    def on_hover(self, idx):
        if self.image_data:
            data = self.image_data[idx]
            data: ImageObj
            image = Image.open(data.path) if data.path else copy(self.image_data[idx].photo._light_image)
            new_width, new_height = self.get_new_size(*image.size)
            image.thumbnail((new_width, new_height))
            darkened_image = Image.new('RGBA', image.size, (0, 0, 0, 100))
            image.paste(darkened_image, (0, 0), darkened_image)
            photo_with_text = self.add_text_overlay(image, "✗")  # 🚽 ✗
            photo_with_text = ImageTk.PhotoImage(photo_with_text)
            self.labels[idx].children.get('!ctklabel2').configure(image=photo_with_text)
            self.labels[idx].children.get('!ctklabel2').bind("<Button-1>",
                                                             lambda event, idx=idx: self.delete_photo(idx))

    def on_leave(self, idx):
        if self.image_data:
            data = self.image_data[idx]
            data: ImageObj
            image = Image.open(data.path) if data.path else copy(self.image_data[idx].photo._light_image)
            new_width, new_height = self.get_new_size(*image.size)
            image.thumbnail((new_width, new_height))
            photo = ImageTk.PhotoImage(image)
            self.labels[idx].children.get('!ctklabel2').configure(image=photo)

    def add_text_overlay(self, image, text):
        draw = ImageDraw.Draw(image)
        path = 'C:\\Windows\\Fonts\\seguiemj.ttf'
        font = ImageFont.truetype(font=path, size=330, encoding='unic')
        text_size = draw.textbbox((0, 0), text, font=font)
        text_position = ((image.width - text_size[2]) // 2, (image.height - text_size[3]) // 2)
        draw.text(text_position, text, fill=('red'), font=font)
        return image

    def delete_photo(self, idx=0):
        self.image_data.pop(idx)
        self.display_photos()

    def get_new_size(self, width, height):
        aspect_ratio = width / height
        if aspect_ratio < 1:
            new_height = self.max_height
            new_width = int(self.max_width * aspect_ratio)
        else:
            new_width = self.max_width
            new_height = int(self.max_height / aspect_ratio)
        return new_width, new_height

    def show_image(self, idx):
        data = self.image_data[idx]
        data: ImageObj
        photo: JpegImageFile = data.photo._light_image
        photo.show()

    def get_right_size_image(self, file_path):
        image = Image.open(file_path)
        if image.size[0] > 4000 or image.size[1] > 4000:
            new_size = (int(image.size[0] // 3), int(image.size[1] // 3))
        elif image.size[0] > 3000 or image.size[1] > 3000:
            new_size = (int(image.size[0] // 2.5), int(image.size[1] // 2.5))
        elif image.size[0] > 2000 or image.size[1] > 2000:
            new_size = (int(image.size[0] // 2), int(image.size[1] // 2))
        else:
            new_size = image.size
        i = 100
        while True:
            with BytesIO() as buffer:
                image = image.resize(new_size, Image.LANCZOS)
                image.save(buffer, format="JPEG", quality=i, optimize=True)
                print('iter. Buffer size: ', len(buffer.getvalue()))
                if len(buffer.getvalue()) < 120000:
                    base_64 =  base64.b64encode(buffer.getvalue())
                    return copy(base_64)
                else:
                    i -= 10

# def main():
#     photo_window = AddPhotoWindow()
#     photo_window.mainloop()
#
#
# if __name__ == "__main__":
#     main()

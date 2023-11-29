# Перенести данные из excel в базу
import base64
import os

from db.engines.sync import Session
from db.models.utb_card import Utb, User, Photo

if not os.environ.get('DB_HOST', None):
    import pythoncom
    import win32com.client as win32


def get_excel_app():
    pythoncom.CoInitialize()
    excel_app = win32.Dispatch("Excel.Application")
    excel_app.Visible = False
    return excel_app


def get_wb(excel, param):
    excel: win32.Dispatch
    workbook = excel.Workbooks.Open(param)
    return workbook


def get_info(wb):
    ws = wb.Worksheets('Лист1')
    used_cells = ws.UsedRange
    rows = used_cells.Rows
    for row in rows:
        if row.Cells(2).Value != None and row.Cells(2).Value != 'Вх. №':
            in_number = row.Cells(2).Value
            car_going_date = row.Cells(3).Value
            car_going_place = row.Cells(4).Value
            car_info = row.Cells(5).Value
            truck_info = row.Cells(6).Value
            license_plate = row.Cells(7).Value
            note = row.Cells(8).Value
            executor = row.Cells(9).Value
            owner = row.Cells(10).Value
            owner_phone = row.Cells(11).Value
            current_path = os.path.dirname(os.path.abspath(__file__))
            photo_path = current_path + "\\" + row.Cells(12).Hyperlinks[0].Address.replace('/', '\\')

            # Открыть фото по пути и перевести в формат Base64

            d = 1
            with Session() as session:
                utb = Utb(in_number=in_number, car_going_date=car_going_date, car_going_place=car_going_place,
                          car_info=car_info, truck_info=truck_info, license_plate=license_plate, note=note,
                          executor=executor, owner=owner, owner_phone=owner_phone, add_by_user_id=4, kr_by_user_id=4)
                session.add(utb)
                session.commit()
                try:
                    with open(photo_path, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read())
                        photo = Photo(photo=encoded_string, utb_id=utb.id)
                        session.add(photo)
                        session.commit()
                except Exception as e:
                    print(f'{e}\ncar_info: {car_info}')
                d = 1


def select_all():
    with Session() as session:
        utbs = session.query(Utb).all()
        for utb in utbs:
            print(utb.add_by_user.username)


def add_users():
    user1 = User(username='DPPSKOVALSV', password='1111', first_name='Станислав', last_name='Коваленко',
                 middle_name='Владиславович')
    user2 = User(username='DPPSTUTUPV', password='1111', first_name='Павел', last_name='Тютюнник',
                 middle_name='Викторович')
    user3 = User(username='DPPS36POSAU', password='1111', first_name='Артем', last_name='Посохов',
                 middle_name='Юрьевич')
    user4 = User(username='DPPSPOPVS', password='1111', first_name='Вячеслав', last_name='Попов',
                 middle_name='Сергеевич')
    user5 = User(username='DPPS23RJAEV', password='1111', first_name='Евгений', last_name='Рядский',
                 middle_name='Викторович')
    user6 = User(username='DPPS36LISOPM', password='1111', first_name='Павел', last_name='Лысогоря',
                 middle_name='Николаевич')
    user7 = User(username='DPPSTATYV', password='1111', first_name='Евгений', last_name='Татара',
                 middle_name='Владимирович')
    user8 = User(username='DPPSTARVM', password='1111', first_name='Валерий', last_name='Тарасов',
                 middle_name='Николаевич')

    with Session() as session:
        session.add_all([user1, user2, user3, user4, user5, user6, user7, user8])
        session.commit()


if __name__ == '__main__':
    app = get_excel_app()
    wb = get_wb(app, 'C:/Users/Kyrylo/PycharmProjects/DUPP_base/1.xlsm')
    get_info(wb)

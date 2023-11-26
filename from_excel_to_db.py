#Перенести данные из excel в базу
import os

from db.engines.sync import Session
from db.models import Utb

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
            with Session() as session:
                utb = Utb(in_number=in_number, car_going_date=car_going_date, car_going_place=car_going_place,
                          car_info=car_info, truck_info=truck_info, license_plate=license_plate, note=note,
                          executor=executor, owner=owner, owner_phone=owner_phone)
                session.add(utb)
                session.commit()
                d=1





if __name__ == '__main__':
    excell_app = get_excel_app()
    wb = get_wb(excell_app, 'C:/Users/Kyrylo/PycharmProjects/DUPP_base/1.xlsm')
    info = get_info(wb)

from datetime import datetime
from textwrap import wrap

import sqlalchemy.orm
from sqlalchemy import select
from sqlalchemy.orm import selectinload

import config
from db.engines.sync import Session
from db.models.utb_card import Utb
from db.models.user import User


def Utb_raw_to_list(raws, position=1):
    sr = []
    if isinstance(raws, Utb):

        id = raws.id
        number = position
        try:
            in_number = int(float(raws.in_number))
        except:
            in_number = raws.in_number
        car_going_date = datetime.strftime(raws.car_going_date, "%d.%m.%Y")
        car_going_place = raws.car_going_place
        car_info = raws.car_info
        truck_info = raws.truck_info
        license_plate = raws.license_plate
        note = '\n'.join(wrap(raws.note, 35))
        executor = raws.executor
        owner = raws.owner
        owner_phone = raws.owner_phone

        sr = [id, number, in_number, car_going_date, car_going_place, car_info, truck_info, license_plate, note,
              executor, owner, owner_phone]
        position += 1
    else:
        for raw in raws:
            try:
                id = list(raw)[0].id
                number = position
                try:
                    in_number = int(float(list(raw)[0].in_number))
                except:
                    in_number = list(raw)[0].in_number
                car_going_date = datetime.strftime(list(raw)[0].car_going_date, "%d.%m.%Y")
                car_going_place = list(raw)[0].car_going_place
                car_info = list(raw)[0].car_info
                truck_info = list(raw)[0].truck_info
                license_plate = list(raw)[0].license_plate
                note = '\n'.join(wrap(list(raw)[0].note, 35))
                executor = list(raw)[0].executor
                owner = list(raw)[0].owner
                owner_phone = list(raw)[0].owner_phone
                sr.append(
                    [id, number, in_number, car_going_date, car_going_place, car_info, truck_info, license_plate, note,
                     executor,
                     owner,
                     owner_phone])
                position += 1
            except Exception as e:
                print(e)
    return sr

def get_data_for_auto_complete_utb():
    data = {}
    try:
        qry = select(Utb.car_going_place).group_by(Utb.car_going_place)
        car_going_place_result = config.session.execute(qry)
        car_going_place_result = car_going_place_result.scalars().all()
        data['car_going_place'] = car_going_place_result

        qry = select(Utb.note).group_by(Utb.note)
        note_result = config.session.execute(qry)
        note_result = note_result.scalars().all()
        data['note'] = note_result

        qry = select(Utb.owner, Utb.owner_phone)
        owner_result = config.session.execute(qry)
        owner_result = owner_result.fetchall()
        data['owner'] = set(owner_result)

    except Exception as e:
        print(e)
    return data

def get_all_users():
    try:
        qry = select(User).options(selectinload(User.utb_add_records), selectinload(User.utb_kr_records))
        res = config.session.execute(qry)
        result = res.scalars().all()
        return result
    except Exception as e:
        print(e)


if __name__ == '__main__':
    get_all_users()


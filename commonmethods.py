def Utb_raw_to_list(raws, position=1):
    if len(raws) > 1:
        sr = []
    for raw in raws:
        id = list(raw)[0].id
        number = position
        in_number = int(float(list(raw)[0].in_number))
        car_going_date = list(raw)[0].car_going_date
        car_going_place = list(raw)[0].car_going_place
        car_info = list(raw)[0].car_info
        truck_info = list(raw)[0].truck_info
        license_plate = list(raw)[0].license_plate
        note = list(raw)[0].note
        executor = list(raw)[0].executor
        owner = list(raw)[0].owner
        owner_phone = list(raw)[0].owner_phone
        if len(raws) > 1:
            sr.append(
                [id, number, in_number, car_going_date, car_going_place, car_info, truck_info, license_plate, note, executor, owner,
                 owner_phone])
            position+=1
        else:
            return [id, number, in_number, car_going_date, car_going_place, car_info, truck_info, license_plate, note, executor, owner,
                 owner_phone]
    return sr
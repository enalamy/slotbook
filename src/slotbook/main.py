from slotbook import room
from slotbook import slot 
from slotbook import booking



def main():

    bookings_by_id = {}
    rooms_by_id = {}
    slots_by_id = {}
    while True: 
        
        print("""
        SlotBook — бронирование переговорных

        1. Добавить комнату
        2. Посмотреть комнаты
        3. Создать слот
        4. Найти свободные слоты
        5. Забронировать слот
        6. Отменить бронирование
        7. Посмотреть историю бронирований
        8. Экспортировать историю в CSV
        0. Выйти

        Выберите действие:""", end = " ")

        command = input().strip()

        match command:
            case "1":
                name = input("Укажите название комнаты: ")
                capacity = input("Укажите вместимость комнаты: ")
                while True:
                    try:
                        new_room = room.add_room(name, capacity, rooms_by_id)
                    except room.RoomNameError as error:
                        print(error)
                        name = input("Укажите название комнаты: ")
                    except room.RoomCapacityError as error:
                        print(error)
                        capacity = input("Укажите вместимость комнаты: ")
                    else:
                        print((f"Комната создана. ID: {new_room.id}"))
                        break
                
            case "2":
                if not rooms_by_id:
                    print("Пока что нет комнат")
                else:
                    for temp_id, temp_value in rooms_by_id.items():
                        print(f"Комната{temp_id}:\n\tНазвание: {temp_value.name}\n\tВместимость: {temp_value.capacity}")
            case "3":
                if not rooms_by_id:
                    print("Сначала добавьте хотя бы одну комнату")
                else:
                    room_id = None
                    starts_at = None

                    while True:
                        if room_id is None:
                            try:
                                room_id = int(input("ID комнаты: "))
                            except ValueError:
                                print("Введите целое число")
                                continue

                        try:
                            if starts_at is None:
                                starts_at = slot.parse_slot_datetime(
                                    input(
                                        "Введите дату и время в формате dd mm yyyy hh: "
                                    )
                                )

                            new_slot = slot.add_slot(
                                room_id, starts_at, rooms_by_id, slots_by_id
                            )

                        except slot.SlotRoomError as error:
                            print(error)
                            room_id = None

                        except slot.SlotDateTimeError as error:
                            print(error)
                            starts_at = None

                        except slot.SlotDuplicateError as error:
                            print(error)
                            print("Выберите другое время для этой комнаты")
                            starts_at = None

                        else:
                            print(f"Слот создан. ID: {new_slot.id}")
                            print(f"Начало: {new_slot.starts_at:%d.%m.%Y %H:%M}")
                            print(f"Конец: {new_slot.ends_at:%d.%m.%Y %H:%M}")
                            break

            case "4": #исправить
                if not slots_by_id:
                    print("Сначала создайте хотя бы один слот")
                else:
                    while True:
                        try:
                            user_date = slot.parse_slot_date(
                                input("Введите дату в формате дд мм гггг: ")
                            )
                        except slot.SlotDateTimeError as error:
                            print(error)
                        else:
                            break

                    while True:
                        user_room = input(
                            "Введите ID комнаты "
                            "или нажмите Enter для поиска по всем комнатам: ").strip()

                        if user_room == "":
                            room_id = None
                        else:
                            try:
                                room_id = int(user_room)
                            except ValueError:
                                print("Введите целое число")
                                continue

                        try:
                            selected_slots = slot.find_free_slots(
                                user_date,
                                rooms_by_id,
                                slots_by_id,
                                bookings_by_id,
                                room_id,
                            )
                        except slot.SlotRoomError as error:
                            print(error)
                            continue

                        break

                    if not selected_slots:
                        if room_id is None:
                            print("Нет свободных слотов на выбранную дату")
                        else:
                            print(
                                "Для этой комнаты нет свободных слотов "
                                "на выбранную дату"
                            )
                    else:
                        print(
                            f"{'ID':<5} | {'Комната':<24} | "
                            f"{'Начало':<16} | {'Конец':<16}"
                        )
                        print("-" * 70)

                        for info in selected_slots:
                            print(
                                f"{info.id:<5} | "
                                f"{rooms_by_id[info.room_id].name:<24} | "
                                f"{info.starts_at:%d.%m.%Y %H:%M} | "
                                f"{info.ends_at:%d.%m.%Y %H:%M}"
                            )

            case "5":
                if not slots_by_id:
                    print("Сначала создайте хотя бы один слот")
                else:
                    while True:
                        worker_name = input("Введите имя работника для которого производится бронирование: ").strip()
                        if worker_name == "":
                            print("Ошбика: имя не может быть пустым\n")
                            continue
                        break
                    while True:
                        text = input("Введите ID слота для бронирования бронирования или Enter для возврата в меню: ").strip()
                        if text == "":
                            break
                        try:
                            user_slot_id = int(text)
                        except ValueError:
                            print("Ошибка: введите целое число\n")
                            continue
                        if user_slot_id not in slots_by_id:
                            print("Ошибка: слота с этим ID не существует\n")
                            continue 
                        try:
                            new_booking = booking.add_booking(user_slot_id, worker_name, bookings_by_id, slots_by_id)
                        except ValueError as error:
                            print(error)
                            continue
                        print(f"Бронирование №{new_booking.id}\n {worker_name} - {rooms_by_id[slots_by_id[user_slot_id].room_id].name}, {slots_by_id[user_slot_id].starts_at.date()}, {slots_by_id[user_slot_id].starts_at:%H:%M} - {slots_by_id[user_slot_id].ends_at:%H:%M}")
                        break

            case "6":
                if not bookings_by_id:
                    print("Сначала забронируйте хотя бы один слот")
                else:
                    while True:
                        text = input("Введите ID бронирования для отмены или Enter для возврата в меню: ").strip()
                        if text == "":
                            break
                        try:
                            user_book_id = int(text)
                        except ValueError:
                            print("Ошибка: введите целое число\n")
                            continue
                        if user_book_id not in bookings_by_id:
                            print("Ошибка: бронирования с этим ID не существует\n")
                            continue 
                        try:
                            booking.cancel_booking(user_book_id, bookings_by_id, slots_by_id)
                        except ValueError as error:
                            print(error)
                            continue
                        print(f"Бронирование №{user_book_id} отменено\n Слот снова доступен")
                        break
            case "7":
                print("Скоро")
            case "8":
                print("Скоро")
            case "0":
                break
            case _:
                print("Введите номер пункта меню")
        
        input("Нажмите любую кнопку ")
if __name__ == "__main__":
    main()
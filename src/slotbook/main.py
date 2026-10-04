from slotbook import room


def main():

    rooms_by_id = {}
    while True: #не забудь убрать менюшку из цикла потом
        
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
                while True:
                    print("Укажите название комнаты: ")
                    temp_name = input().strip()
                    if not temp_name:
                        print("Название не может быть пустым")
                        continue
                    if any(current_room.name.casefold() == temp_name.casefold()
                        for current_room in rooms_by_id.values()):
                        print("Это имя уже используется")
                    else:
                        break

                while True:
                    try:
                        temp_capacity = (int(input("Укажите вместимость комнаты: ")))
                    except ValueError:
                        print("Введите целое число")
                        continue
                    if temp_capacity <= 0:
                        print("Вместимость должна быть больше 0")
                        continue
                    
                    break

                temp_obj = room.Room(temp_name, temp_capacity)
                rooms_by_id[temp_obj.id] = temp_obj
                print(f"Комната создана. ID: {temp_obj.id}")
                
            case "2":
                if not rooms_by_id:
                    print("Пока что нет комнат")
                else:
                    for temp_id, temp_value in rooms_by_id.items():
                        print(f"Комната{temp_id}:\n\tНазвание: {temp_value.name}\n\tВместимость: {temp_value.capacity}")
            case "3":
                print("Скоро")
            case "4":
                print("Скоро")
            case "5":
                print("Скоро")
            case "6":
                print("Скоро")
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
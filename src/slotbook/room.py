class Room:

    _next_id = 1 
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity
        self.__id = Room._next_id
        Room._next_id += 1

    @property
    def id(self):
        return self.__id
        
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise RoomNameError("Название должно быть строкой")

        value = value.strip()

        if not value:
            raise RoomNameError("Название не может быть пустым")

        self.__name = value

    @property
    def capacity(self):
        return self.__capacity
    
    @capacity.setter
    def capacity(self, value):  
        if isinstance(value, bool) or not isinstance(value, int):
            raise RoomCapacityError("Вместимость должна быть целым числом")

        if value <= 0:
            raise RoomCapacityError("Вместимость должна быть больше нуля")

        self.__capacity = value

    def __str__(self):
        return f"ID: {self.id},\nName: {self.name},\nCapacity: {self.capacity}"

class RoomNameError(ValueError):
    pass


class RoomCapacityError(ValueError):
    pass

def add_room(name, capacity, rooms_by_id):
    name = name.strip()
    
    try:
        capacity = int(capacity)
    except ValueError:
        raise RoomCapacityError("Вместимость должна быть целым числом") from None

    if any(current_room.name.casefold() == name.casefold() for current_room in rooms_by_id.values()):
        raise RoomNameError("Комната с таким названием уже существует")
    
    temp_obj = Room(name, capacity)
    rooms_by_id[temp_obj.id] = temp_obj
    return temp_obj
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
        if value is None or value == "" or value == "".strip():
            print("Название не может быть пустым")
        self.__name = value

    @property
    def capacity(self):
        return self.__capacity
    
    @capacity.setter
    def capacity(self, value):  
        if value <= 0:
            raise ValueError("Вместимость должна быть положительным целым числом") 
        self.__capacity = value

    def __str__(self):
        return f"ID: {self.id},\nName: {self.name},\nCapacity: {self.capacity}"

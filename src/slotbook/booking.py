from datetime import datetime


class Booking:

    _next_id = 1 
    def __init__(self, slot_id, worker_name):
        self.worker_name = worker_name
        self.__id = Booking._next_id
        Booking._next_id += 1
        self.status = "active"
        self.slot_id = slot_id
        self.created_at = datetime.now()
        self.cancelled_at = None

    @property
    def id(self):
        return self.__id
    
    def cancel(self):
        if self.status == "cancelled":
            raise ValueError("Бронирование уже отменено")

        self.cancelled_at = datetime.now()
        self.status = "cancelled"

    @property
    def worker_name(self):
        return self.__worker_name

    @worker_name.setter
    def worker_name(self, value):
        if not isinstance(value, str):
            raise ValueError("Имя должно быть строкой")

        value = value.strip()

        if not value:
            raise ValueError("Имя не может быть пустым")

        self.__worker_name = value


def add_booking(slot_id, worker_name, bookings_by_id, slots_by_id):
    try:
        slot_id = int(slot_id)
    except ValueError:
        raise ValueError("ID должно быть целым числом") from None
    
    if slot_id not in slots_by_id:
        raise ValueError("Такого слота не существует")

    if any(current_book.slot_id == slot_id and current_book.status == "active" for current_book in bookings_by_id.values()):
        raise ValueError("Этот слот уже забронирован, выберите другой")
    temp_obj = slots_by_id[slot_id]
    if temp_obj.starts_at <= datetime.now():
        raise ValueError("Можно забронировать только неначавшийся слот")

    new_booking = Booking(slot_id, worker_name)
    bookings_by_id[new_booking.id] = new_booking
    return new_booking

def cancel_booking(booking_id, bookings_by_id, slots_by_id):
    if booking_id in bookings_by_id:
        selected_slot = slots_by_id[bookings_by_id[booking_id].slot_id]
        if selected_slot.starts_at <= datetime.now():
            raise ValueError("Нельзя отменить бронирование начавшегося слота")
        return bookings_by_id[booking_id].cancel()
    else:
        raise ValueError("Такой брони не существует")
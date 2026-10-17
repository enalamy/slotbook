from datetime import datetime
import csv
from pathlib import Path
from tempfile import NamedTemporaryFile
from functools import wraps
import time

class Booking:
    _next_id = 1

    def __init__(self, slot_id, worker_name, booking_id=None):
        self.worker_name = worker_name

        if booking_id is None:
            booking_id = Booking._next_id

        if (
            isinstance(booking_id, bool)
            or not isinstance(booking_id, int)
            or booking_id <= 0
        ):
            raise ValueError(
                "ID бронирования должен быть положительным целым числом"
            )

        self.__id = booking_id
        self.status = "active"
        self.slot_id = slot_id
        self.created_at = datetime.now()
        self.cancelled_at = None

        Booking._next_id = max(Booking._next_id, booking_id + 1)

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

def get_booking_history(bookings_by_id):
    return sorted(bookings_by_id.values(),
        key=lambda current_booking: current_booking.created_at,
        reverse=True,)    


def iter_booking_rows(bookings_by_id, slots_by_id, rooms_by_id):
    for booking_id in sorted(bookings_by_id):
            current_booking = bookings_by_id[booking_id]
            current_slot = slots_by_id[current_booking.slot_id]
            current_room = rooms_by_id[current_slot.room_id]
            yield [
                current_booking.id,
                current_slot.room_id,
                current_room.name,
                current_booking.worker_name,
                current_slot.starts_at,
                current_slot.ends_at,
                current_booking.status,
                current_booking.created_at,
                current_booking.cancelled_at
            ]

def time_counter(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        print(f"Функция '{func.__name__}' выполнилась за {execution_time:.6f} сек.")
        return result
    return wrapper


@time_counter
def export_booking_history(

    path, bookings_by_id, slots_by_id, rooms_by_id
):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    temp_path = None
    count = 0

    try:
        with NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="",
            dir=path.parent,
            suffix=".tmp",
            delete=False,
        ) as file:
            temp_path = Path(file.name)
            writer = csv.writer(file)

            writer.writerow([
                "booking_id",
                "room_id",
                "room_name",
                "employee_name",
                "starts_at",
                "ends_at",
                "status",
                "created_at",
                "cancelled_at",
            ])

            for row in iter_booking_rows(
                bookings_by_id, slots_by_id, rooms_by_id
            ):
                writer.writerow(row)
                count += 1

        # Файл уже закрыт, все строки успешно записаны.
        temp_path.replace(path)
        return count

    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)
   
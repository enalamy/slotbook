from datetime import date, datetime, timedelta

class SlotRoomError(ValueError):
    pass


class SlotDateTimeError(ValueError):
    pass


class SlotDuplicateError(ValueError):
    pass

class Slot:
    _next_id = 1 
    def __init__(self, room_id, starts_at):
        self.__id = Slot._next_id
        Slot._next_id += 1
        self.starts_at = starts_at
        self.__room_id = room_id

    @property
    def id(self):
        return self.__id
    
    @property
    def room_id(self):
        return self.__room_id
    
    @property
    def ends_at(self):
        return self.starts_at + timedelta(hours=1)

def parse_slot_datetime(text):
    if not isinstance(text, str):
        raise SlotDateTimeError("Дата и время должны быть переданы строкой")

    text = text.strip()

    if not text:
        raise SlotDateTimeError("Дата и время не могут быть пустыми")

    date_formats = (
        "%Y %m %d",
        "%Y-%m-%d",
        "%d.%m.%Y",
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%d %m %Y",
    )
    time_formats = ("%H", "%H:%M", "%H %M", "%H%M", "%H.%M")

    for date_format in date_formats:
        for time_format in time_formats:
            format_string = f"{date_format} {time_format}"

            try:
                parsed = datetime.strptime(text, format_string)
            except ValueError:
                continue

            if parsed.minute != 0:
                raise SlotDateTimeError("Слот должен начинаться в начале часа")

            return parsed
    raise SlotDateTimeError(
    "Некорректная дата или время. Пример: 15 10 2026 12"
)

def add_slot(room_id, starts_at, rooms_by_id, slots_by_id):
    if room_id not in rooms_by_id:
        raise SlotRoomError(f"Комната с ID {room_id} не существует")

    if (
        starts_at.minute != 0
        or starts_at.second != 0
        or starts_at.microsecond != 0
    ):
        raise SlotDateTimeError("Слот должен начинаться в начале часа")
        
    if starts_at <= datetime.now():
        raise SlotDateTimeError("Слот должен быть в будущем")

    if any(
    current_slot.room_id == room_id
    and current_slot.starts_at == starts_at
    for current_slot in slots_by_id.values()
    ):
        raise SlotDuplicateError("Такой слот уже существует")

    temp_slot = Slot(room_id, starts_at)
    slots_by_id[temp_slot.id] = temp_slot

    return temp_slot

def parse_slot_date(text):
    if not isinstance(text, str):
        raise SlotDateTimeError("Дата должна быть передана строкой")

    text = text.strip()

    if not text:
        raise SlotDateTimeError("Дата не может быть пустой")

    try:
        parsed = datetime.strptime(text, "%d %m %Y").date()
    except ValueError:
        raise SlotDateTimeError("Некорректная дата. Пример: 15 10 2026") from None

    if parsed < date.today():
        raise SlotDateTimeError("Дата должна быть от сегодня")

    return parsed

def find_free_slots(
    selected_date,
    rooms_by_id,
    slots_by_id,
    bookings_by_id,
    room_id=None,
):
    if room_id is not None and room_id not in rooms_by_id:
        raise SlotRoomError(f"Комната с ID {room_id} не существует")

    now = datetime.now()
    found_slots = []

    for current_slot in slots_by_id.values():
        if current_slot.starts_at.date() != selected_date:
            continue

        if current_slot.starts_at <= now:
            continue

        if room_id is not None and current_slot.room_id != room_id:
            continue

        if any(
            current_booking.slot_id == current_slot.id
            and current_booking.status == "active"
            for current_booking in bookings_by_id.values()
        ):
            continue

        found_slots.append(current_slot)

    return sorted(
        found_slots,
        key=lambda current_slot: (
            current_slot.starts_at,
            rooms_by_id[current_slot.room_id].name,
        ),
    )
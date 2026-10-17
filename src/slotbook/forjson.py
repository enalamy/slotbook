from datetime import datetime
import json
from pathlib import Path
from slotbook import room, slot, booking
from tempfile import NamedTemporaryFile


def save_state(path, rooms_by_id, slots_by_id, bookings_by_id):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    data = {
    "rooms": {},
    "slots": {},
    "bookings": {},
    }

    for id, room in rooms_by_id.items():
        data["rooms"][str(id)] = {
            "id" : room.id,
            "name": room.name,
            "capacity": room.capacity,
        }
    if slots_by_id != None:
        for id, slot in slots_by_id.items():
            data["slots"][str(id)] = {
                "id" : slot.id,
                "room_id" : slot.room_id,
                "starts_at": slot.starts_at.isoformat(),
                "ends_at": slot.ends_at.isoformat(),
            }
    if bookings_by_id != None:
        for id, booking in bookings_by_id.items():
            data["bookings"][str(id)] = {
                "id": booking.id,
                "slot_id": booking.slot_id,
                "worker_name": booking.worker_name,
                "status": booking.status,
                "created_at": booking.created_at.isoformat(),
                "cancelled_at": (booking.cancelled_at.isoformat() if booking.cancelled_at is not None else None),
            }

    temp_path = None

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
            json.dump(data, file, ensure_ascii=False, indent=4)

        temp_path.replace(path)

    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)

def load_state(path, rooms_by_id, slots_by_id, bookings_by_id):
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return

    if not isinstance(data, dict):
        raise ValueError("Состояние должно быть JSON-объектом")

    for section in ("rooms", "slots", "bookings"):
        if not isinstance(data.get(section), dict):
            raise ValueError(
                f"Раздел '{section}' должен содержать словарь"
            )

    loaded_rooms = {}
    loaded_slots = {}
    loaded_bookings = {}
    json_rooms = data["rooms"]
    json_slots = data["slots"]
    json_bookings = data["bookings"]

    for room_id, room_data in json_rooms.items():
        restored_room = room.Room(
            name=room_data["name"],
            capacity=room_data["capacity"],
            room_id=int(room_id),
        )
        loaded_rooms[restored_room.id] = restored_room

    for slot_id, slot_data in json_slots.items():
        if slot_data["room_id"] not in loaded_rooms:
            raise ValueError(
                f"Слот №{slot_id} ссылается на несуществующую "
                f"комнату №{slot_data['room_id']}"
            )
        restored_slot = slot.Slot(
            room_id=slot_data["room_id"],
            starts_at=datetime.fromisoformat(slot_data["starts_at"]),
            slot_id=int(slot_id),
        )
        loaded_slots[restored_slot.id] = restored_slot

    for booking_id, booking_data in json_bookings.items():
        if booking_data["slot_id"] not in loaded_slots:
            raise ValueError(
                f"Бронь №{booking_id} ссылается на несуществующий "
                f"слот №{booking_data['slot_id']}"
            )

        if booking_data["status"] not in ("active", "cancelled"):
            raise ValueError(
                f"У брони №{booking_id} неизвестный статус"
            )
        if booking_data["status"] == "active":
            if any(
                item.slot_id == booking_data["slot_id"]
                and item.status == "active"
                for item in loaded_bookings.values()
            ):
                raise ValueError(
                    f"У слота №{booking_data['slot_id']} "
                    "несколько активных бронирований"
                )
        restored_booking = booking.Booking(
            slot_id=booking_data["slot_id"],
            worker_name=booking_data["worker_name"],
            booking_id=int(booking_id),
        )
        restored_booking.status = booking_data["status"]
        restored_booking.created_at = datetime.fromisoformat(booking_data["created_at"])

        if booking_data["cancelled_at"] is None:
            restored_booking.cancelled_at = None
        else:
            restored_booking.cancelled_at = datetime.fromisoformat(booking_data["cancelled_at"])
        loaded_bookings[restored_booking.id] = restored_booking

    rooms_by_id.clear()
    rooms_by_id.update(loaded_rooms)

    slots_by_id.clear()
    slots_by_id.update(loaded_slots)

    bookings_by_id.clear()
    bookings_by_id.update(loaded_bookings)
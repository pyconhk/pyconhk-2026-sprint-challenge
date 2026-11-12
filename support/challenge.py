import asyncio
import hashlib
import json
import re
from collections.abc import Iterable
from dataclasses import dataclass

ROOMS = ("A", "B", "C")
_LOGIN = re.compile(r"[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*")


@dataclass(frozen=True, order=True)
class Event:
    minute: int
    room: str
    event_id: str


def normalise_login(value: str) -> str:
    if not 1 <= len(value) <= 39 or _LOGIN.fullmatch(value) is None:
        raise ValueError("Enter a valid GitHub username.")
    return value.lower()


def room_records(login: str, clue: str, room: str) -> tuple[Event, ...]:
    if room not in ROOMS:
        raise ValueError(f"Unknown room: {room}")

    seed = json.dumps([normalise_login(login), clue], separators=(",", ":"))
    encoded_seed = seed.encode("ascii")
    shared_id = hashlib.sha256(encoded_seed).hexdigest()[:8]
    fingerprint = hashlib.sha256(encoded_seed + room.encode("ascii")).hexdigest()
    setup = Event(30, room, f"setup-{shared_id}")
    return (
        Event(50 + int(fingerprint[8:10], 16) % 20, room, setup.event_id),
        setup,
        Event(30, room, f"check-in-{fingerprint[10:18]}"),
        setup,
        Event(
            10 + int(fingerprint[18:20], 16) % 20,
            room,
            f"welcome-{fingerprint[20:28]}",
        ),
    )


async def load_room(login: str, clue: str, room: str) -> tuple[Event, ...]:
    await asyncio.sleep(0)
    return room_records(login, clue, room)


def report_digest(events: Iterable[Event]) -> str:
    rows = [[event.minute, event.room, event.event_id] for event in events]
    report = json.dumps(rows, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(report.encode("ascii")).hexdigest()

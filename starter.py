"""Fix build_report, then run this file to create your Sprint ticket proof."""

import argparse
import asyncio

from pydantic import ValidationError

from support.challenge import ROOMS, Event, load_room, normalise_login, report_digest
from support.proof import GAME_SEED, ContactDetails, write_proof


# Please modify only the following function.
async def build_report(login: str, clue: str) -> list[Event]:
    """Keep the first occurrence of each event and sort by minute, room, and ID."""
    records: list[Event] = []
    for room in ROOMS:
        # TODO: Wait for the room's records before adding them to the report.
        room_events = load_room(login, clue, room)
        records.extend(room_events)
    # TODO: Keep the earliest record per event ID, using room order for ties.
    return sorted(records)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create your Sprint ticket proof.")
    parser.add_argument("login", type=normalise_login, help="Your GitHub username")
    args = parser.parse_args()

    report = asyncio.run(build_report(args.login, GAME_SEED))
    try:
        contact = ContactDetails(
            first_name=input("First name: "),
            last_name=input("Last name: "),
            email=input("Email for your Eventbrite ticket: "),
        )
    except ValidationError:
        parser.error("Enter your first name, last name, and a valid email address.")
    try:
        output = write_proof(args.login, report_digest(report), contact)
    except (OSError, TypeError, ValueError) as error:
        parser.error(str(error))
    print(f"Created {output}. Commit only this file to your PR.")


if __name__ == "__main__":
    main()

import asyncio

from support.challenge import report_digest
from starter import build_report


def test_report_contains_all_rooms() -> None:
    report = asyncio.run(build_report("sprint-example", "example-clue"))
    assert {event.room for event in report} == {"A", "B", "C"}


def test_report_matches_expected_digest() -> None:
    report = asyncio.run(build_report("sprint-example", "example-clue"))
    expected = "eb33dbd50d7c42c11b54ac54c467fd7cdeaf18bf6dc401e7e80a51f2182c7728"
    assert report_digest(report) == expected

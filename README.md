# PyCon HK 2026 Sprint Day ticket challenge

This challenge is for people who still need a ticket for Sprint Day on Sunday, 15 November. The first 30 eligible applications get a ticket. Open your pull request by **Saturday, 14 November 2026 at 23:59 Hong Kong time (UTC+8)**. If we can offer you a place, we'll register you in Eventbrite and you'll get the ticket by email.

## Fix the room report

Fork this repository and clone your fork. You'll need [Python 3.10 or later](https://www.python.org/downloads/) and [uv](https://docs.astral.sh/uv/getting-started/installation/).

The three rooms each keep a log of events. A record has a minute, a room and an event ID. The same event can appear several times, so the report should show when and where it first happened.

**Please modify only the `build_report()` function in [`starter.py`](starter.py).**

Wait for each room's async loader to finish before using its results. Then keep one record per event ID, choosing the earliest minute. If two rooms logged that event at the same minute, prefer A, then B, then C. Sort the finished report by minute, then room, then event ID.

For example, if `setup` appears in room B at minute 30, room A at minute 30 and room C at minute 50, keep the record for room A at minute 30. Run the tests from the repository folder. They fail on the starter code and should pass once your report is correct.

```sh
uv run pytest -q
```

## Generate the encrypted proof

Once the tests pass, run this from the repository folder. Use the GitHub username of the account that will open the pull request.

```sh
uv run python starter.py YOUR_GITHUB_USERNAME
```

When prompted, enter your first name, last name and the email address where you want to receive your Eventbrite ticket. The command encrypts your result and contact details into one string and saves it to `tickets/<lowercase-github-username>.txt`. For example, if your username is `PyCoder`, the file is `tickets/pycoder.txt`. Use the file as generated and keep your contact details out of the PR text and comments.

## Open the pull request

Create a branch in your fork and commit **only** the generated file under `tickets/`. Keep your changes to `starter.py` on your computer. On GitHub, open a PR from your fork's branch into `main` on `pyconhk/pyconhk-2026-sprint-challenge`. GitHub fills in the [PR checklist](.github/pull_request_template.md). Tick both boxes before submitting.

The format check confirms that you submitted one file in the right place. The organizers verify the proof and review eligible applications in PR opening order. If two requests use the same GitHub account or email, we process the first eligible one. We'll reply on your PR. If you're approved, Eventbrite will email your ticket.

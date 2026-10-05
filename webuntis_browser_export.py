#!/usr/bin/env python3
import argparse
import csv
import os
import re
import shutil
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Dict, List, Tuple

from playwright.sync_api import BrowserType, Page, sync_playwright


LESSON_ROUTE = re.compile(
    r"/lessonDetails/\d+/\d+/\d+/([^/?]+)/([^/?]+)"
)
GERMAN_WEEKDAYS = (
    "Montag",
    "Dienstag",
    "Mittwoch",
    "Donnerstag",
    "Freitag",
    "Samstag",
    "Sonntag",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Exportiert Fach und Lehrstoff aus den gerenderten WebUntis-Stundendetails."
    )
    parser.add_argument("--url", default=os.getenv("WEBUNTIS_URL", "https://bszet.webuntis.com"))
    parser.add_argument("--start", default="2026-08-31", help="Startdatum (beliebiger Tag der ersten Woche), YYYY-MM-DD")
    parser.add_argument("--weeks", type=int, default=4, help="Anzahl aufeinanderfolgender Schulwochen")
    parser.add_argument("--year-id", default=os.getenv("WEBUNTIS_YEAR_ID", "30"))
    parser.add_argument("--output", default="webuntis_4_wochen_export.csv")
    parser.add_argument(
        "--proxy",
        default=os.getenv("HTTPS_PROXY") or os.getenv("https_proxy") or os.getenv("HTTP_PROXY") or os.getenv("http_proxy"),
        help="Optionaler Browser-Proxy",
    )
    parser.add_argument(
        "--profile-dir",
        default=str(Path.home() / ".webuntis-berichtsheft-profile"),
        help="Lokaler Playwright-Profilordner für die Login-Session",
    )
    return parser.parse_args()


def find_edge() -> str | None:
    candidates = [shutil.which("msedge")]
    for variable in ("PROGRAMFILES(X86)", "PROGRAMFILES", "LOCALAPPDATA"):
        root = os.getenv(variable)
        if root:
            candidates.append(str(Path(root) / "Microsoft" / "Edge" / "Application" / "msedge.exe"))
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return candidate
    return None


def build_weeks(start_value: str, count: int) -> List[date]:
    start = date.fromisoformat(start_value)
    if count < 1:
        raise ValueError("--weeks muss mindestens 1 sein.")
    monday = start - timedelta(days=start.weekday())
    return [monday + timedelta(weeks=offset) for offset in range(count)]


def format_date(value: Any) -> str:
    raw = str(value)
    return f"{raw[:4]}-{raw[4:6]}-{raw[6:8]}"


def format_time(value: Any) -> str:
    raw = str(value).zfill(4)
    return f"{raw[:2]}:{raw[2:4]}"


def week_subjects(page: Page, monday: date, year_id: str) -> Dict[Tuple[str, str, str], str]:
    result = page.evaluate(
        """async ({week, yearId}) => {
            const tokenResponse = await fetch('/WebUntis/api/token/new', {
                credentials: 'include', headers: {Accept: 'application/json'}
            });
            if (!tokenResponse.ok) return {status: tokenResponse.status, message: 'Token konnte nicht geladen werden'};
            const token = (await tokenResponse.text()).replace(/^\"|\"$/g, '');
            const segment = token.split('.')[1];
            const payload = JSON.parse(atob(segment.replace(/-/g, '+').replace(/_/g, '/').padEnd(Math.ceil(segment.length / 4) * 4, '=')));
            const response = await fetch(`/WebUntis/api/public/timetable/weekly/data?elementType=5&elementId=${payload.person_id}&date=${week}&formatId=1`, {
                credentials: 'include',
                headers: {
                    Authorization: `Bearer ${token}`,
                    Accept: 'application/json',
                    'Tenant-Id': String(payload.tenant_id),
                    'X-WebUntis-Api-School-Year-Id': yearId
                }
            });
            return {status: response.status, json: await response.json()};
        }""",
        {"week": monday.isoformat(), "yearId": year_id},
    )
    if result.get("status") != 200:
        raise RuntimeError(
            f"Stundenplan für {monday.isoformat()} konnte nicht geladen werden "
            f"(HTTP {result.get('status')}). Bist du noch angemeldet und stimmt die Schuljahr-ID?"
        )

    data = result.get("json", {}).get("data", {}).get("result", {}).get("data", {})
    subjects = {
        str(item.get("id")): str(item.get("name") or "")
        for item in data.get("elements", [])
        if item.get("type") == 3
    }
    by_period: Dict[Tuple[str, str, str], str] = {}
    for periods in data.get("elementPeriods", {}).values():
        for period in periods or []:
            subject_element = next(
                (element for element in period.get("elements", []) if element.get("type") == 3),
                None,
            )
            if subject_element is None:
                continue
            key = (
                format_date(period.get("date")),
                format_time(period.get("startTime")),
                format_time(period.get("endTime")),
            )
            by_period[key] = subjects.get(str(subject_element.get("id")), "")
    return by_period


def card_subject(card) -> str:
    return card.evaluate(
        """element => {
            const tags = [...element.querySelectorAll('.lesson-card-regular-tag')];
            const subject = tags.find(tag => !tag.classList.contains('lesson-card-top-element'));
            return subject ? subject.textContent.trim() : '';
        }"""
    )

def append_lesson_if_valid(
    rows: List[Dict[str, str]],
    seen_periods: set[Tuple[str, str, str]],
    row: Dict[str, str],
) -> str:
    if not row["lesson_topic"].strip():
        return "missing_topic"

    period = (row["date"], row["start"], row["end"])
    if period in seen_periods:
        return "duplicate"

    seen_periods.add(period)
    rows.append(row)
    return "added"



def extract_week(page: Page, monday: date, base_url: str, year_id: str) -> List[Dict[str, str]]:
    target = f"{base_url.rstrip('/')}/timetable/my-student?date={monday.isoformat()}"
    page.goto(target, wait_until="domcontentloaded")
    page.locator("#layout-main").wait_for(state="visible", timeout=30000)
    page.wait_for_timeout(1200)

    subjects = week_subjects(page, monday, year_id)
    cards = page.locator(".lesson-card-info-container")
    card_count = cards.count()
    rows: List[Dict[str, str]] = []
    seen_periods: set[Tuple[str, str, str]] = set()
    missing_topic_count = 0
    duplicate_count = 0

    for index in range(card_count):
        card = cards.nth(index)
        fallback_subject = card_subject(card)
        card.click(timeout=15000)
        dialog = page.locator('[role="dialog"]').first
        dialog.wait_for(state="visible", timeout=15000)
        page.wait_for_timeout(250)

        match = LESSON_ROUTE.search(page.url)
        if match is None:
            raise RuntimeError(f"Stunden-URL konnte nicht ausgewertet werden: {page.url}")
        start_value, end_value = match.groups()
        lesson_date = date.fromisoformat(start_value[:10])
        start_time = start_value[11:16]
        end_time = end_value[11:16]
        subject = subjects.get((lesson_date.isoformat(), start_time, end_time), "") or fallback_subject
        topic_fields = dialog.locator("input, textarea")
        topic_values = [topic_fields.nth(i).input_value() for i in range(topic_fields.count())]
        topic = topic_values[-1] if topic_values else ""

        row = {
            "date": lesson_date.isoformat(),
            "weekday": GERMAN_WEEKDAYS[lesson_date.weekday()],
            "subject": subject,
            "start": start_time,
            "end": end_time,
            "lesson_topic": topic.strip(),
        }
        result = append_lesson_if_valid(rows, seen_periods, row)
        if result == "missing_topic":
            missing_topic_count += 1
        elif result == "duplicate":
            duplicate_count += 1

        close_button = dialog.locator("button").first
        close_button.click()
        dialog.wait_for(state="hidden", timeout=10000)

    print(
        f"{monday.isoformat()}: {len(rows)} Stunden exportiert, "
        f"{missing_topic_count} ohne Lehrstoff und {duplicate_count} Dubletten ausgelassen"
    )
    return rows


def write_csv(rows: List[Dict[str, str]], output_path: str) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["date", "weekday", "subject", "start", "end", "lesson_topic"]
    with path.open("w", newline="", encoding="utf-8-sig") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = parse_args()
    weeks = build_weeks(args.start, args.weeks)
    proxy = {"server": args.proxy} if args.proxy else None

    with sync_playwright() as playwright:
        browser_type: BrowserType = playwright.chromium
        launch_options: Dict[str, Any] = {
            "user_data_dir": args.profile_dir,
            "headless": False,
            "viewport": {"width": 1600, "height": 1000},
        }
        edge_path = find_edge()
        if edge_path:
            launch_options["executable_path"] = edge_path
        if proxy:
            launch_options["proxy"] = proxy

        context = browser_type.launch_persistent_context(**launch_options)
        try:
            page = context.pages[0] if context.pages else context.new_page()
            page.goto(f"{args.url.rstrip('/')}/WebUntis/#/basic/login", wait_until="domcontentloaded")
            print("Bitte melde dich im geöffneten WebUntis-Browser an.")
            input("Nach erfolgreichem Login hier Enter drücken: ")

            rows: List[Dict[str, str]] = []
            for monday in weeks:
                rows.extend(extract_week(page, monday, args.url, args.year_id))
            write_csv(rows, args.output)
            print(f"CSV geschrieben: {Path(args.output).resolve()}")
            print(f"Stunden mit eingetragenem Lehrstoff: {len(rows)}")
        finally:
            context.close()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("Abbruch durch Benutzer.", file=sys.stderr)
        raise SystemExit(1)
    except Exception as exc:
        print(f"Fehler: {exc}", file=sys.stderr)
        raise SystemExit(1)

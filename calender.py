import caldav
import os
import sys
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import vobject


url = "https://caldav.icloud.com/"
load_dotenv("apple_key.env")
username = os.getenv("ICLOUD_USERNAME")
password = os.getenv("ICLOUD_APP_PASSWORD")

def check_icloud():
    if not username or not password:
        raise RuntimeError("iCloud credentials not found")
    try:
        client = caldav.DAVClient(
            url=url,
            username=USERNAME,
            password=PASSWORD
        )
        principal = client.principal()
        calendars = principal.calendars()

        print("iCloud CalDAV Connected")
    except:
        print("iCloud CalDAV Connection Failed")
        sys.exit(1)



def load_calendar(days=7):
    client = caldav.DAVClient(
        url=url,
        username=username,
        password=password
    )

    principal = client.principal()
    calendars = principal.calendars()

    now = datetime.now(timezone.utc)
    end = now + timedelta(days=days)

    results = []

    for cal in calendars:
        events = cal.search(start=now, end=end, event=True, expand=True)


        for event in events:
            data = event.data  # 原始 iCalendar 文本

            results.append({
                "calendar": cal.name,
                "raw": data
            })

    return results



def parse_ics(raw_ics: str):
    cal = vobject.readOne(raw_ics)
    vevent = cal.vevent

    return {
        "title": vevent.summary.value if hasattr(vevent, "summary") else "",
        "start": vevent.dtstart.value,
        "end": vevent.dtend.value if hasattr(vevent, "dtend") else None,
        "description": vevent.description.value if hasattr(vevent, "description") else "",
        "uid": vevent.uid.value if hasattr(vevent, "uid") else ""
    }

def clean_event(days=7):
    clean_events = []

    results = load_calendar(days)
    for item in results:  # results 就是你现在 print 出来的那个 list
        parsed = parse_ics(item["raw"])
        parsed["calendar"] = item["calendar"]
        clean_events.append(parsed)

    return clean_events

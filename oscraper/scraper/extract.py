from bs4 import BeautifulSoup
import re
import logging
from typing import List, Dict, Optional, Tuple

logger = logging.getLogger(__name__)


def parse_date_interval_to_iso(date_str: str) -> Tuple[str, str]:
    """Parse a date interval string and return (start_date, end_date) in ISO format (YYYY-MM-DD). Raises ValueError if no pattern matches."""
    date_str = date_str.strip()
    # 13-15.06.2025 or 04-06.07.2025
    m = re.match(r"(\d{1,2})-(\d{1,2})\.(\d{2})\.(\d{4})", date_str)
    if m:
        d1, d2, month, year = m.groups()
        start_date = f"{year}-{month}-{int(d1):02d}"
        end_date = f"{year}-{month}-{int(d2):02d}"
        logger.debug(
            f"Matched pattern 'DD-DD.MM.YYYY': {date_str} -> {start_date}, {end_date}"
        )
        return start_date, end_date
    # 29.07.-01.08.2025
    m = re.match(r"(\d{1,2})\.(\d{2})\.-(\d{1,2})\.(\d{2})\.(\d{4})", date_str)
    if m:
        d1, m1, d2, m2, year = m.groups()
        start_date = f"{year}-{m1}-{int(d1):02d}"
        end_date = f"{year}-{m2}-{int(d2):02d}"
        logger.debug(
            f"Matched pattern 'DD.MM.-DD.MM.YYYY': {date_str} -> {start_date}, {end_date}"
        )
        return start_date, end_date
    # 20-24.08.2025
    m = re.match(r"(\d{1,2})-(\d{1,2})\.(\d{2})\.(\d{4})", date_str)
    if m:
        d1, d2, month, year = m.groups()
        start_date = f"{year}-{month}-{int(d1):02d}"
        end_date = f"{year}-{month}-{int(d2):02d}"
        logger.debug(
            f"Matched pattern 'DD-DD.MM.YYYY': {date_str} -> {start_date}, {end_date}"
        )
        return start_date, end_date
    # 21.06.2025
    m = re.match(r"(\d{1,2})\.(\d{2})\.(\d{4})", date_str)
    if m:
        d, month, year = m.groups()
        start_date = end_date = f"{year}-{month}-{int(d):02d}"
        logger.debug(f"Matched pattern 'DD.MM.YYYY': {date_str} -> {start_date}")
        return start_date, end_date
    # No pattern matched
    logger.debug(f"No date pattern matched for: {date_str}")
    raise ValueError(f"Date string doesn't match expected formats: {date_str}")


def parse_event_text(text: str) -> Dict[str, Optional[str]]:
    """Parse event text into structured data.

    Expected format: {name} ({location}, {organiser}, {date interval}) [{wre}]
    or {name} ({organiser}, {date interval}) [{wre}]
    Raises ValueError if text doesn't match the expected format.
    """
    # Extract WRE count if present
    wre_match = re.search(r"(\d+)\s*WRE", text)
    wre_count = int(wre_match.group(1)) if wre_match else 0

    # Remove WRE part for further parsing
    text_without_wre = re.sub(r"\s*\d+\s*WRE\s*", "", text)

    # Extract the main parts using regex
    # First try with location
    match = re.match(r"(.*?)\s*\((.*?),\s*(.*?),\s*(.*?)\)", text_without_wre)
    if match:
        name, location, organiser, date_str = match.groups()
    else:
        # Try without location
        match = re.match(r"(.*?)\s*\((.*?),\s*(.*?)\)", text_without_wre)
        if not match:
            raise ValueError(f"Text doesn't match expected format: {text}")
        name, organiser, date_str = match.groups()
        location = None

    if not date_str or not date_str.strip():
        raise ValueError(f"No date interval found in event text: {text}")

    start_date, end_date = parse_date_interval_to_iso(date_str)

    return {
        "text": text,  # Keep the original text
        "name": name.strip(),
        "organiser": organiser.strip(),
        "location": location.strip() if location is not None else None,
        "start_date": start_date,
        "end_date": end_date,
        "wre_count": wre_count,
    }


def extract_events(html_content: str) -> List[Dict[str, str]]:
    """Extract event information from HTML content."""
    soup = BeautifulSoup(html_content, "html5lib")
    events = []

    for i, p in enumerate(soup.body.find_all("p", recursive=False)):
        # Log the HTML source of the paragraph at DEEP_DEBUG level
        logger.log(5, "Paragraph %d HTML: %r", i, str(p))

        # Get text and normalize whitespace
        text = re.sub(r"\s+", " ", p.get_text()).strip()
        logger.debug("Paragraph %d: %r", i, text)

        # Skip empty paragraphs, headers, and year-only paragraphs
        if not text or text == "Evenimente" or re.match(r"^\d{4}$", text):
            logger.debug("Skipping paragraph %d: %r", i, text)
            continue

        # Remove links and their text
        for a in p.find_all("a"):
            link_text = a.get_text().strip()
            logger.log(5, "Removing link HTML: %r", str(a))
            logger.debug("Removing link: %r", link_text)
            a.decompose()

        # Get text again after removing links
        text = re.sub(r"\s+", " ", p.get_text()).strip()
        if not text:
            logger.debug("Skipping paragraph %d: Empty after removing links", i)
            continue

        # Stop at paragraphs starting with underscore
        if text.startswith("_"):
            logger.debug("Stopping at paragraph %d", i)
            break

        # Parse the event text into structured data
        event_data = parse_event_text(text)
        events.append(event_data)

    return events

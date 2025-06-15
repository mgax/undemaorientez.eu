from bs4 import BeautifulSoup
import re
import logging

logger = logging.getLogger(__name__)


def extract_events(html_content):
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

        events.append(text)
    return events

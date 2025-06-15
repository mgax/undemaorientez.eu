from pathlib import Path
import json
from oscraper.scraper.extract import extract_events


def test_extract_events():
    example_path = Path(__file__).parent / "data" / "scraped_example.html"
    with open(example_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    events = extract_events(html_content)

    result_path = Path(__file__).parent / "data" / "extract_result.json"
    with open(result_path, "r", encoding="utf-8") as f:
        expected_events = json.load(f)

    assert events == expected_events

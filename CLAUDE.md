# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

### Development Environment
- **Install dependencies**: `uv sync`
- **Run development server**: `uv run manage.py runserver`
- **Run tests**: `uv run pytest`
- **Create migrations**: `uv run manage.py makemigrations`
- **Apply migrations**: `uv run manage.py migrate`

### Management Commands
- **Fetch events**: `uv run manage.py fetch_events` - Downloads orienteering.ro events page
- **Extract events**: `uv run manage.py extract_events` - Parses HTML and extracts event data as JSON (use `-v` or `-v3` for debug output)
- **Import events**: `uv run manage.py import_events` - Creates draft Event pages in Wagtail CMS
- **Generate feed**: `uv run manage.py generate_feed` - Creates Atom RSS feed from events

## Architecture

### Project Structure
This is a Django project with Wagtail CMS integration for orienteering events management. The project consists of two main Django apps:

1. **`oscraper.scraper`** - Web scraping functionality
   - Fetches and parses orienteering.ro events page
   - Extracts structured event data from HTML
   - Generates RSS/Atom feeds

2. **`oscraper.cms`** - Wagtail CMS integration
   - Manages orienteering events as Wagtail pages
   - Provides admin interface for event management
   - Page models: HomePage (intro page) and Event (event details)

### Data Flow
1. `fetch_events` downloads HTML from orienteering.ro → `data/scraped/`
2. `extract_events` parses HTML → extracts event data with date parsing
3. `import_events` creates Wagtail Event pages from extracted data
4. `generate_feed` creates RSS feed from event data

### Key Components
- **Event extraction**: `oscraper/scraper/extract.py` - Complex date parsing logic for Romanian date formats
- **Event model**: `oscraper/cms/models.py` - Wagtail Event page with organiser, location, dates, original_text
- **Database**: SQLite stored in `data/db.sqlite3`
- **Scraped data**: Stored in `data/scraped/` directory

### Configuration
- Uses environment variables for configuration (DJANGO_SECRET_KEY required)
- Settings in `oscraper/settings.py`
- Database and scraped data stored in `data/` directory
- Timezone set to Europe/Bucharest

### Testing
- Test files in `tests/` subdirectories of each app
- Uses pytest with Django integration
- Test data stored in `tests/data/` directories

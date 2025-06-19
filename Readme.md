# Orienteering Scraper

## Overview

The Orienteering Scraper is a tool that scrapes the http://orienteering.ro website and extracts the events that are listed. It also includes a Wagtail CMS for managing orienteering events.

## Installation

This project uses `uv` for dependency management. To set up the project:

```bash
# Create virtual environment
uv venv

# Install dependencies
uv sync
```

## Environment Variables

This project uses environment variables for configuration. If you're using `direnv`, create a `.envrc` file in the project root with the following variables:

```bash
# Required: Django secret key for security
export DJANGO_SECRET_KEY="your-secret-key-here"

# Optional: Enable debug mode (1, yes, y, true = enabled, anything else = disabled)
export DJANGO_DEBUG="1"

# Optional: Base URL for the RSS feed (defaults to http://example.com)
export OSCRAPER_BASE_URL="http://localhost:8000"

# Optional: Base URL for Wagtail admin (defaults to http://localhost:8000)
export WAGTAILADMIN_BASE_URL="http://localhost:8000"
```

Run `direnv allow` to load the environment variables.

## Database Setup

After installation, you need to set up the database:

```bash
# Create and apply database migrations
uv run manage.py migrate

# Create a superuser for admin access
uv run manage.py createsuperuser
```

## Running the Site Locally

To run the development server:

```bash
uv run manage.py runserver
```

The site will be available at:
- **Main site**: http://localhost:8000/
- **Wagtail admin**: http://localhost:8000/admin/
- **Django admin**: http://localhost:8000/django-admin/

## Development

To set up pre-commit hooks (automatically enforces code quality and style standards):

```bash
pre-commit install
```

To add new dependencies:

```bash
uv add <package-name>
```

To update dependencies:

```bash
# Update lock file
uv lock
```

Run tests with:

```bash
uv run pytest
```

## Database Migrations

When you make changes to models, create and apply migrations:

```bash
# Create migrations for model changes
uv run manage.py makemigrations

# Apply migrations to the database
uv run manage.py migrate
```

## CMS Features

The project includes a Wagtail CMS with the following page types:

- **HomePage**: Root page for the site with an intro field
- **Event**: Pages for orienteering events with fields for:
  - Description (rich text)
  - Organiser
  - Location
  - Start date
  - End date
  - WRE count (World Ranking Event count)

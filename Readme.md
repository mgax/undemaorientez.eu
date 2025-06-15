# Orienteering Scraper

## Overview

The Orienteering Scraper is a tool that scrapes the http://orienteering.ro website and extracts the events that are listed.

## Installation

This project uses `uv` for dependency management. To set up the project:

```bash
# Create virtual environment
uv venv

# Install dependencies
uv sync
```

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

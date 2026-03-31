# IGOD.gov.in Link Scraper

## Overview

This project contains Python scripts for learning how to perform web scraping using Selenium and BeautifulSoup. It is designed to crawl pages on `https://igod.gov.in`, collect internal links for traversal, and store external links.

> **Important:** This code is provided for learning and security practice only. Do not use it against websites without permission. Use it responsibly and ethically.

## What the code does

- `Scrap.py`
  - A basic web scraper that starts from `https://igod.gov.in/categories`.
  - Uses Selenium to open the page and extract HTML from a `content-row` element.
  - Parses links with BeautifulSoup.
  - Adds links containing `igod.gov.in` to `totraverse.txt` for later traversal.
  - Writes non-`igod.gov.in` links to `finalized.txt`.

- `optimizedScrapper.py`
  - A more complete crawler with persistence and deduplication.
  - Maintains sets of `visited.txt`, `to_traverse.txt`, and `finalized.txt`.
  - Starts from `https://igod.gov.in/categories` when no `to_traverse.txt` exists.
  - Scrolls pages until content loading stabilizes.
  - Filters out `tel:`, `mailto:`, `javascript:` and `#` links.
  - For internal `igod.gov.in` links, it adds them to the traversal queue.
  - For external links, it inserts them into the database and stores them in `finalized.txt`.

- `database.py`
  - Provides MySQL connection helpers.
  - Contains both local and remote database connection options.
  - Includes a helper to kill a query if needed.

- `insert_on_database.py`
  - Connects to the database using `database.py`.
  - Inserts extracted external URLs into the `goverment_links` table.
  - Prints inserted links and retries on failure.

## Files

- `Scrap.py`
- `optimizedScrapper.py`
- `database.py`
- `insert_on_database.py`
- `visited.txt` - URLs already processed
- `to_traverse.txt` - URLs still to visit
- `finalized.txt` - Extracted external URLs
- `totraverse.txt` - Traversed internal URLs (older output format)

## Dependencies

- Python 3.x
- Selenium
- BeautifulSoup4
- PyMySQL
- ChromeDriver installed and the path updated correctly in `Scrap.py` and `optimizedScrapper.py`

Example install command:

```bash
pip install selenium beautifulsoup4 pymysql
```

## Usage

1. Update the ChromeDriver path in `Scrap.py` and `optimizedScrapper.py`:
   - `C:\Translation Exe\chromedriver.exe`
2. Run the optimized scraper:

```bash
python optimizedScrapper.py
```

## Notes

- This project is not production-ready. It is a learning exercise for web scraping and simple automation.
- The code includes manual paths and database credentials that should not be used in real deployments.
- Always respect website terms of service and robots.txt when scraping.

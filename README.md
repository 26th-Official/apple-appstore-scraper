# Apple App Store Scraper

A Scrapy-based scraper for the Apple App Store that extracts app information.

## Features

- Scrapes app details from the Apple App Store
- Extracts app name, user rating, developer, price, and URL
- **Pause and Resume functionality**: Allows you to pause and resume scraping
- **In-place counter**: Shows real-time progress with minimal logging

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/apple-appstore-scraper.git
cd apple-appstore-scraper
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage with Scrapy

```bash
scrapy crawl apps -o apps.json
```

### Using the Run Script with Pause/Resume Functionality

The project includes a custom script that makes it easy to pause and resume scraping:

```bash
python run_spider.py --output apps.json --format json
```

To pause the scraper, press `Ctrl+C` once. The script will gracefully pause the scraping process and save the current state.

To resume a previously paused scrape:

```bash
python run_spider.py --resume --output apps.json --format json
```

### Command Line Arguments

- `--resume`: Resume a previously paused crawl
- `--output`: Specify the output file path (default: apps.json)
- `--format`: Specify the output format (default: json)
- `--verbose`: Enable verbose logging (by default, logging is minimized)

## How Pause/Resume Works

The scraper uses Scrapy's built-in job persistence feature to save the state of the crawl. When you pause the scraper:

1. The current state is saved to the `crawls/appstore-jobs` directory
2. When you resume, the scraper picks up where it left off
3. Data is appended to the existing output file

## In-Place Counter

The scraper includes a custom extension that displays an in-place counter showing:
- Number of items scraped
- Current scraping rate (items per second)
- Final statistics when the scraper finishes

This provides real-time feedback while minimizing log output for a cleaner terminal experience.

## Notes

- The first time you press `Ctrl+C`, the scraper will pause gracefully
- If you press `Ctrl+C` a second time, the scraper will force quit without saving state
- The pause operation may take a moment to complete as it needs to finish processing current requests
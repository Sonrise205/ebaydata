# Eldorado Competitor Price Scraper

A Python tool that scrapes competitor pricing data from Eldorado.gg for Arc Raiders items.

## Features

- **Smart Item Matching**: Fuzzy matching handles title variations (Roman numerals, emojis, typos, etc.)
- **Comprehensive Data**: Collects seller username, price, rating, delivery time, and profile links
- **Profit Margin Calculation**: Automatically calculates margins based on your pricing
- **Dual Export Formats**: CSV for spreadsheets, formatted TXT for quick review
- **Rate Limiting**: Built-in delays to avoid getting blocked

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install Playwright browser
playwright install chromium
```

## Usage

### Basic Usage

```bash
# Scrape all items with prices (83 items)
python3 main.py

# Show database statistics only
python3 main.py --stats
```

### Filtering Options

```bash
# Only Top Seller items
python3 main.py --demand "Top Seller"

# Only first 10 items
python3 main.py --limit 10

# Show browser window (for debugging)
python3 main.py --no-headless

# Include items without prices
python3 main.py --all
```

## Output Files

Results are saved to the `output/` directory:

- `competitor_data.csv` - Raw data for spreadsheet analysis
- `competitor_report.txt` - Formatted human-readable report

### CSV Columns

| Column | Description |
|--------|-------------|
| item_name | Item name from database |
| demand | Demand level (Top Seller, Mid Demand, etc.) |
| category | Item category |
| our_price_low | Our low price |
| our_price_high | Our high price |
| seller_username | Competitor's username |
| seller_url | Link to seller's profile |
| seller_price | Competitor's price |
| seller_rating | Seller rating and review count |
| margin_low | Profit margin vs low price |
| margin_high | Profit margin vs high price |

## Database

The item database contains 207 Arc Raiders items categorized by demand:

- **Top Seller**: 21 items
- **Mid Demand**: 24 items
- **Low Demand**: 30 items
- **Rare**: 6 items
- **Dead Stock**: 126 items

Only items with prices set (83 items) are scraped by default.

## Configuration

Edit `config.py` to customize:

```python
# Scraping delays (seconds)
REQUEST_DELAY_MIN = 3.0
REQUEST_DELAY_MAX = 4.0

# Matching threshold (0-100)
FUZZY_MATCH_THRESHOLD = 75

# Output directory
OUTPUT_DIR = "output"
```

## Smart Matching Examples

The matcher handles various title variations:

| Database Item | Listing Title | Match |
|--------------|---------------|-------|
| Angled Grip II Blueprint | angled grip 2 blueprint | ✓ |
| Angled Grip II Blueprint | ANGLED GRIP II BLUEPRINT | ✓ |
| Angled Grip II Blueprint | ⭐ANGLED GRIP II BLUEPRINT⭐ | ✓ |
| Bobcat Blueprint | Bobcat Blueprint Fast Delivery | ✓ |
| Bobcat Blueprint | Wolfpack Blueprint | ✗ |

## Estimated Runtime

| Items | Time |
|-------|------|
| 10 items | ~40 seconds |
| 50 items | ~3-4 minutes |
| 83 items (all with prices) | ~5-6 minutes |
| 207 items (all) | ~14-15 minutes |

## License

MIT

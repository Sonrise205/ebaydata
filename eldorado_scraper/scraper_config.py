# config.py - Configuration for Eldorado Scraper

# Base URLs
BASE_URL = "https://www.eldorado.gg"
ARC_RAIDERS_ITEMS_URL = "https://www.eldorado.gg/arc-raiders-items/i/319"
SELLER_PROFILE_URL_TEMPLATE = "https://www.eldorado.gg/users/{username}?category=CustomItem&tab=Offers"

# Scraping settings
REQUEST_DELAY_MIN = 3.0  # Minimum delay between requests (seconds)
REQUEST_DELAY_MAX = 4.0  # Maximum delay between requests (seconds)
PAGE_LOAD_TIMEOUT = 30000  # Page load timeout (milliseconds)
SEARCH_RESULT_WAIT = 2000  # Wait for search results (milliseconds)

# Matching settings
FUZZY_MATCH_THRESHOLD = 75  # Minimum fuzzy match score (0-100)

# Output settings
OUTPUT_DIR = "output"
CSV_FILENAME = "competitor_data.csv"
TXT_FILENAME = "competitor_report.txt"

# Browser settings
HEADLESS = True  # Run browser in headless mode
SLOW_MO = 100  # Slow down browser actions (milliseconds)

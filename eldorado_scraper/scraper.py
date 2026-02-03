# scraper.py - Playwright-based Eldorado Scraper
# Scrapes competitor listings from Eldorado.gg for Arc Raiders items

import asyncio
import random
import re
from datetime import datetime
from typing import Optional
from playwright.async_api import async_playwright, Page, Browser, TimeoutError as PlaywrightTimeout

import config
from matcher import is_match, calculate_match_score


class EldoradoScraper:
    """
    Scraper for Eldorado.gg Arc Raiders items marketplace.
    """
    
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.playwright = None
        
    async def start(self):
        """Initialize the browser."""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=self.headless,
            slow_mo=config.SLOW_MO
        )
        self.page = await self.browser.new_page()
        
        # Set viewport
        await self.page.set_viewport_size({"width": 1920, "height": 1080})
        
        # Set a realistic user agent
        await self.page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })
        
        print(f"[{self._timestamp()}] Browser started (headless={self.headless})")
        
    async def stop(self):
        """Close the browser."""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        print(f"[{self._timestamp()}] Browser closed")
        
    def _timestamp(self) -> str:
        return datetime.now().strftime("%H:%M:%S")
    
    async def _random_delay(self):
        """Random delay between requests to avoid rate limiting."""
        delay = random.uniform(config.REQUEST_DELAY_MIN, config.REQUEST_DELAY_MAX)
        await asyncio.sleep(delay)
        
    async def navigate_to_items_page(self):
        """Navigate to Arc Raiders items page."""
        try:
            await self.page.goto(config.ARC_RAIDERS_ITEMS_URL, timeout=config.PAGE_LOAD_TIMEOUT)
            await self.page.wait_for_load_state("networkidle")
            print(f"[{self._timestamp()}] Navigated to Arc Raiders items page")
            return True
        except PlaywrightTimeout:
            print(f"[{self._timestamp()}] Timeout navigating to items page")
            return False
        except Exception as e:
            print(f"[{self._timestamp()}] Error navigating: {e}")
            return False
    
    async def search_item(self, item_name: str) -> bool:
        """
        Search for an item on the page.
        
        Args:
            item_name: The item name to search for
            
        Returns:
            True if search was successful
        """
        try:
            # Find the search input
            search_input = self.page.locator("input[placeholder='Search Items']")
            
            # Wait for it to be visible
            await search_input.wait_for(state="visible", timeout=5000)
            
            # Clear any existing search
            await search_input.click()
            await self.page.keyboard.press("Control+A")
            await self.page.keyboard.press("Backspace")
            
            # Type the search query
            await search_input.fill(item_name)
            
            # Press Enter to search
            await self.page.keyboard.press("Enter")
            
            # Wait for results to load
            await asyncio.sleep(config.SEARCH_RESULT_WAIT / 1000)
            
            # Wait for offer items to appear (or "no results" message)
            try:
                await self.page.wait_for_selector("eld-offer-item, .no-results", timeout=5000)
            except PlaywrightTimeout:
                pass  # Results may already be loaded
            
            return True
            
        except Exception as e:
            print(f"[{self._timestamp()}] Error searching for '{item_name}': {e}")
            return False
    
    async def clear_filters(self):
        """Clear any existing filters on the page."""
        try:
            clear_btn = self.page.locator("text=Clear filters")
            if await clear_btn.count() > 0:
                await clear_btn.click()
                await asyncio.sleep(0.5)
        except:
            pass  # No filters to clear
    
    async def scrape_listings(self) -> list:
        """
        Scrape all visible listings from the current page.
        
        Returns:
            List of listing dictionaries
        """
        listings = []
        
        try:
            # Wait for offer items
            await self.page.wait_for_selector("eld-offer-item", timeout=5000)
            
            # Get all offer items
            offer_elements = self.page.locator("eld-offer-item")
            count = await offer_elements.count()
            
            for i in range(count):
                try:
                    element = offer_elements.nth(i)
                    listing = await self._extract_listing_data(element)
                    if listing:
                        listings.append(listing)
                except Exception as e:
                    # Skip problematic listings
                    continue
                    
        except PlaywrightTimeout:
            # No listings found
            pass
        except Exception as e:
            print(f"[{self._timestamp()}] Error scraping listings: {e}")
            
        return listings
    
    async def _extract_listing_data(self, element) -> Optional[dict]:
        """
        Extract data from a single offer element.
        
        Args:
            element: Playwright locator for the offer element
            
        Returns:
            Dictionary with listing data or None
        """
        try:
            # Get the offer title
            title_el = element.locator(".offer-title")
            title = await title_el.inner_text() if await title_el.count() > 0 else ""
            title = title.strip()
            
            # Get seller username
            username_el = element.locator(".seller-details .username")
            username = await username_el.inner_text() if await username_el.count() > 0 else "Unknown"
            username = username.strip()
            
            # Get price
            price_el = element.locator("eld-offer-price strong")
            price_text = await price_el.inner_text() if await price_el.count() > 0 else "$0"
            price = self._parse_price(price_text)
            
            # Get seller rating
            rating_el = element.locator(".seller-details > div:last-child")
            rating_text = ""
            if await rating_el.count() > 0:
                rating_text = await rating_el.inner_text()
            rating_text = rating_text.strip()
            
            # Get delivery time
            delivery_el = element.locator(".offer-delivery .value")
            delivery = await delivery_el.inner_text() if await delivery_el.count() > 0 else "N/A"
            delivery = delivery.strip()
            
            # Get item type/category tags
            tags = []
            tag_elements = element.locator("eld-trade-env-item span[data-testid]")
            tag_count = await tag_elements.count()
            for j in range(tag_count):
                tag_text = await tag_elements.nth(j).inner_text()
                tags.append(tag_text.strip())
            
            # Construct seller profile URL
            seller_url = config.SELLER_PROFILE_URL_TEMPLATE.format(username=username)
            
            return {
                "title": title,
                "seller_username": username,
                "seller_url": seller_url,
                "price": price,
                "price_text": price_text.strip(),
                "rating": rating_text,
                "delivery_time": delivery,
                "tags": tags,
                "scraped_at": datetime.now().isoformat(),
            }
            
        except Exception as e:
            return None
    
    def _parse_price(self, price_text: str) -> float:
        """Parse price text like '$3.90' to float."""
        try:
            # Remove $ and any non-numeric chars except .
            cleaned = re.sub(r'[^\d.]', '', price_text)
            return float(cleaned) if cleaned else 0.0
        except ValueError:
            return 0.0
    
    async def get_results_count(self) -> int:
        """Get the number of results found."""
        try:
            count_el = self.page.locator("eld-results-count .results-count")
            if await count_el.count() > 0:
                text = await count_el.inner_text()
                # Extract number from "31 items found"
                match = re.search(r'(\d+)', text)
                if match:
                    return int(match.group(1))
        except:
            pass
        return 0
    
    async def scrape_item(self, item_name: str, item_category: str = None, match_threshold: int = 75) -> dict:
        """
        Search for and scrape listings for a specific item.
        
        Args:
            item_name: Item name from our database
            item_category: Item category for matching bonus
            match_threshold: Minimum match score
            
        Returns:
            Dictionary with item data and matched listings
        """
        result = {
            "item_name": item_name,
            "item_category": item_category,
            "search_time": datetime.now().isoformat(),
            "total_results": 0,
            "matched_listings": [],
            "all_listings": [],
            "error": None,
        }
        
        try:
            # Search for the item
            search_success = await self.search_item(item_name)
            
            if not search_success:
                result["error"] = "Search failed"
                return result
            
            # Get results count
            result["total_results"] = await self.get_results_count()
            
            # Scrape all visible listings
            all_listings = await self.scrape_listings()
            result["all_listings"] = all_listings
            
            # Filter listings that match our item
            matched = []
            for listing in all_listings:
                match_result = calculate_match_score(item_name, listing["title"], item_category)
                if match_result["score"] >= match_threshold:
                    listing["match_score"] = match_result["score"]
                    matched.append(listing)
            
            result["matched_listings"] = matched
            
        except Exception as e:
            result["error"] = str(e)
            
        return result


async def scrape_all_items(items: list, headless: bool = True, progress_callback=None) -> list:
    """
    Scrape competitor data for all items.
    
    Args:
        items: List of item dictionaries from database
        headless: Run browser in headless mode
        progress_callback: Optional callback function(current, total, item_name)
        
    Returns:
        List of scrape results
    """
    scraper = EldoradoScraper(headless=headless)
    results = []
    
    try:
        await scraper.start()
        
        # Navigate to the items page
        if not await scraper.navigate_to_items_page():
            print("Failed to navigate to items page")
            return results
        
        # Clear any filters
        await scraper.clear_filters()
        
        total = len(items)
        
        for i, item in enumerate(items, 1):
            item_name = item["name"]
            item_category = item.get("category")
            
            if progress_callback:
                progress_callback(i, total, item_name)
            else:
                print(f"[{scraper._timestamp()}] [{i}/{total}] Scraping: {item_name}")
            
            # Scrape this item
            result = await scraper.scrape_item(item_name, item_category)
            
            # Add our price info to the result
            result["our_price_low"] = item.get("our_price_low")
            result["our_price_high"] = item.get("our_price_high")
            result["our_price_str"] = item.get("our_price_str")
            result["demand"] = item.get("demand")
            
            results.append(result)
            
            # Log match summary
            matched_count = len(result["matched_listings"])
            if result["error"]:
                print(f"         ⚠️  Error: {result['error']}")
            elif matched_count > 0:
                lowest_price = min(l["price"] for l in result["matched_listings"])
                print(f"         ✓ {matched_count} matches found (lowest: ${lowest_price:.2f})")
            else:
                print(f"         ○ No matches found")
            
            # Delay between requests
            if i < total:
                await scraper._random_delay()
                
    finally:
        await scraper.stop()
    
    return results


# ============================================================================
# Quick test
# ============================================================================
if __name__ == "__main__":
    async def test():
        from items_database import get_searchable_items
        
        # Get first 3 items for testing
        items = get_searchable_items()[:3]
        
        print("=" * 60)
        print("SCRAPER TEST (first 3 items)")
        print("=" * 60)
        
        results = await scrape_all_items(items, headless=True)
        
        print("\n" + "=" * 60)
        print("RESULTS SUMMARY")
        print("=" * 60)
        
        for result in results:
            print(f"\n{result['item_name']}:")
            print(f"  Total results: {result['total_results']}")
            print(f"  Matched: {len(result['matched_listings'])}")
            if result['matched_listings']:
                for listing in result['matched_listings'][:3]:
                    print(f"    - {listing['seller_username']}: ${listing['price']:.2f}")
    
    asyncio.run(test())

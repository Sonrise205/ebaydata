#!/usr/bin/env python3
# main.py - Entry point for Eldorado Competitor Scraper
# Scrapes competitor pricing data from Eldorado.gg for Arc Raiders items

import asyncio
import argparse
import sys
from datetime import datetime

import scraper_config as config
from items_database import build_items_database, get_searchable_items, get_items_by_demand
from scraper import scrape_all_items
from exporter import export_results, export_to_csv, export_to_txt


def print_banner():
    """Print application banner."""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ███████╗██╗     ██████╗  ██████╗ ██████╗  █████╗ ██████╗  ██████╗          ║
║   ██╔════╝██║     ██╔══██╗██╔═══██╗██╔══██╗██╔══██╗██╔══██╗██╔═══██╗         ║
║   █████╗  ██║     ██║  ██║██║   ██║██████╔╝███████║██║  ██║██║   ██║         ║
║   ██╔══╝  ██║     ██║  ██║██║   ██║██╔══██╗██╔══██║██║  ██║██║   ██║         ║
║   ███████╗███████╗██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝╚██████╔╝         ║
║   ╚══════╝╚══════╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝          ║
║                                                                              ║
║                    COMPETITOR PRICE SCRAPER                                  ║
║                       Arc Raiders Items                                      ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    print(banner)


def print_stats():
    """Print database statistics."""
    all_items = build_items_database()
    searchable = get_searchable_items()
    
    print("📊 DATABASE STATISTICS")
    print("=" * 50)
    print(f"   Total items in database: {len(all_items)}")
    print(f"   Items with prices (searchable): {len(searchable)}")
    print()
    
    # Count by demand
    from collections import Counter
    demand_counts = Counter(item["demand"] for item in all_items)
    searchable_counts = Counter(item["demand"] for item in searchable)
    
    print("   By Demand Level:")
    for demand in ["Top Seller", "Mid Demand", "Low Demand", "Rare", "Dead Stock"]:
        total = demand_counts.get(demand, 0)
        search = searchable_counts.get(demand, 0)
        print(f"     {demand}: {total} total, {search} searchable")
    print()


def progress_callback(current: int, total: int, item_name: str):
    """Progress callback for scraping."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    pct = (current / total) * 100
    print(f"[{timestamp}] [{current}/{total}] ({pct:.1f}%) Scraping: {item_name}")


async def run_scraper(
    demand_filter: str = None,
    limit: int = None,
    headless: bool = True,
    skip_no_price: bool = True,
):
    """
    Run the scraper with specified options.
    
    Args:
        demand_filter: Filter by demand level (e.g., "Top Seller")
        limit: Limit number of items to scrape
        headless: Run browser in headless mode
        skip_no_price: Skip items without prices
    """
    print_banner()
    print_stats()
    
    # Get items to scrape
    if skip_no_price:
        items = get_searchable_items()
        print(f"📋 Using searchable items only (with prices)")
    else:
        items = build_items_database()
        print(f"📋 Using all items (including no-price)")
    
    # Filter by demand if specified
    if demand_filter:
        items = [i for i in items if i["demand"] == demand_filter]
        print(f"   Filtered by demand: {demand_filter}")
    
    # Limit if specified
    if limit:
        items = items[:limit]
        print(f"   Limited to: {limit} items")
    
    print(f"\n🎯 Items to scrape: {len(items)}")
    print(f"⏱️  Estimated time: {len(items) * 4} - {len(items) * 5} seconds")
    print()
    
    if not items:
        print("❌ No items to scrape!")
        return
    
    # Confirm before starting
    print("─" * 50)
    print("Press ENTER to start scraping (or Ctrl+C to cancel)...")
    try:
        input()
    except KeyboardInterrupt:
        print("\n❌ Cancelled by user")
        return
    
    print()
    print("🚀 STARTING SCRAPER")
    print("=" * 50)
    
    start_time = datetime.now()
    
    # Run scraper
    results = await scrape_all_items(
        items,
        headless=headless,
        progress_callback=progress_callback
    )
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print()
    print("=" * 50)
    print(f"✅ SCRAPING COMPLETE")
    print(f"   Duration: {duration:.1f} seconds")
    print(f"   Items scraped: {len(results)}")
    
    # Count results
    items_with_matches = sum(1 for r in results if r.get("matched_listings"))
    total_listings = sum(len(r.get("matched_listings", [])) for r in results)
    
    print(f"   Items with matches: {items_with_matches}")
    print(f"   Total competitor listings: {total_listings}")
    print()
    
    # Export results
    print("📁 EXPORTING RESULTS")
    print("=" * 50)
    
    csv_path, txt_path = export_results(results)
    
    print(f"   CSV: {csv_path}")
    print(f"   TXT: {txt_path}")
    print()
    
    print("🎉 ALL DONE!")
    print()
    
    return results


def main():
    """Main entry point with CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description="Eldorado Competitor Price Scraper for Arc Raiders",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                           # Scrape all items with prices
  python main.py --demand "Top Seller"     # Only Top Seller items
  python main.py --limit 10                # First 10 items only
  python main.py --no-headless             # Show browser window
  python main.py --all                     # Include items without prices
        """
    )
    
    parser.add_argument(
        "--demand",
        choices=["Top Seller", "Mid Demand", "Low Demand", "Rare", "Dead Stock"],
        help="Filter by demand level"
    )
    
    parser.add_argument(
        "--limit",
        type=int,
        help="Limit number of items to scrape"
    )
    
    parser.add_argument(
        "--no-headless",
        action="store_true",
        help="Show browser window (not headless)"
    )
    
    parser.add_argument(
        "--all",
        action="store_true",
        help="Include items without prices"
    )
    
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show database statistics and exit"
    )
    
    args = parser.parse_args()
    
    # Stats only mode
    if args.stats:
        print_banner()
        print_stats()
        return
    
    # Run the scraper
    asyncio.run(run_scraper(
        demand_filter=args.demand,
        limit=args.limit,
        headless=not args.no_headless,
        skip_no_price=not args.all,
    ))


if __name__ == "__main__":
    main()

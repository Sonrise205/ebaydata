# exporter.py - Export scrape results to CSV and formatted TXT reports

import csv
import os
from datetime import datetime
from typing import List, Optional

import scraper_config as config


def calculate_margin(our_price: Optional[float], competitor_price: float) -> tuple:
    """
    Calculate profit margin.
    
    Returns:
        (margin_dollars, margin_percent) or (None, None) if can't calculate
    """
    if our_price is None or competitor_price <= 0:
        return None, None
    
    margin_dollars = our_price - competitor_price
    margin_percent = (margin_dollars / competitor_price) * 100
    
    return margin_dollars, margin_percent


def format_margin(margin_dollars: Optional[float], margin_percent: Optional[float]) -> str:
    """Format margin for display."""
    if margin_dollars is None:
        return "N/A"
    
    sign = "+" if margin_dollars >= 0 else ""
    return f"{sign}${margin_dollars:.2f} ({sign}{margin_percent:.0f}%)"


def ensure_output_dir():
    """Create output directory if it doesn't exist."""
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)


def export_to_csv(results: List[dict], filename: str = None) -> str:
    """
    Export scrape results to CSV file.
    
    Args:
        results: List of scrape result dictionaries
        filename: Output filename (default from config)
        
    Returns:
        Path to the created CSV file
    """
    ensure_output_dir()
    
    if filename is None:
        filename = config.CSV_FILENAME
    
    filepath = os.path.join(config.OUTPUT_DIR, filename)
    
    # CSV columns
    fieldnames = [
        "item_name",
        "demand",
        "category",
        "our_price_low",
        "our_price_high",
        "seller_username",
        "seller_url",
        "seller_price",
        "seller_rating",
        "delivery_time",
        "match_score",
        "margin_low",
        "margin_low_pct",
        "margin_high",
        "margin_high_pct",
        "listing_title",
        "scraped_at",
    ]
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for result in results:
            item_name = result["item_name"]
            demand = result.get("demand", "")
            category = result.get("item_category", "")
            our_low = result.get("our_price_low")
            our_high = result.get("our_price_high")
            
            # Write a row for each matched listing
            for listing in result.get("matched_listings", []):
                seller_price = listing.get("price", 0)
                
                # Calculate margins
                margin_low, margin_low_pct = calculate_margin(our_low, seller_price)
                margin_high, margin_high_pct = calculate_margin(our_high, seller_price)
                
                row = {
                    "item_name": item_name,
                    "demand": demand,
                    "category": category,
                    "our_price_low": our_low,
                    "our_price_high": our_high,
                    "seller_username": listing.get("seller_username", ""),
                    "seller_url": listing.get("seller_url", ""),
                    "seller_price": seller_price,
                    "seller_rating": listing.get("rating", ""),
                    "delivery_time": listing.get("delivery_time", ""),
                    "match_score": listing.get("match_score", 0),
                    "margin_low": margin_low,
                    "margin_low_pct": f"{margin_low_pct:.1f}%" if margin_low_pct else "",
                    "margin_high": margin_high,
                    "margin_high_pct": f"{margin_high_pct:.1f}%" if margin_high_pct else "",
                    "listing_title": listing.get("title", ""),
                    "scraped_at": listing.get("scraped_at", ""),
                }
                writer.writerow(row)
            
            # If no matches, write a row indicating that
            if not result.get("matched_listings"):
                row = {
                    "item_name": item_name,
                    "demand": demand,
                    "category": category,
                    "our_price_low": our_low,
                    "our_price_high": our_high,
                    "seller_username": "NO_LISTINGS_FOUND",
                    "seller_url": "",
                    "seller_price": "",
                    "seller_rating": "",
                    "delivery_time": "",
                    "match_score": "",
                    "margin_low": "",
                    "margin_low_pct": "",
                    "margin_high": "",
                    "margin_high_pct": "",
                    "listing_title": result.get("error", "No matches"),
                    "scraped_at": result.get("search_time", ""),
                }
                writer.writerow(row)
    
    return filepath


def export_to_txt(results: List[dict], filename: str = None) -> str:
    """
    Export scrape results to formatted TXT report.
    
    Args:
        results: List of scrape result dictionaries
        filename: Output filename (default from config)
        
    Returns:
        Path to the created TXT file
    """
    ensure_output_dir()
    
    if filename is None:
        filename = config.TXT_FILENAME
    
    filepath = os.path.join(config.OUTPUT_DIR, filename)
    
    # Build the report
    lines = []
    
    # Header
    lines.append("═" * 80)
    lines.append("                    ELDORADO COMPETITOR ANALYSIS")
    lines.append("                         Arc Raiders Items")
    lines.append(f"                    Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("═" * 80)
    lines.append("")
    
    # Group results by demand
    demand_groups = {}
    for result in results:
        demand = result.get("demand", "Unknown")
        if demand not in demand_groups:
            demand_groups[demand] = []
        demand_groups[demand].append(result)
    
    # Define demand order
    demand_order = ["Top Seller", "Mid Demand", "Low Demand", "Rare", "Dead Stock", "Unknown"]
    
    # Statistics
    total_items = len(results)
    items_with_listings = sum(1 for r in results if r.get("matched_listings"))
    items_no_listings = total_items - items_with_listings
    
    # Summary section
    lines.append("┌" + "─" * 78 + "┐")
    lines.append("│" + " SUMMARY".ljust(78) + "│")
    lines.append("├" + "─" * 78 + "┤")
    lines.append(f"│  Total Items Searched: {total_items}".ljust(79) + "│")
    lines.append(f"│  Items with Competitors: {items_with_listings}".ljust(79) + "│")
    lines.append(f"│  Items with No Listings: {items_no_listings}".ljust(79) + "│")
    lines.append("└" + "─" * 78 + "┘")
    lines.append("")
    
    # Process each demand group
    for demand in demand_order:
        if demand not in demand_groups:
            continue
        
        group = demand_groups[demand]
        
        lines.append("┌" + "─" * 78 + "┐")
        lines.append(f"│  {demand.upper()} ITEMS ({len(group)} items)".ljust(79) + "│")
        lines.append("└" + "─" * 78 + "┘")
        lines.append("")
        
        for result in group:
            item_name = result["item_name"]
            our_price_str = result.get("our_price_str", "N/A")
            our_low = result.get("our_price_low")
            our_high = result.get("our_price_high")
            category = result.get("item_category", "N/A")
            matched = result.get("matched_listings", [])
            error = result.get("error")
            
            lines.append(f"📦 {item_name}")
            lines.append(f"   Our Price: {our_price_str} | Category: {category}")
            
            if error:
                lines.append(f"   ⚠️  Error: {error}")
            elif not matched:
                lines.append("   ⚠️  NO LISTINGS FOUND (item may be out of stock on Eldorado)")
            else:
                # Table header
                lines.append("   ┌" + "─" * 90 + "┐")
                header = f"   │ {'Seller':<18} │ {'Price':>7} │ {'Rating':<16} │ {'Margin(Low)':>15} │ {'Margin(High)':>15} │"
                lines.append(header)
                lines.append("   ├" + "─" * 90 + "┤")
                
                # Sort by price
                sorted_listings = sorted(matched, key=lambda x: x.get("price", 999))
                
                for listing in sorted_listings[:15]:  # Max 15 per item
                    seller = listing.get("seller_username", "Unknown")[:18]
                    price = listing.get("price", 0)
                    rating = listing.get("rating", "")[:16]
                    
                    # Calculate margins
                    margin_low, margin_low_pct = calculate_margin(our_low, price)
                    margin_high, margin_high_pct = calculate_margin(our_high, price)
                    
                    margin_low_str = format_margin(margin_low, margin_low_pct)[:15]
                    margin_high_str = format_margin(margin_high, margin_high_pct)[:15]
                    
                    row = f"   │ {seller:<18} │ ${price:>6.2f} │ {rating:<16} │ {margin_low_str:>15} │ {margin_high_str:>15} │"
                    lines.append(row)
                
                lines.append("   └" + "─" * 90 + "┘")
                
                # Seller links
                if matched:
                    lines.append("")
                    lines.append("   Seller Links:")
                    for i, listing in enumerate(sorted_listings[:10], 1):
                        url = listing.get("seller_url", "")
                        seller = listing.get("seller_username", "Unknown")
                        lines.append(f"   [{i}] {seller}: {url}")
                
                # Summary stats
                if matched:
                    prices = [l.get("price", 0) for l in matched if l.get("price", 0) > 0]
                    if prices:
                        lowest = min(prices)
                        avg = sum(prices) / len(prices)
                        lines.append("")
                        lines.append(f"   📊 Summary: {len(matched)} sellers | Lowest: ${lowest:.2f} | Avg: ${avg:.2f}")
            
            lines.append("")
            lines.append("─" * 80)
            lines.append("")
    
    # Top profit opportunities
    lines.append("")
    lines.append("═" * 80)
    lines.append("                         TOP PROFIT OPPORTUNITIES")
    lines.append("═" * 80)
    lines.append("")
    
    # Find items with best margins
    opportunities = []
    for result in results:
        our_low = result.get("our_price_low")
        if our_low is None:
            continue
        
        matched = result.get("matched_listings", [])
        if not matched:
            continue
        
        lowest_price = min(l.get("price", 999) for l in matched)
        margin_dollars, margin_pct = calculate_margin(our_low, lowest_price)
        
        if margin_dollars and margin_pct:
            opportunities.append({
                "item": result["item_name"],
                "lowest_competitor": lowest_price,
                "our_price": our_low,
                "margin": margin_dollars,
                "margin_pct": margin_pct,
            })
    
    # Sort by margin percent descending
    opportunities.sort(key=lambda x: x["margin_pct"], reverse=True)
    
    for i, opp in enumerate(opportunities[:15], 1):
        lines.append(f"  {i:2}. {opp['item']}")
        lines.append(f"      Lowest competitor: ${opp['lowest_competitor']:.2f} | Your price: ${opp['our_price']:.2f}")
        lines.append(f"      Margin: +${opp['margin']:.2f} (+{opp['margin_pct']:.0f}%)")
        lines.append("")
    
    # Footer
    lines.append("")
    lines.append("═" * 80)
    lines.append(f"Report generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("═" * 80)
    
    # Write to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    return filepath


def export_results(results: List[dict]) -> tuple:
    """
    Export results to both CSV and TXT formats.
    
    Args:
        results: List of scrape result dictionaries
        
    Returns:
        Tuple of (csv_path, txt_path)
    """
    csv_path = export_to_csv(results)
    txt_path = export_to_txt(results)
    
    return csv_path, txt_path


# ============================================================================
# Test with sample data
# ============================================================================
if __name__ == "__main__":
    # Sample test data
    sample_results = [
        {
            "item_name": "Bobcat Blueprint",
            "item_category": "Blueprints",
            "demand": "Top Seller",
            "our_price_low": 4.99,
            "our_price_high": 6.99,
            "our_price_str": "$4.99-$6.99",
            "search_time": datetime.now().isoformat(),
            "total_results": 15,
            "matched_listings": [
                {
                    "title": "Bobcat Blueprint Fast Delivery",
                    "seller_username": "Kond",
                    "seller_url": "https://www.eldorado.gg/users/Kond?category=CustomItem&tab=Offers",
                    "price": 3.90,
                    "rating": "100% (4046)",
                    "delivery_time": "20 min",
                    "match_score": 95,
                    "scraped_at": datetime.now().isoformat(),
                },
                {
                    "title": "BOBCAT BLUEPRINT",
                    "seller_username": "EZtrader",
                    "seller_url": "https://www.eldorado.gg/users/EZtrader?category=CustomItem&tab=Offers",
                    "price": 1.00,
                    "rating": "99.6% (47709)",
                    "delivery_time": "20 min",
                    "match_score": 92,
                    "scraped_at": datetime.now().isoformat(),
                },
            ],
            "error": None,
        },
        {
            "item_name": "Wolfpack",
            "item_category": "Weapons",
            "demand": "Top Seller",
            "our_price_low": 2.99,
            "our_price_high": 2.99,
            "our_price_str": "$2.99",
            "search_time": datetime.now().isoformat(),
            "total_results": 0,
            "matched_listings": [],
            "error": None,
        },
    ]
    
    print("Testing export functions...")
    csv_path, txt_path = export_results(sample_results)
    print(f"CSV exported to: {csv_path}")
    print(f"TXT exported to: {txt_path}")
    
    # Print TXT content
    print("\n" + "=" * 60)
    print("TXT REPORT PREVIEW:")
    print("=" * 60)
    with open(txt_path, 'r') as f:
        print(f.read())

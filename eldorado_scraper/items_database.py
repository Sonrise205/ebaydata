# items_database.py - Arc Raiders Items Database
# Contains all items with their demand levels and our prices

def parse_price(price_str):
    """Parse price string like '$4.99-$6.99' or '$2.99' or 'Varies' or '—'"""
    if not price_str or price_str in ['—', 'Varies', 'OOS', '']:
        return None, None
    
    price_str = price_str.replace('$', '').strip()
    
    if '-' in price_str:
        parts = price_str.split('-')
        try:
            low = float(parts[0].strip())
            high = float(parts[1].strip())
            return low, high
        except ValueError:
            return None, None
    else:
        try:
            price = float(price_str.strip())
            return price, price
        except ValueError:
            return None, None


# ============================================================================
# TOP SELLER ITEMS (21 items)
# ============================================================================
TOP_SELLER_ITEMS = [
    {"name": "Bobcat Blueprint", "category": "Blueprints", "our_price": "$4.99-$6.99"},
    {"name": "Wolfpack", "category": "Weapons", "our_price": "$2.99"},
    {"name": "Tempest Blueprint", "category": "Blueprints", "our_price": "$8.99-$12.99"},
    {"name": "Equalizer", "category": "Weapons", "our_price": "$3.49"},
    {"name": "Vulcano Blueprint", "category": "Blueprints", "our_price": "$5.99-$7.99"},
    {"name": "Wolfpack Blueprint", "category": "Blueprints", "our_price": "$3.99-$4.99"},
    {"name": "Aphelion", "category": "Weapons", "our_price": "$3.99-$4.99"},
    {"name": "Jupiter", "category": "Weapons", "our_price": "$3.99-$4.99"},
    {"name": "Venator Blueprint", "category": "Blueprints", "our_price": "$5.49"},
    {"name": "Snap Hook", "category": "Weapons", "our_price": "$4.49"},
    {"name": "Deadline", "category": "Weapons", "our_price": "$3.49"},
    {"name": "Vita Spray", "category": "Cosmetics & Misc", "our_price": "$3.49"},
    {"name": "Snap Hook Blueprint", "category": "Blueprints", "our_price": "$4.99-$7.99"},
    {"name": "Vita Spray Blueprint", "category": "Blueprints", "our_price": "$5.99-$7.99"},
    {"name": "Vita Shot Blueprint", "category": "Blueprints", "our_price": "$4-$6"},
    {"name": "Looting Mk.3 (Survivor) Blueprint", "category": "Blueprints", "our_price": "$5.99-$8.99"},
    {"name": "Extended Light Mag III Blueprint", "category": "Blueprints", "our_price": "$3.99-$5.99"},
    {"name": "Custom Orders", "category": "Cosmetics & Misc", "our_price": "Varies"},
    {"name": "Electrician BP Emerald Wave", "category": "Cosmetics & Misc", "our_price": "$15-$25"},
    {"name": "Hiker Backpack Sky Ice", "category": "Cosmetics & Misc", "our_price": "$8-$12"},
    {"name": "Looting MK3 Surv x2 (Augment)", "category": "Cosmetics & Misc", "our_price": "$1.49-$2.49"},
]

# ============================================================================
# MID DEMAND ITEMS (24 items)
# ============================================================================
MID_DEMAND_ITEMS = [
    {"name": "Anvil Blueprint", "category": "Blueprints", "our_price": "$3.49-$3.89"},
    {"name": "Aphelion Blueprint", "category": "Blueprints", "our_price": "$1.99"},
    {"name": "Equalizer Blueprint", "category": "Blueprints", "our_price": "$4.99"},
    {"name": "Kinetic Converter", "category": "Weapons", "our_price": "$3.49"},
    {"name": "Il Toro Blueprint", "category": "Blueprints", "our_price": "$4.99"},
    {"name": "Queen Reactor", "category": "Materials & Bundles", "our_price": "$3.49"},
    {"name": "500K Coins", "category": "Cosmetics & Misc", "our_price": "$15-$17"},
    {"name": "Extended Barrel mod", "category": "Materials & Bundles", "our_price": "$2.49"},
    {"name": "Bobcat IV", "category": "Weapons", "our_price": "$2.49"},
    {"name": "Looting Mk.3 (Safekeeper) Blueprint", "category": "Blueprints", "our_price": "$13-$17.99"},
    {"name": "Osprey Blueprint", "category": "Blueprints", "our_price": "$2.99"},
    {"name": "Bastion Cell", "category": "Materials & Bundles", "our_price": "$2.49"},
    {"name": "Deadline Blueprint", "category": "Blueprints", "our_price": "$2.99-$4.49"},
    {"name": "Extended Barrel Blueprint", "category": "Blueprints", "our_price": "$2.99"},
    {"name": "Medium Gun Parts Blueprint", "category": "Blueprints", "our_price": "$2.99"},
    {"name": "Jupiter Blueprint", "category": "Blueprints", "our_price": "$3.99"},
    {"name": "Seeker Grenade Blueprint", "category": "Blueprints", "our_price": "$3.49"},
    {"name": "Torrente Blueprint", "category": "Blueprints", "our_price": "$3.49"},
    {"name": "Motor", "category": "Materials & Bundles", "our_price": "$1.99"},
    {"name": "Padded Stock mod", "category": "Materials & Bundles", "our_price": "$1.99"},
    {"name": "Trailblazer Blueprint", "category": "Blueprints", "our_price": "$3.49"},
    {"name": "Extended Medium Mag III Blueprint", "category": "Blueprints", "our_price": "$3.99-$4.99"},
    {"name": "Tactical Mk.3 (Revival) Blueprint", "category": "Blueprints", "our_price": "$8.49-$12"},
    {"name": "EPIC Key Bundle (20 keys)", "category": "Keys", "our_price": "$30-$50"},
]

# ============================================================================
# LOW DEMAND ITEMS (30 items)
# ============================================================================
LOW_DEMAND_ITEMS = [
    {"name": "Complex Gun Parts", "category": "Materials & Bundles", "our_price": "$1.99"},
    {"name": "Heavy Gun Parts Blueprint", "category": "Materials & Bundles", "our_price": "$1.99"},
    {"name": "Trigger Nade Blueprint", "category": "Blueprints", "our_price": "$2.99"},
    {"name": "Complex Gun Parts Blueprint", "category": "Materials & Bundles", "our_price": "$1.99"},
    {"name": "Anvil Splitter", "category": "Weapons", "our_price": "$2.49"},
    {"name": "Light Gun Parts Blueprint", "category": "Blueprints", "our_price": "$2.49"},
    {"name": "Padded Stock Blueprint", "category": "Blueprints", "our_price": "$2.49"},
    {"name": "Sentinel Firing Core", "category": "Materials & Bundles", "our_price": "$1.99"},
    {"name": "Compensator III Blueprint", "category": "Blueprints", "our_price": "$2.99"},
    {"name": "Hullcracker Blueprint", "category": "Blueprints", "our_price": "$13.99"},
    {"name": "Vulcano IV", "category": "Weapons", "our_price": "$2.49"},
    {"name": "Mushroom", "category": "Materials & Bundles", "our_price": "$0.99"},
    {"name": "Matriarch Reactor", "category": "Materials & Bundles", "our_price": "$2.49"},
    {"name": "Bombardier Cell", "category": "Materials & Bundles", "our_price": "$1.99"},
    {"name": "Venator IV", "category": "Weapons", "our_price": "$2.29"},
    {"name": "Leaper Pulse Unit", "category": "Materials & Bundles", "our_price": "$1.49"},
    {"name": "Tempest IV", "category": "Weapons", "our_price": "$2.99"},
    {"name": "100K Coins", "category": "Cosmetics & Misc", "our_price": "$5.89"},
    {"name": "Burletta Blueprint", "category": "Blueprints", "our_price": "$7.99-$9.99"},
    {"name": "Anvil IV", "category": "Weapons", "our_price": "$1.99"},
    {"name": "Apricot", "category": "Cosmetics & Misc", "our_price": "—"},
    {"name": "Blue Gate Comm Tower (RARE)", "category": "Keys", "our_price": "$1.79"},
    {"name": "Buried City Hospital (RARE)", "category": "Keys", "our_price": "$1.99"},
    {"name": "Common Keys (non-EPIC)", "category": "Keys", "our_price": "$0.99-$1.99"},
    {"name": "Dam Testing Annex (RARE)", "category": "Keys", "our_price": "$1.89"},
    {"name": "Hullcracker IV", "category": "Weapons", "our_price": "$2.49"},
    {"name": "Renegade IV", "category": "Weapons", "our_price": "$2.29"},
    {"name": "Spaceport Container (RARE)", "category": "Keys", "our_price": "$1.99"},
    {"name": "Spaceport Control Tower (RARE)", "category": "Keys", "our_price": "$1.99"},
    {"name": "Stella Montis Security (RARE)", "category": "Keys", "our_price": "$2.29"},
]

# ============================================================================
# RARE ITEMS (6 items)
# ============================================================================
RARE_ITEMS = [
    {"name": "Fireworks Box Blueprint", "category": "Blueprints", "our_price": "$5-$15"},
    {"name": "Blue Gate Cellar Key (RARE)", "category": "Keys", "our_price": "$5-$10"},
    {"name": "Blue Gate Confiscation (EPIC)", "category": "Keys", "our_price": "$15-$30"},
    {"name": "Buried City Town Hall (EPIC)", "category": "Keys", "our_price": "$15-$25"},
    {"name": "Dam Control Tower (EPIC)", "category": "Keys", "our_price": "$15-$25"},
    {"name": "Stella Montis Archives (EPIC)", "category": "Keys", "our_price": "$15-$25"},
]

# ============================================================================
# DEAD STOCK ITEMS (126 items)
# ============================================================================
DEAD_STOCK_ITEMS = [
    {"name": "Extended Light Mag II Blueprint", "category": "Blueprints", "our_price": "—"},
    {"name": "1000 Assorted Seeds", "category": "Materials & Bundles", "our_price": "—"},
    {"name": "3x Light Bulb", "category": "Materials & Bundles", "our_price": "—"},
    {"name": "3x Motor", "category": "Materials & Bundles", "our_price": "—"},
    {"name": "5x Heavy Gun Parts", "category": "Materials & Bundles", "our_price": "—"},
    {"name": "5x Light Gun Parts", "category": "Materials & Bundles", "our_price": "—"},
    {"name": "5x Medium Gun Parts", "category": "Materials & Bundles", "our_price": "—"},
    {"name": "Advanced ARC Powercell", "category": "Materials & Bundles", "our_price": "—"},
    {"name": "Advanced Electrical Comp (x5)", "category": "Materials & Bundles", "our_price": "—"},
    {"name": "Advanced Mechanical Comp (x5)", "category": "Materials & Bundles", "our_price": "—"},
    {"name": "Antiseptic", "category": "Materials & Bundles", "our_price": "—"},
    {"name": "Arc Alloy (x20)", "category": "Materials & Bundles", "our_price": "—"},
    {"name": "Arc Circuitry (x5)", "category": "Materials & Bundles", "our_price": "—"},
    {"name": "Barricade Kit Blueprint", "category": "Blueprints", "our_price": "$1.99-$4.99"},
    {"name": "Blaze Grenade Blueprint", "category": "Blueprints", "our_price": "$2.49-$5.99"},
    {"name": "Blue Gate Cellar Key", "category": "Keys", "our_price": "—"},
    {"name": "Blue Gate Confiscation Key", "category": "Keys", "our_price": "—"},
    {"name": "Blue Gate Village Key", "category": "Keys", "our_price": "—"},
    {"name": "Blue Light Stick Blueprint", "category": "Blueprints", "our_price": "—"},
    {"name": "Bobcat IV - FULLY MODDED", "category": "Weapons", "our_price": "—"},
    {"name": "Buried City Hospital Key", "category": "Keys", "our_price": "—"},
    {"name": "Buried City JKV Employee Card", "category": "Keys", "our_price": "—"},
    {"name": "Buried City Residential Key", "category": "Keys", "our_price": "—"},
    {"name": "Buried City Residential Mastery", "category": "Keys", "our_price": "—"},
    {"name": "Buried City Town Hall Key", "category": "Keys", "our_price": "—"},
    {"name": "Candle Holder", "category": "Materials & Bundles", "our_price": "—"},
    {"name": "Cat Bed", "category": "Cosmetics & Misc", "our_price": "—"},
    {"name": "Combat Mk.3 (Flanking) Blueprint", "category": "Blueprints", "our_price": "—"},
    {"name": "Cooling Coil", "category": "Materials & Bundles", "our_price": "—"},
    {"name": "Cracked Bioscanner", "category": "Materials & Bundles", "our_price": "—"},
    {"name": "Dam Staff Room Key", "category": "Keys", "our_price": "—"},
    {"name": "Dam Surveillance Key", "category": "Keys", "our_price": "—"},
    {"name": "Dam Testing Annex Key", "category": "Keys", "our_price": "—"},
    {"name": "Damaged Heat Sink", "category": "Materials & Bundles", "our_price": "—"},
    {"name": "Defibrillator (x3)", "category": "Cosmetics & Misc", "our_price": "—"},
    {"name": "Defibrillator Blueprint", "category": "Blueprints", "our_price": "—"},
    {"name": "Dog Collar", "category": "Cosmetics & Misc", "our_price": "—"},
    {"name": "Exodus Modules", "category": "Materials & Bundles", "our_price": "—"},
    {"name": "Explosives Station Lvl 1 Upgrade", "category": "Workshop Upgrades", "our_price": "—"},
    {"name": "Explosives Station Lvl 2 Upgrade", "category": "Workshop Upgrades", "our_price": "—"},
    {"name": "Explosives Station Lvl 3 Upgrade", "category": "Workshop Upgrades", "our_price": "—"},
    {"name": "Extended Shotgun Mag II Blueprint", "category": "Blueprints", "our_price": "—"},
    {"name": "Fireball Burner", "category": "Cosmetics & Misc", "our_price": "—"},
    {"name": "Fried Motherboard", "category": "Materials & Bundles", "our_price": "—"},
    {"name": "Gas Mine Blueprint", "category": "Blueprints", "our_price": "—"},
    {"name": "Gear Bench Lvl 1 Upgrade", "category": "Workshop Upgrades", "our_price": "—"},
    {"name": "Gear Bench Lvl 2 Upgrade", "category": "Workshop Upgrades", "our_price": "—"},
    {"name": "Gear Bench Lvl 3 Upgrade", "category": "Workshop Upgrades", "our_price": "—"},
    {"name": "Green Light Stick Blueprint", "category": "Blueprints", "our_price": "—"},
    {"name": "Gunsmith Lvl 1 Upgrade", "category": "Workshop Upgrades", "our_price": "—"},
    {"name": "Gunsmith Lvl 2 Upgrade", "category": "Workshop Upgrades", "our_price": "—"},
    {"name": "Gunsmith Lvl 3 Upgrade", "category": "Workshop Upgrades", "our_price": "—"},
    {"name": "Herbal Bandage (x5)", "category": "Cosmetics & Misc", "our_price": "—"},
    {"name": "Hornet Driver", "category": "Materials & Bundles", "our_price": "—"},
    {"name": "Il Toro IV - FULLY MODDED", "category": "Weapons", "our_price": "—"},
    {"name": "Industrial Battery", "category": "Materials & Bundles", "our_price": "—"},
    {"name": "Jolt Mine Blueprint", "category": "Blueprints", "our_price": "—"},
    {"name": "Laboratory Reagents", "category": "Materials & Bundles", "our_price": "—"},
    {"name": "Lemon", "category": "Cosmetics & Misc", "our_price": "—"},
    {"name": "Light Bulb", "category": "Materials & Bundles", "our_price": "—"},
    {"name": "Lure Grenade Blueprint", "category": "Blueprints", "our_price": "—"},
    {"name": "Medical Lab Lvl 1 Upgrade", "category": "Workshop Upgrades", "our_price": "—"},
    {"name": "Medical Lab Lvl 2 Upgrade", "category": "Workshop Upgrades", "our_price": "—"},
    {"name": "Medical Lab Lvl 3 Upgrade", "category": "Workshop Upgrades", "our_price": "—"},
    {"name": "Muzzle Brake II Blueprint", "category": "Blueprints", "our_price": "—"},
    {"name": "Olives", "category": "Cosmetics & Misc", "our_price": "—"},
    {"name": "Osprey IV - FULLY MODDED", "category": "Weapons", "our_price": "—"},
    {"name": "Photoelectric Cloak", "category": "Cosmetics & Misc", "our_price": "—"},
    {"name": "Pop Trigger", "category": "Cosmetics & Misc", "our_price": "—"},
    {"name": "Power Cable", "category": "Materials & Bundles", "our_price": "—"},
    {"name": "Power Rod", "category": "Materials & Bundles", "our_price": "—"},
    {"name": "Prickly Pear", "category": "Cosmetics & Misc", "our_price": "—"},
    {"name": "Pulse Mine Blueprint", "category": "Blueprints", "our_price": "—"},
    {"name": "Raider Hatch Key", "category": "Keys", "our_price": "—"},
    {"name": "Red Light Stick Blueprint", "category": "Blueprints", "our_price": "—"},
    {"name": "Refiner Lvl 1 Upgrade", "category": "Workshop Upgrades", "our_price": "—"},
    {"name": "Refiner Lvl 2 Upgrade", "category": "Workshop Upgrades", "our_price": "—"},
    {"name": "Refiner Lvl 3 Upgrade", "category": "Workshop Upgrades", "our_price": "—"},
    {"name": "Renegade IV - FULLY MODDED", "category": "Weapons", "our_price": "—"},
    {"name": "Rusted Tools", "category": "Cosmetics & Misc", "our_price": "—"},
    {"name": "Scrappy the Rooster 2-5 Upgrade", "category": "Workshop Upgrades", "our_price": "—"},
    {"name": "Spaceport Container Key", "category": "Keys", "our_price": "—"},
    {"name": "Spaceport Control Tower Key", "category": "Keys", "our_price": "—"},
    {"name": "Spaceport Trench Tower Key", "category": "Keys", "our_price": "—"},
    {"name": "Spaceport Warehouse Key", "category": "Keys", "our_price": "—"},
    {"name": "Spotter Relay", "category": "Cosmetics & Misc", "our_price": "—"},
    {"name": "Stable Stock I Blueprint", "category": "Blueprints", "our_price": "—"},
    {"name": "Stable Stock II Blueprint", "category": "Blueprints", "our_price": "—"},
    {"name": "Stella Montis Archives Key", "category": "Keys", "our_price": "—"},
    {"name": "Stella Montis Assembly Admin", "category": "Keys", "our_price": "—"},
    {"name": "Stella Montis Medical Storage", "category": "Keys", "our_price": "—"},
    {"name": "Stella Montis Security Key", "category": "Keys", "our_price": "—"},
    {"name": "Sterilized Bandage (x3)", "category": "Cosmetics & Misc", "our_price": "—"},
    {"name": "Stitcher IV - FULLY MODDED", "category": "Weapons", "our_price": "—"},
    {"name": "Synthesized Fuel", "category": "Materials & Bundles", "our_price": "—"},
    {"name": "Tactical Mk.3 (Defensive) Blueprint", "category": "Blueprints", "our_price": "—"},
    {"name": "Tempest IV - FULLY MODDED", "category": "Weapons", "our_price": "—"},
    {"name": "Tick Pod", "category": "Cosmetics & Misc", "our_price": "—"},
    {"name": "Toaster", "category": "Cosmetics & Misc", "our_price": "—"},
    {"name": "Trigger Nade (x2)", "category": "Cosmetics & Misc", "our_price": "—"},
    {"name": "Utility Station Lvl 1 Upgrade", "category": "Workshop Upgrades", "our_price": "—"},
    {"name": "Utility Station Lvl 2 Upgrade", "category": "Workshop Upgrades", "our_price": "—"},
    {"name": "Utility Station Lvl 3 Upgrade", "category": "Workshop Upgrades", "our_price": "—"},
    {"name": "Venator IV - FULLY MODDED", "category": "Weapons", "our_price": "—"},
    {"name": "Vertical Grip II Blueprint", "category": "Blueprints", "our_price": "—"},
    {"name": "Very Comfortable Pillow", "category": "Materials & Bundles", "our_price": "—"},
    {"name": "Vulcano IV - FULLY MODDED", "category": "Weapons", "our_price": "—"},
    {"name": "Wasp Driver", "category": "Cosmetics & Misc", "our_price": "—"},
    {"name": "Wolfpack x10", "category": "Cosmetics & Misc", "our_price": "—"},
    {"name": "x10 Candleberries", "category": "Materials & Bundles", "our_price": "—"},
    {"name": "x10 Simple Gun Parts", "category": "Materials & Bundles", "our_price": "—"},
    {"name": "x15 Steel Spring", "category": "Materials & Bundles", "our_price": "—"},
    {"name": "x3 Exodus Modules", "category": "Materials & Bundles", "our_price": "—"},
    {"name": "x3 Magnetic Accelerator", "category": "Materials & Bundles", "our_price": "—"},
    {"name": "x5 Processor", "category": "Materials & Bundles", "our_price": "—"},
    {"name": "x5 Sensors", "category": "Materials & Bundles", "our_price": "—"},
    {"name": "x5 Zipline", "category": "Cosmetics & Misc", "our_price": "—"},
    {"name": "x500 Assorted Seeds", "category": "Materials & Bundles", "our_price": "—"},
    {"name": "Yellow Light Stick Blueprint", "category": "Blueprints", "our_price": "—"},
    {"name": "Anvil IV + Silencer II", "category": "Weapons", "our_price": "$2.69"},
    {"name": "Aphelion IV", "category": "Weapons", "our_price": "—"},
    {"name": "Burletta IV", "category": "Weapons", "our_price": "—"},
    {"name": "Il Toro IV", "category": "Weapons", "our_price": "—"},
    {"name": "Osprey IV", "category": "Weapons", "our_price": "—"},
    {"name": "Stitcher IV", "category": "Weapons", "our_price": "$0.99"},
    {"name": "Torrente IV", "category": "Weapons", "our_price": "—"},
]


def build_items_database():
    """
    Build the complete items database with parsed prices.
    Returns a list of item dictionaries.
    """
    all_items = []
    
    # Process each demand category
    demand_categories = [
        ("Top Seller", TOP_SELLER_ITEMS),
        ("Mid Demand", MID_DEMAND_ITEMS),
        ("Low Demand", LOW_DEMAND_ITEMS),
        ("Rare", RARE_ITEMS),
        ("Dead Stock", DEAD_STOCK_ITEMS),
    ]
    
    for demand, items in demand_categories:
        for item in items:
            price_low, price_high = parse_price(item["our_price"])
            all_items.append({
                "name": item["name"],
                "category": item["category"],
                "demand": demand,
                "our_price_low": price_low,
                "our_price_high": price_high,
                "our_price_str": item["our_price"],
            })
    
    return all_items


def get_items_by_demand(demand_level=None):
    """
    Get items filtered by demand level.
    If demand_level is None, returns all items.
    """
    all_items = build_items_database()
    
    if demand_level is None:
        return all_items
    
    return [item for item in all_items if item["demand"] == demand_level]


def get_searchable_items():
    """
    Get items that have prices set (excludes items with no price).
    These are the items worth searching for competitors.
    """
    all_items = build_items_database()
    return [item for item in all_items if item["our_price_low"] is not None]


# Quick stats
if __name__ == "__main__":
    all_items = build_items_database()
    searchable = get_searchable_items()
    
    print(f"Total items in database: {len(all_items)}")
    print(f"Items with prices (searchable): {len(searchable)}")
    print()
    
    # Count by demand
    from collections import Counter
    demand_counts = Counter(item["demand"] for item in all_items)
    for demand, count in demand_counts.items():
        print(f"  {demand}: {count} items")

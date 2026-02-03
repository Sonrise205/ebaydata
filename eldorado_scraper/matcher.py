# matcher.py - Smart Fuzzy Matching System for Item Names
# Handles variations like: "Angled Grip II" vs "angled grip 2" vs "ANGLED GRIP II BLUEPRINT"

import re
from rapidfuzz import fuzz, process

# Roman numeral to Arabic conversion
ROMAN_TO_ARABIC = {
    'i': '1', 'ii': '2', 'iii': '3', 'iv': '4', 'v': '5',
    'vi': '6', 'vii': '7', 'viii': '8', 'ix': '9', 'x': '10',
    'xi': '11', 'xii': '12', 'xiii': '13', 'xiv': '14', 'xv': '15',
}

# Common filler words to remove from listings (marketing fluff)
FILLER_WORDS = {
    'fast', 'quick', 'instant', 'delivery', 'safe', 'best', 'price',
    'cheap', 'discount', 'sale', 'hot', 'new', 'stock', 'available',
    '24/7', 'online', 'trusted', 'verified', 'seller', 'store', 'shop',
    'buy', 'get', 'now', 'today', 'limited', 'offer', 'deal', 'bargain',
    'pro', 'premium', 'vip', 'exclusive', 'rare', 'legendary', 'epic',
}

# Category keywords that help verify matches
CATEGORY_KEYWORDS = {
    'Blueprints': ['blueprint', 'bp', 'schematic', 'plan'],
    'Weapons': ['weapon', 'gun', 'rifle', 'pistol', 'smg', 'shotgun'],
    'Materials & Bundles': ['material', 'bundle', 'parts', 'component', 'x3', 'x5', 'x10', 'x15', 'x20'],
    'Keys': ['key', 'keycard', 'card', 'access'],
    'Cosmetics & Misc': ['cosmetic', 'skin', 'spray', 'backpack', 'coins'],
    'Workshop Upgrades': ['upgrade', 'lvl', 'level', 'station', 'bench'],
}


def normalize_text(text: str) -> str:
    """
    Normalize text for comparison:
    1. Lowercase
    2. Remove emojis and special characters
    3. Convert Roman numerals to Arabic
    4. Remove extra whitespace
    """
    if not text:
        return ""
    
    # Lowercase
    text = text.lower()
    
    # Remove emojis and special unicode characters
    # Keep only alphanumeric, spaces, and basic punctuation
    text = re.sub(r'[^\w\s\'-]', ' ', text)
    
    # Convert Roman numerals to Arabic (word boundaries)
    words = text.split()
    normalized_words = []
    for word in words:
        # Check if word is a Roman numeral
        if word in ROMAN_TO_ARABIC:
            normalized_words.append(ROMAN_TO_ARABIC[word])
        # Also handle 'll' as 'II' (common typo)
        elif word == 'll':
            normalized_words.append('2')
        else:
            normalized_words.append(word)
    
    text = ' '.join(normalized_words)
    
    # Normalize multiple spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def remove_filler_words(text: str) -> str:
    """Remove common filler/marketing words from text."""
    words = text.split()
    filtered = [w for w in words if w not in FILLER_WORDS]
    return ' '.join(filtered)


def extract_core_keywords(item_name: str) -> set:
    """
    Extract core keywords from an item name.
    These are the essential words that identify the item.
    """
    normalized = normalize_text(item_name)
    cleaned = remove_filler_words(normalized)
    
    # Split into words and remove very short words (except numbers)
    words = cleaned.split()
    keywords = set()
    
    for word in words:
        # Keep numbers and words with 2+ characters
        if word.isdigit() or len(word) >= 2:
            keywords.add(word)
    
    return keywords


def calculate_match_score(db_item_name: str, listing_title: str, db_category: str = None) -> dict:
    """
    Calculate how well a listing title matches a database item.
    
    Returns a dict with:
        - score: 0-100 match score
        - method: which matching method gave the best score
        - details: additional match details
    """
    # Normalize both strings
    norm_db = normalize_text(db_item_name)
    norm_listing = normalize_text(listing_title)
    
    # Remove filler words for cleaner comparison
    clean_db = remove_filler_words(norm_db)
    clean_listing = remove_filler_words(norm_listing)
    
    # Method 1: Direct fuzzy ratio
    fuzzy_ratio = fuzz.ratio(clean_db, clean_listing)
    
    # Method 2: Partial ratio (good for when one is substring of other)
    partial_ratio = fuzz.partial_ratio(clean_db, clean_listing)
    
    # Method 3: Token set ratio (ignores word order)
    token_set_ratio = fuzz.token_set_ratio(clean_db, clean_listing)
    
    # Method 4: Token sort ratio (sorts words then compares)
    token_sort_ratio = fuzz.token_sort_ratio(clean_db, clean_listing)
    
    # Method 5: Keyword presence check
    db_keywords = extract_core_keywords(db_item_name)
    listing_keywords = extract_core_keywords(listing_title)
    
    # Calculate keyword overlap
    if db_keywords:
        keyword_overlap = len(db_keywords & listing_keywords) / len(db_keywords)
        keyword_score = keyword_overlap * 100
    else:
        keyword_score = 0
    
    # Combine scores (weighted average)
    # Token set ratio is usually best for our use case
    combined_score = (
        fuzzy_ratio * 0.15 +
        partial_ratio * 0.15 +
        token_set_ratio * 0.35 +
        token_sort_ratio * 0.20 +
        keyword_score * 0.15
    )
    
    # Bonus: If category keyword is present in listing, boost score
    category_bonus = 0
    if db_category and db_category in CATEGORY_KEYWORDS:
        cat_keywords = CATEGORY_KEYWORDS[db_category]
        for cat_kw in cat_keywords:
            if cat_kw in norm_listing:
                category_bonus = 5
                break
    
    final_score = min(100, combined_score + category_bonus)
    
    # Determine which method contributed most
    scores = {
        'fuzzy_ratio': fuzzy_ratio,
        'partial_ratio': partial_ratio,
        'token_set_ratio': token_set_ratio,
        'token_sort_ratio': token_sort_ratio,
        'keyword_score': keyword_score,
    }
    best_method = max(scores, key=scores.get)
    
    return {
        'score': final_score,
        'method': best_method,
        'details': {
            'normalized_db': norm_db,
            'normalized_listing': norm_listing,
            'db_keywords': db_keywords,
            'listing_keywords': listing_keywords,
            'scores': scores,
            'category_bonus': category_bonus,
        }
    }


def is_match(db_item_name: str, listing_title: str, threshold: int = 75, db_category: str = None) -> bool:
    """
    Determine if a listing title matches a database item.
    
    Args:
        db_item_name: Item name from our database
        listing_title: Title from Eldorado listing
        threshold: Minimum score to consider a match (0-100)
        db_category: Category of the item (optional, for bonus)
    
    Returns:
        True if the listing matches the database item
    """
    result = calculate_match_score(db_item_name, listing_title, db_category)
    return result['score'] >= threshold


def find_best_matches(db_item_name: str, listings: list, threshold: int = 75, db_category: str = None) -> list:
    """
    Find all listings that match a database item above the threshold.
    
    Args:
        db_item_name: Item name from our database
        listings: List of listing dicts with 'title' key
        threshold: Minimum score to consider a match
        db_category: Category of the item
    
    Returns:
        List of (listing, score) tuples for matches above threshold
    """
    matches = []
    
    for listing in listings:
        title = listing.get('title', listing.get('offer_title', ''))
        result = calculate_match_score(db_item_name, title, db_category)
        
        if result['score'] >= threshold:
            matches.append((listing, result['score']))
    
    # Sort by score descending
    matches.sort(key=lambda x: x[1], reverse=True)
    
    return matches


# ============================================================================
# Test the matcher
# ============================================================================
if __name__ == "__main__":
    # Test cases
    test_cases = [
        # (db_item, listing_title, expected_match)
        ("Angled Grip II Blueprint", "Angled Grip II | 2 Blueprint", True),
        ("Angled Grip II Blueprint", "angled grip 2 blueprint", True),
        ("Angled Grip II Blueprint", "ANGLED GRIP II BLUEPRINT", True),
        ("Angled Grip II Blueprint", "⭐ANGLED GRIP II BLUEPRINT⭐", True),
        ("Angled Grip II Blueprint", "Angled Grip II Blueprint⭐ Safe & Fast ✨", True),
        ("Angled Grip II Blueprint", "Angle Grip II Blueprint", True),  # Typo
        ("Angled Grip II Blueprint", "angled grıp II", True),  # Turkish i
        ("Angled Grip II Blueprint", "Bobcat Blueprint", False),  # Different item
        ("Bobcat Blueprint", "Bobcat Blueprint Fast Delivery", True),
        ("Bobcat Blueprint", "⭐ BOBCAT BLUEPRINT ⭐ BEST PRICE", True),
        ("Looting Mk.3 (Survivor) Blueprint", "LOOTING MK. 3 (SURVIVOR) BLUEPRINT", True),
        ("500K Coins", "500K Coins - Arc Raiders", True),
        ("Wolfpack", "Wolfpack x10", False),  # Different - one is bundle
    ]
    
    print("=" * 70)
    print("MATCHER TEST RESULTS")
    print("=" * 70)
    
    for db_item, listing, expected in test_cases:
        result = calculate_match_score(db_item, listing)
        is_match_result = result['score'] >= 75
        status = "✓" if is_match_result == expected else "✗"
        
        print(f"\n{status} DB: '{db_item}'")
        print(f"   Listing: '{listing}'")
        print(f"   Score: {result['score']:.1f} | Method: {result['method']}")
        print(f"   Match: {is_match_result} (expected: {expected})")

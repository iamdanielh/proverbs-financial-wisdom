#!/usr/bin/env python3
"""
Flipping Research Engine
Multi-marketplace deal finder for arbitrage opportunities.
Analyzes listings across platforms, calculates potential margins,
and alerts on profitable flips.

Built for Dan: analytical, efficiency-focused, no-fluff automation.
"""

import json
import sys
import re
from datetime import datetime, timedelta
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from typing import Dict, List, Optional


class MarketplaceScraper:
    """Base class for marketplace scrapers."""
    
    def __init__(self, name: str):
        self.name = name
        
    def fetch(self, category: str, limit: int = 50) -> List[Dict]:
        """Override in subclasses. Returns list of listings."""
        raise NotImplementedError


class MockMarketplace(MarketplaceScraper):
    """Mock scraper for development/demo.
    In production, inherit and implement real scrapers for:
    - eBay (completed/active listings)
    - Facebook Marketplace
    - Craigslist
    - OfferUp
    - StockX/GOAT (for sneakers)
    - Swappa (for electronics)
    """
    
    SAMPLE_CATEGORIES = {
        "laptops": [
            {"title": "MacBook Pro 16 M3 Pro 18GB 512GB", "price": 1899, "original": 2499, "condition": "like_new", "source": "demo_fbm"},
            {"title": "Dell XPS 15 i7 32GB RAM RTX 4060", "price": 850, "original": 1899, "condition": "good", "source": "demo_cg"},
            {"title": "ThinkPad X1 Carbon Gen 11", "price": 650, "original": 1800, "condition": "good", "source": "demo_ebay"},
        ],
        "gaming": [
            {"title": "PS5 Disc Edition Bundle", "price": 350, "original": 559, "condition": "like_new", "source": "demo_fbm"},
            {"title": "Nintendo Switch OLED", "price": 180, "original": 349, "condition": "good", "source": "demo_ebay"},
            {"title": "Steam Deck OLED 512GB", "price": 450, "original": 549, "condition": "like_new", "source": "demo_cl"},
        ],
        "sneakers": [
            {"title": "Jordan 4 Retro Thunder (2023) Size 10", "price": 280, "original": 380, "condition": "new", "source": "demo_fbm"},
            {"title": "Nike Dunk Low Panda Size 9", "price": 85, "original": 115, "condition": "new", "source": "demo_ebay"},
        ],
        "electronics": [
            {"title": "iPhone 15 Pro 256GB Unlocked", "price": 750, "original": 1199, "condition": "like_new", "source": "demo_swappa"},
            {"title": "Samsung Galaxy S24 Ultra 512GB", "price": 680, "original": 1419, "condition": "good", "source": "demo_fbm"},
            {"title": "iPad Pro 12.9 M2 256GB", "price": 720, "original": 1199, "condition": "like_new", "source": "demo_cg"},
        ]
    }
    
    def fetch(self, category: str, limit: int = 50) -> List[Dict]:
        """Get sample listings for category."""
        listings = self.SAMPLE_CATEGORIES.get(category, [])
        # Add realistic metadata
        for item in listings:
            item["fetched_at"] = datetime.now().isoformat()
            item["marketplace"] = self.name
        return listings[:limit]


class PricingEngine:
    """Calculate fair market value and profit margins."""
    
    # Market value multipliers by condition
    CONDITION_MULTIPLIERS = {
        "new": 1.0,
        "like_new": 0.85,
        "excellent": 0.80,
        "good": 0.70,
        "fair": 0.55,
        "poor": 0.35
    }
    
    # Platform fee estimates
    PLATFORM_FEES = {
        "ebay": 0.135,      # 12.9% + $0.30
        "stockx": 0.10,     # Seller fee
        "goat": 0.125,      # Commission + cash out
        "facebook": 0.05,   # Approx for shipping/tax handling
        "craigslist": 0.0,  # Cash only
        "offerup": 0.125,   # Shipping fee
        "swappa": 0.00,     # Buyer pays
    }
    
    # Shipping estimate (conservative)
    SHIPPING_ESTIMATE = 15.0
    
    def estimate_fmv(self, item: Dict) -> float:
        """Estimate fair market value based on original price and condition."""
        original = item.get("original", item.get("price", 0) * 1.5)
        condition = item.get("condition", "good")
        multiplier = self.CONDITION_MULTIPLIERS.get(condition, 0.70)
        return original * multiplier
    
    def calculate_flip_potential(self, item: Dict, resale_platform: str = "ebay") -> Dict:
        """Calculate profit potential for a flip."""
        price = item.get("price", 0)
        fmv = self.estimate_fmv(item)
        
        # Conservative resale price (90% of FMV to move quickly)
        resale_price = fmv * 0.90
        
        # Fees
        fee_rate = self.PLATFORM_FEES.get(resale_platform.lower(), 0.13)
        platform_fees = resale_price * fee_rate
        
        # Net proceeds
        net_proceeds = resale_price - platform_fees - self.SHIPPING_ESTIMATE
        
        # Profit
        gross_profit = net_proceeds - price
        roi = (gross_profit / price * 100) if price > 0 else 0
        margin = (gross_profit / resale_price * 100) if resale_price > 0 else 0
        
        return {
            "purchase_price": price,
            "estimated_fmv": round(fmv, 2),
            "resale_price": round(resale_price, 2),
            "platform_fees": round(platform_fees, 2),
            "shipping": self.SHIPPING_ESTIMATE,
            "net_proceeds": round(net_proceeds, 2),
            "gross_profit": round(gross_profit, 2),
            "roi_percent": round(roi, 1),
            "margin_percent": round(margin, 1),
            "platform": resale_platform,
            "is_viable": gross_profit > 50 and roi > 15
        }


class DealAnalyzer:
    """Analyze deals and generate alerts."""
    
    def __init__(self, config_path: str = "flip_config.json"):
        self.config = self.load_config(config_path)
        self.engine = PricingEngine()
        self.scrapers = self.setup_scrapers()
        
    def load_config(self, path: str) -> Dict:
        """Load or create configuration."""
        defaults = {
            "categories": ["laptops", "gaming", "electronics", "sneakers"],
            "min_profit": 50,
            "min_roi": 15,
            "max_investment": 2000,
            "preferred_platforms": ["ebay", "stockx", "facebook"],
            "data_dir": "./data"
        }
        try:
            with open(path) as f:
                cfg = json.load(f)
                defaults.update(cfg)
                return defaults
        except FileNotFoundError:
            with open(path, 'w') as f:
                json.dump(defaults, f, indent=2)
            print(f"Created config: {path}")
            return defaults
    
    def setup_scrapers(self) -> List[MarketplaceScraper]:
        """Initialize marketplace scrapers."""
        scrapers = []
        # In production, add real scrapers here
        scrapers.append(MockMarketplace("DemoMarket"))
        return scrapers
    
    def fetch_all_listings(self) -> List[Dict]:
        """Gather listings from all sources."""
        all_listings = []
        for scraper in self.scrapers:
            for category in self.config["categories"]:
                try:
                    listings = scraper.fetch(category)
                    for item in listings:
                        item["category"] = category
                    all_listings.extend(listings)
                except Exception as e:
                    print(f"Error fetching {category} from {scraper.name}: {e}")
        return all_listings
    
    def analyze_deals(self, listings: List[Dict]) -> List[Dict]:
        """Analyze listings for flip opportunities."""
        viable_deals = []
        
        for item in listings:
            # Check investment limit
            price = item.get("price", 0)
            if price > self.config["max_investment"]:
                continue
            
            # Calculate profitability for each platform
            best_platform = None
            best_profit = 0
            best_analysis = None
            
            for platform in self.config["preferred_platforms"]:
                analysis = self.engine.calculate_flip_potential(item, platform)
                
                if analysis["is_viable"] and analysis["gross_profit"] > best_profit:
                    best_profit = analysis["gross_profit"]
                    best_platform = platform
                    best_analysis = analysis
            
            if best_analysis:
                deal = {
                    **item,
                    "analysis": best_analysis,
                    "resale_platform": best_platform,
                    "score": self.score_deal(best_analysis)
                }
                viable_deals.append(deal)
        
        # Sort by score (highest first)
        viable_deals.sort(key=lambda x: x["score"], reverse=True)
        return viable_deals
    
    def score_deal(self, analysis: Dict) -> float:
        """Score a deal based on multiple factors."""
        profit_score = min(analysis["gross_profit"] / 100, 10)  # Cap at 10
        roi_score = min(analysis["roi_percent"] / 20, 5)       # Cap at 5
        
        # Fast flip bonus (high margin = quick sale)
        margin_score = analysis["margin_percent"] / 10
        
        # Total score (weighted)
        return profit_score * 0.5 + roi_score * 0.3 + margin_score * 0.2
    
    def generate_report(self, deals: List[Dict]):
        """Print and save deal analysis."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        print(f"\n{'='*75}")
        print(f"FLIPPING RESEARCH ENGINE | {timestamp}")
        print(f"{'='*75}\n")
        
        viable = [d for d in deals if d["analysis"]["is_viable"]]
        total = len(deals)
        
        print(f"Scanned {total} listings | Found {len(viable)} viable deals\n")
        
        if not viable:
            print("No viable flip opportunities found.")
            return
        
        # Print table header
        print(f"{'DEAL':<45} {'PRICE':>10} {'PROFIT':>10} {'ROI':>7} {'SCORE':>6}")
        print(f"{'-'*75}")
        
        # Print top deals
        for deal in viable[:10]:
            title = deal.get("title", "Unknown")[:44]
            price = deal["analysis"]["purchase_price"]
            profit = deal["analysis"]["gross_profit"]
            roi = deal["analysis"]["roi_percent"]
            score = round(deal["score"], 1)
            
            print(f"{title:<45} ${price:>9} ${profit:>9} {roi:>6}% {score:>6}")
        
        print(f"\n{'-'*75}")
        print(f"\nTop opportunity:")
        if viable:
            best = viable[0]
            a = best["analysis"]
            print(f"  📱 {best.get('title')}")
            print(f"     Category: {best.get('category').upper()}")
            print(f"     Source: {best.get('source', 'Unknown')}")
            print(f"     Condition: {best.get('condition', 'unknown')}")
            print(f"  🛒 Buy: ${a['purchase_price']} → 💰 Resell: ${a['resale_price']} on {a['platform']}")
            print(f"  📊 Profit: ${a['gross_profit']} | ROI: {a['roi_percent']}% | Margin: {a['margin_percent']}%")
        
        # Save to file
        self.save_deals(viable)
    
    def save_deals(self, deals: List[Dict]):
        """Save deals to JSON for tracking."""
        data_dir = Path(self.config.get("data_dir", "./data"))
        data_dir.mkdir(exist_ok=True)
        
        deals_file = data_dir / "flip_opportunities.json"
        
        # Load existing
        all_deals = []
        if deals_file.exists():
            try:
                with open(deals_file) as f:
                    all_deals = json.load(f)
            except:
                pass
        
        # Add new deals with timestamp
        run_data = {
            "timestamp": datetime.now().isoformat(),
            "deals_found": len(deals),
            "deals": deals
        }
        all_deals.append(run_data)
        
        # Keep last 50 runs
        all_deals = all_deals[-50:]
        
        with open(deals_file, 'w') as f:
            json.dump(all_deals, f, indent=2, default=str)
        
        print(f"\n💾 Saved to: {deals_file}")
    
    def run(self):
        """Main execution."""
        print("🔍 Fetching listings from marketplaces...")
        listings = self.fetch_all_listings()
        
        print(f"📊 Analyzing {len(listings)} listings...")
        deals = self.analyze_deals(listings)
        
        self.generate_report(deals)


def main():
    analyzer = DealAnalyzer()
    try:
        analyzer.run()
    except KeyboardInterrupt:
        print("\nAnalysis stopped.")
        sys.exit(0)


if __name__ == "__main__":
    main()
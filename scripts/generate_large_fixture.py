#!/usr/bin/env python3
"""
Generate large CSV fixture for load testing.

Usage:
    python scripts/generate_large_fixture.py > tests/fixtures/bulk_deals_large.csv
"""

import csv
import sys
from datetime import datetime, timedelta
import random

# Sample symbols
SYMBOLS = ["RELIANCE", "TCS", "HDFCBANK", "INFY", "ICICIBANK", "HINDUNILVR", "SBIN", "BHARTIARTL", "ITC", "KOTAKBANK"]

# Sample client names
CLIENTS = [
    "ABC CAPITAL SERVICES LTD.",
    "XYZ SECURITIES PVT. LTD.",
    "DEF INVESTMENTS",
    "GHI TRADING COMPANY",
    "JKL FINANCIAL SERVICES",
    "MNO CAPITAL",
    "PQR SECURITIES",
    "STU INVESTMENTS",
    "VWX TRADING",
    "YZA FINANCIAL"
]

def generate_deal(date, symbol, client, deal_type, quantity, price):
    """Generate a single deal row."""
    return {
        "Date": date.strftime("%d-%b-%Y"),
        "Symbol": symbol,
        "Client Name": client,
        "Buy / Sell": deal_type,
        "Quantity Traded": str(quantity),
        "Trade Price / Wght. Avg. Price": f"{price:.2f}"
    }

def main():
    """Generate large CSV fixture."""
    num_rows = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    
    writer = csv.DictWriter(
        sys.stdout,
        fieldnames=["Date", "Symbol", "Client Name", "Buy / Sell", "Quantity Traded", "Trade Price / Wght. Avg. Price"]
    )
    
    writer.writeheader()
    
    start_date = datetime(2024, 1, 1)
    
    for i in range(num_rows):
        date = start_date + timedelta(days=random.randint(0, 365))
        symbol = random.choice(SYMBOLS)
        client = random.choice(CLIENTS)
        deal_type = random.choice(["BUY", "SELL"])
        quantity = random.randint(10000, 1000000)
        price = random.uniform(100.0, 5000.0)
        
        writer.writerow(generate_deal(date, symbol, client, deal_type, quantity, price))

if __name__ == "__main__":
    main()



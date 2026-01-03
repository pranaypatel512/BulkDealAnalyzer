"""
CSV Parser for Bulk Deals Data

This module handles parsing of CSV files containing bulk deals data.
"""

from typing import List, Optional
import csv
from datetime import datetime
from pathlib import Path
import io

from pydantic import BaseModel, Field, validator


class BulkDeal(BaseModel):
    """Model for a single bulk deal record."""
    
    date: datetime
    symbol: str = Field(..., min_length=1, max_length=20)
    client_name: str = Field(..., min_length=1)
    deal_type: str = Field(..., pattern="^(BUY|SELL)$")
    quantity: int = Field(..., gt=0)
    price: float = Field(..., gt=0)
    
    @validator('date', pre=True)
    def parse_date(cls, v):
        if isinstance(v, str):
            # Parse NSE date format: "01-Jan-2024"
            return datetime.strptime(v, "%d-%b-%Y")
        return v
    
    @validator('deal_type')
    def validate_deal_type(cls, v):
        v = v.upper().strip()
        if v not in ['BUY', 'SELL']:
            raise ValueError(f"Deal type must be BUY or SELL, got {v}")
        return v


class ParseResult(BaseModel):
    """Result of CSV parsing operation."""
    
    deals: List[BulkDeal]
    errors: List[str] = []
    total_rows: int = 0
    valid_rows: int = 0
    invalid_rows: int = 0


def parse_csv_file(file_path: Path) -> ParseResult:
    """
    Parse bulk deals CSV file.
    
    Args:
        file_path: Path to CSV file
        
    Returns:
        ParseResult with parsed deals and any errors
    """
    deals = []
    errors = []
    total_rows = 0
    valid_rows = 0
    invalid_rows = 0
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is row 1)
                total_rows += 1
                
                try:
                    # Parse and validate row
                    deal = BulkDeal(
                        date=row['Date'],
                        symbol=row['Symbol'].strip(),
                        client_name=row['Client Name'].strip(),
                        deal_type=row['Buy / Sell'].strip(),
                        quantity=int(row['Quantity Traded']),
                        price=float(row['Trade Price / Wght. Avg. Price'])
                    )
                    deals.append(deal)
                    valid_rows += 1
                    
                except (ValueError, KeyError, TypeError) as e:
                    invalid_rows += 1
                    errors.append(f"Row {row_num}: {str(e)}")
                    continue
                    
    except FileNotFoundError:
        errors.append(f"File not found: {file_path}")
    except Exception as e:
        errors.append(f"Error reading file: {str(e)}")
    
    return ParseResult(
        deals=deals,
        errors=errors,
        total_rows=total_rows,
        valid_rows=valid_rows,
        invalid_rows=invalid_rows
    )


def parse_csv_content(content: str) -> ParseResult:
    """
    Parse bulk deals CSV content from string.
    
    Args:
        content: CSV file content as string
        
    Returns:
        ParseResult with parsed deals and any errors
    """
    deals = []
    errors = []
    total_rows = 0
    valid_rows = 0
    invalid_rows = 0
    
    try:
        reader = csv.DictReader(io.StringIO(content))
        
        for row_num, row in enumerate(reader, start=2):
            total_rows += 1
            
            try:
                deal = BulkDeal(
                    date=row['Date'],
                    symbol=row['Symbol'].strip(),
                    client_name=row['Client Name'].strip(),
                    deal_type=row['Buy / Sell'].strip(),
                    quantity=int(row['Quantity Traded']),
                    price=float(row['Trade Price / Wght. Avg. Price'])
                )
                deals.append(deal)
                valid_rows += 1
                
            except (ValueError, KeyError, TypeError) as e:
                invalid_rows += 1
                errors.append(f"Row {row_num}: {str(e)}")
                continue
                
    except Exception as e:
        errors.append(f"Error parsing CSV content: {str(e)}")
    
    return ParseResult(
        deals=deals,
        errors=errors,
        total_rows=total_rows,
        valid_rows=valid_rows,
        invalid_rows=invalid_rows
    )


def filter_buy_deals(deals: List[BulkDeal]) -> List[BulkDeal]:
    """Filter only BUY deals."""
    return [deal for deal in deals if deal.deal_type == 'BUY']


def sort_by_quantity(deals: List[BulkDeal], descending: bool = True) -> List[BulkDeal]:
    """Sort deals by quantity."""
    return sorted(deals, key=lambda x: x.quantity, reverse=descending)



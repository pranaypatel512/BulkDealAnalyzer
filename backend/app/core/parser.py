"""
CSV Parser for Bulk Deals Data

This module handles parsing of CSV files containing NSE bulk deals data.
Supports the actual NSE CSV format with various header formats.
"""

import csv
import io
from datetime import datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, field_validator


class BulkDeal(BaseModel):
    """Model for a single bulk deal record."""

    date: datetime
    symbol: str = Field(..., min_length=1, max_length=20)
    security_name: str | None = None
    client_name: str = Field(..., min_length=1)
    deal_type: str = Field(..., pattern="^(BUY|SELL)$")
    quantity: int = Field(..., gt=0)
    price: float = Field(..., gt=0)
    remarks: str | None = None

    @field_validator('date', mode='before')
    @classmethod
    def parse_date(cls, v):
        if isinstance(v, str):
            # Parse NSE date format: "02-Jan-2026"
            v = v.strip().strip('"')
            return datetime.strptime(v, "%d-%b-%Y")
        return v

    @field_validator('deal_type', mode='before')
    @classmethod
    def validate_deal_type(cls, v):
        if isinstance(v, str):
            v = v.upper().strip().strip('"')
        if v not in ['BUY', 'SELL']:
            raise ValueError(f"Deal type must be BUY or SELL, got {v}")
        return v

    @field_validator('quantity', mode='before')
    @classmethod
    def parse_quantity(cls, v):
        if isinstance(v, str):
            # Remove commas and quotes from quantity: "67,181" -> 67181
            v = v.strip().strip('"').replace(',', '')
            return int(v)
        return v

    @field_validator('price', mode='before')
    @classmethod
    def parse_price(cls, v):
        if isinstance(v, str):
            # Remove commas and quotes from price: "1,208.26" -> 1208.26
            v = v.strip().strip('"').replace(',', '')
            return float(v)
        return v

    @field_validator('symbol', 'client_name', mode='before')
    @classmethod
    def clean_string(cls, v):
        if isinstance(v, str):
            return v.strip().strip('"')
        return v


class ParseResult(BaseModel):
    """Result of CSV parsing operation."""

    deals: list[BulkDeal]
    errors: list[str] = []
    total_rows: int = 0
    valid_rows: int = 0
    invalid_rows: int = 0


def normalize_header(header: str) -> str:
    """
    Normalize CSV header to standard format.

    Handles NSE format with trailing newlines and various naming conventions.
    """
    # Remove whitespace, newlines, and quotes
    header = header.strip().strip('"').replace('\n', '').replace('\r', '')
    # Normalize to lowercase for comparison
    header_lower = header.lower()

    # Map various header formats to standard keys
    header_mapping = {
        'date': 'date',
        'symbol': 'symbol',
        'security name': 'security_name',
        'client name': 'client_name',
        'buy/sell': 'deal_type',
        'buy / sell': 'deal_type',
        'quantity traded': 'quantity',
        'trade price/ weighted. avg. price': 'price',
        'trade price / wght. avg. price': 'price',
        'remarks': 'remarks',
    }

    return header_mapping.get(header_lower, header_lower)


def normalize_row(row: dict[str, Any]) -> dict[str, Any]:
    """Normalize a CSV row by cleaning header keys."""
    normalized = {}
    for key, value in row.items():
        norm_key = normalize_header(key)
        # Clean the value
        if isinstance(value, str):
            value = value.strip().strip('"')
        normalized[norm_key] = value
    return normalized


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
        # Try different encodings
        encodings = ['utf-8-sig', 'utf-8', 'latin-1', 'cp1252']
        content = None

        for encoding in encodings:
            try:
                with open(file_path, encoding=encoding) as f:
                    content = f.read()
                break
            except UnicodeDecodeError:
                continue

        if content is None:
            errors.append("Could not decode file with any supported encoding")
            return ParseResult(deals=[], errors=errors, total_rows=0, valid_rows=0, invalid_rows=0)

        reader = csv.DictReader(io.StringIO(content))

        for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is row 1)
            total_rows += 1

            try:
                # Normalize the row headers
                norm_row = normalize_row(row)

                # Parse and validate row
                deal = BulkDeal(
                    date=norm_row.get('date', ''),
                    symbol=norm_row.get('symbol', ''),
                    security_name=norm_row.get('security_name'),
                    client_name=norm_row.get('client_name', ''),
                    deal_type=norm_row.get('deal_type', ''),
                    quantity=norm_row.get('quantity', '0'),
                    price=norm_row.get('price', '0'),
                    remarks=norm_row.get('remarks'),
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
                # Normalize the row headers
                norm_row = normalize_row(row)

                deal = BulkDeal(
                    date=norm_row.get('date', ''),
                    symbol=norm_row.get('symbol', ''),
                    security_name=norm_row.get('security_name'),
                    client_name=norm_row.get('client_name', ''),
                    deal_type=norm_row.get('deal_type', ''),
                    quantity=norm_row.get('quantity', '0'),
                    price=norm_row.get('price', '0'),
                    remarks=norm_row.get('remarks'),
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


def filter_buy_deals(deals: list[BulkDeal]) -> list[BulkDeal]:
    """Filter only BUY deals."""
    return [deal for deal in deals if deal.deal_type == 'BUY']


def filter_sell_deals(deals: list[BulkDeal]) -> list[BulkDeal]:
    """Filter only SELL deals."""
    return [deal for deal in deals if deal.deal_type == 'SELL']


def sort_by_quantity(deals: list[BulkDeal], descending: bool = True) -> list[BulkDeal]:
    """Sort deals by quantity."""
    return sorted(deals, key=lambda x: x.quantity, reverse=descending)


def sort_by_price(deals: list[BulkDeal], descending: bool = True) -> list[BulkDeal]:
    """Sort deals by price."""
    return sorted(deals, key=lambda x: x.price, reverse=descending)


def filter_by_symbol(deals: list[BulkDeal], symbol: str) -> list[BulkDeal]:
    """Filter deals by symbol."""
    return [deal for deal in deals if deal.symbol.upper() == symbol.upper()]

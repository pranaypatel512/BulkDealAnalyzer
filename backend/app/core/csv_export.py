from __future__ import annotations

import csv
import io
from typing import Any

CSV_HEADER = [
    "Date",
    "Symbol",
    "Security Name",
    "Client Name",
    "Type",
    "Qty",
    "Price",
    "Remarks",
]


def deals_to_csv(deals: list[dict[str, Any]]) -> str:
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(CSV_HEADER)

    for d in deals:
        writer.writerow(
            [
                (d.get("date") or ""),
                (d.get("symbol") or ""),
                (d.get("security_name") or ""),
                (d.get("client_name") or ""),
                (d.get("deal_type") or ""),
                (d.get("quantity") or 0),
                (d.get("price") or 0),
                (d.get("remarks") or ""),
            ],
        )

    return buf.getvalue()


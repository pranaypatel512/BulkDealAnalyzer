"""Tests for NSEFetcher JSON->CSV normalization across response shapes."""

from app.services.nse_fetcher import NSEFetcher


def _csv_from(deals: list[dict]) -> str:
    # Avoid NSEFetcher.__init__ (it needs Supabase env); _nse_json_to_csv doesn't require it.
    fetcher = NSEFetcher.__new__(NSEFetcher)
    return fetcher._nse_json_to_csv(deals)


def test_nse_json_to_csv_handles_camelcase_keys_and_bought_sold():
    deals = [
        {
            "tradeDate": "2026-02-16",
            "symbol": "INFY",
            "companyName": "Infosys Limited",
            "participantName": "Kotak Mahindra",
            "buySell": "Bought",
            "quantityTraded": "200,000",
            "wap": "1520.25",
            "remarks": "",
        },
        {
            "tradeDate": "16-Feb-2026",
            "symbol": "TCS",
            "companyName": "Tata Consultancy Services",
            "participantName": "ICICI",
            "buySell": "Sold",
            "quantityTraded": 1000,
            "wap": 3500.5,
            "remarks": "test",
        },
    ]

    csv_text = _csv_from(deals)
    assert "Date,Symbol,Security Name,Client Name" in csv_text
    assert "INFY" in csv_text
    assert "Kotak Mahindra" in csv_text
    assert ",BUY," in csv_text
    assert "TCS" in csv_text
    assert ",SELL," in csv_text


def test_nse_json_to_csv_handles_uppercase_underscore_keys():
    deals = [
        {
            "TRADE_DATE": "2026-02-16",
            "SYMBOL": "HDFCBANK",
            "SECURITY_NAME": "HDFC Bank Ltd",
            "CLIENT_NAME": "Some Broker",
            "BUY_SELL": "S",
            "QTY_TRD": "500",
            "WAP": "1675.10",
            "REMARKS": None,
        }
    ]

    csv_text = _csv_from(deals)
    assert "HDFCBANK" in csv_text
    assert "Some Broker" in csv_text
    assert ",SELL," in csv_text


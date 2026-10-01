from app.utils.formatters import format_currency, format_percent, get_price_color


def test_format_currency_brl():
    assert format_currency(1234.56, "BRL") == "R$ 1.234,56"


def test_format_currency_usd():
    assert format_currency(100.5, "USD") == "US$ 100,50"


def test_format_percent():
    assert format_percent(5.25) == "+5.25%"
    assert format_percent(-2.1) == "-2.10%"


def test_get_price_color():
    assert get_price_color(1.5) == "bold green"
    assert get_price_color(-0.8) == "bold red"
    assert get_price_color(0.0) == "bright_black"

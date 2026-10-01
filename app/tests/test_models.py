import pytest
from pydantic import ValidationError
from app.models import AssetQuote, AssetType


def test_asset_quote_creation_and_properties():
    quote = AssetQuote(
        ticker="petr4.sa",
        asset_type=AssetType.STOCK,
        current_price=35.50,
        previous_close=34.00,
        currency="BRL",
    )

    # Verifica se o ticker foi convertido para caixa alta
    assert quote.ticker == "PETR4.SA"
    # Verifica o cálculo da variação nominal
    assert quote.price_change == 1.50
    # Verifica o cálculo da variação percentual
    assert quote.price_change_percent == 4.41


def test_asset_quote_invalid_price():
    with pytest.raises(ValidationError):
        AssetQuote(
            ticker="VALE3",
            asset_type=AssetType.STOCK,
            current_price=-10.0,  # Preço negativo deve falhar
            currency="BRL",
        )
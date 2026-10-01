from unittest.mock import patch, MagicMock
import pytest
import requests

from app.models import AssetType
from app.services.finance_api import FinanceAPIService, AssetNotFoundError, FinanceAPIError


@patch("requests.get")
def test_fetch_quote_success(mock_get):
    # Simula resposta bem-sucedida da API do Yahoo Finance
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "chart": {
            "result": [
                {
                    "meta": {
                        "regularMarketPrice": 38.50,
                        "chartPreviousClose": 37.00,
                        "currency": "BRL",
                        "regularMarketDayHigh": 39.00,
                        "regularMarketDayLow": 36.80,
                        "regularMarketVolume": 15000000,
                    }
                }
            ]
        }
    }
    mock_get.return_value = mock_response

    service = FinanceAPIService()
    quote = service.fetch_quote("PETR4", AssetType.STOCK)

    assert quote.ticker == "PETR4.SA"
    assert quote.current_price == 38.50
    assert quote.price_change == 1.50


@patch("requests.get")
def test_fetch_quote_not_found(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    service = FinanceAPIService()
    with pytest.raises(AssetNotFoundError):
        service.fetch_quote("INVALIDTICKER", AssetType.STOCK)


@patch("requests.get")
def test_fetch_quote_timeout(mock_get):
    mock_get.side_effect = requests.exceptions.Timeout()

    service = FinanceAPIService()
    with pytest.raises(FinanceAPIError):
        service.fetch_quote("PETR4", AssetType.STOCK)
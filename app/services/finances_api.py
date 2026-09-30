import logging
import requests
from typing import Optional
from app.config import settings
from app.models import AssetQuote, AssetType

# Configuração básica de logs para o módulo
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FinanceAPIError(Exception):
    """Exceção base para erros na API de Finanças."""
    pass


class AssetNotFoundError(FinanceAPIError):
    """Exceção lançada quando um ticker não é encontrado."""
    pass


class FinanceAPIService:
    """
    Serviço responsável por consumir dados financeiros em tempo real
    da API pública do Yahoo Finance.
    """

    def __init__(self, base_url: Optional[str] = None, timeout: Optional[int] = None):
        self.base_url = base_url or settings.YAHOO_FINANCE_BASE_URL
        self.timeout = timeout or settings.REQUEST_TIMEOUT
        # Headers para simular uma requisição de navegador legítima e evitar erro 403
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }

    def fetch_quote(self, ticker: str, asset_type: AssetType = AssetType.STOCK) -> AssetQuote:
        """
        Busca a cotação atual de um ativo pelo seu ticker.

        :param ticker: Código do ativo (ex: 'PETR4.SA', 'VALE3.SA', 'BTC-USD')
        :param asset_type: Tipo de ativo (STOCK, FII, CRYPTO)
        :return: Instância validada do modelo AssetQuote
        """
        formatted_ticker = ticker.strip().upper()

        # Adiciona o sufixo .SA para ações e FIIs brasileiros se o usuário esquecer
        if asset_type in (AssetType.STOCK, AssetType.FII) and not formatted_ticker.endswith(".SA"):
            formatted_ticker = f"{formatted_ticker}.SA"

        url = f"{self.base_url}/{formatted_ticker}"

        try:
            logger.info(f"Buscando cotação para o ativo: {formatted_ticker}")
            response = requests.get(url, headers=self.headers, timeout=self.timeout)

            if response.status_code == 404:
                raise AssetNotFoundError(f"Ativo '{formatted_ticker}' não encontrado.")

            response.raise_for_status()
            data = response.json()

            # Navegação no payload do Yahoo Finance
            chart_result = data.get("chart", {}).get("result")
            if not chart_result:
                raise AssetNotFoundError(f"Dados não disponíveis para o ativo '{formatted_ticker}'.")

            result_data = chart_result[0]
            meta = result_data.get("meta", {})

            # Extração dos preços
            current_price = meta.get("regularMarketPrice")
            previous_close = meta.get("chartPreviousClose") or meta.get("previousClose")
            currency = meta.get("currency", "BRL")
            day_high = meta.get("regularMarketDayHigh")
            day_low = meta.get("regularMarketDayLow")
            volume = meta.get("regularMarketVolume")

            if current_price is None:
                raise FinanceAPIError(f"Preço atual indisponível para '{formatted_ticker}'.")

            # Constrói e valida a cotação usando o Pydantic DTO
            return AssetQuote(
                ticker=formatted_ticker,
                asset_type=asset_type,
                current_price=float(current_price),
                currency=currency,
                previous_close=float(previous_close) if previous_close else None,
                day_high=float(day_high) if day_high else None,
                day_low=float(day_low) if day_low else None,
                volume=int(volume) if volume else None
            )
        
        except requests.exceptions.Timeout:
            logger.error(f"Timeout ao conectar com a API para {formatted_ticker}")
            raise FinanceAPIError("O serviço de cotações demorou muito para responder.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro de comunicação HTTP: {e}")
            raise FinanceAPIError(f"Falha na comunicação com a API financeira: {str(e)}")
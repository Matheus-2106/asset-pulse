from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class AssetType(str, Enum):
    """Tipos de ativos suportados pela aplicação."""
    STOCK = "STOCK"      # Ações (ex: PETR4, VALE3, AAPL)
    FII = "FII"          # Fundos Imobiliários (ex: HGLG11, MXRF11)
    CRYPTO = "CRYPTO"    # Criptomoedas (ex: BTC-USD, ETH-USD)


class AssetQuote(BaseModel):
    """
    Modelo de dados para a cotação de um ativo financeiro em tempo real.
    Garante validação e tipos corretos vindos da API externa.
    """
    ticker: str = Field(..., description="Símbolo do ativo (ex: PETR4.SA, BTC-USD)")
    asset_type: AssetType = Field(..., description="Categoria do ativo")
    current_price: float = Field(..., gt=0, description="Preço atual da cotação")
    currency: str = Field(default="BRL", description="Moeda da cotação")
    previous_close: Optional[float] = Field(None, description="Preço do fechamento anterior")
    day_high: Optional[float] = Field(None, description="Preço máximo do dia")
    day_low: Optional[float] = Field(None, description="Preço mínimo do dia")
    volume: Optional[int] = Field(None, ge=0, description="Volume de negociações")

    @field_validator("ticker")
    @classmethod
    def uppercase_ticker(cls, v: str) -> str:
        """Garante que o ticker seja sempre armazenado em caixa alta."""
        return v.upper().strip()

    @property
    def price_change(self) -> float:
        """Calcula a variação nominal do preço em relação ao fechamento anterior."""
        if self.previous_close:
            return round(self.current_price - self.previous_close, 2)
        return 0.0

    @property
    def price_change_percent(self) -> float:
        """Calcula a variação percentual do preço."""
        if self.previous_close and self.previous_close > 0:
            pct = ((self.current_price - self.previous_close) / self.previous_close) * 100
            return round(pct, 2)
        return 0.0


class AssetAlert(BaseModel):
    """Modelo para configuração de alertas de preço de ativos."""
    ticker: str
    target_price: float = Field(..., gt=0)
    alert_above: bool = Field(
        default=True,
        description="Se True, alerta quando o preço subir acima do alvo. Se False, quando cair."
    )
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env caso ele exista
load_dotenv()


class Settings:
    """Configurações globais da aplicação."""
    APP_NAME: str = "AssetPulse"
    VERSION: str = "0.1.0"

    # URL Base para API pública de mercado financeiro (Yahoo Finance v8)
    YAHOO_FINANCE_BASE_URL: str = os.getenv(
        "YAHOO_FINANCE_BASE_URL",
        "https://query1.finance.yahoo.com/v8/finance/chart"
    )

    # Timeout padrão para requisições HTTP em segundos
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "10"))


settings = Settings()
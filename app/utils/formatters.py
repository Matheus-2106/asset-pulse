def format_currency(value: float, currency: str = "BRL") -> str:
    """Formata valores numéricos para representação em moeda (R$ ou US$)."""
    symbol = "US$" if currency == "USD" else "R$"
    return f"{symbol} {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def format_percent(value: float) -> str:
    """Formata variações percentuais com sinal explícito de positivo ou negativo."""
    sign = "+" if value > 0 else ""
    return f"{sign}{value:.2f}%"


def get_price_color(change_percent: float) -> str:
    """Retorna a cor baseada no desempenho do ativo."""
    if change_percent > 0:
        return "bold green"
    elif change_percent < 0:
        return "bold red"
    return "bright_black"
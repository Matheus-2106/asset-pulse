import sys
import argparse
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

from app.models import AssetType, AssetQuote
from app.services.finance_api import FinanceAPIService, FinanceAPIError, AssetNotFoundError
from app.utils.formatters import format_currency, format_percent, get_price_color

console = Console()

# Catálogo de ativos sugeridos para consulta rápida
PRESET_ASSETS = {
    AssetType.STOCK: [
        ("PETR4", "Petrobras PN"),
        ("VALE3", "Vale ON"),
        ("ITUB4", "Itaú Unibanco PN"),
        ("BBAS3", "Banco do Brasil ON"),
        ("AAPL", "Apple Inc. (EUA)"),
    ],
    AssetType.FII: [
        ("HGLG11", "CSHG Logística"),
        ("MXRF11", "Maxi Renda"),
        ("XPLG11", "XP Log FII"),
        ("KNCR11", "Kinea Rendimentos Imobiliários"),
    ],
    AssetType.CRYPTO: [
        ("BTC-USD", "Bitcoin"),
        ("ETH-USD", "Ethereum"),
        ("SOL-USD", "Solana"),
    ],
}


def display_welcome():
    """Exibe o cabeçalho inicial da aplicação."""
    console.print(
        Panel.fit(
            "[bold cyan]AssetPulse[/bold cyan] - Monitor de Investimentos\n"
            "[dim]Acompanhe cotações do mercado em tempo real[/dim]",
            border_style="cyan",
        )
    )


def render_quote_table(quote: AssetQuote):
    """Renderiza a tabela estilizada com os dados do ativo."""
    table = Table(
        title=f"Cotação: [bold yellow]{quote.ticker}[/bold yellow]",
        show_header=True,
        header_style="bold magenta",
    )

    table.add_column("Métrica", style="cyan", no_wrap=True)
    table.add_column("Valor", justify="right")

    color = get_price_color(quote.price_change_percent)

    table.add_row("Preço Atual", f"[{color}]{format_currency(quote.current_price, quote.currency)}[/{color}]")
    table.add_row("Variação Nominal", f"[{color}]{format_currency(quote.price_change, quote.currency)}[/{color}]")
    table.add_row("Variação (%)", f"[{color}]{format_percent(quote.price_change_percent)}[/{color}]")

    if quote.previous_close:
        table.add_row("Fechamento Anterior", format_currency(quote.previous_close, quote.currency))
    if quote.day_high:
        table.add_row("Máxima do Dia", format_currency(quote.day_high, quote.currency))
    if quote.day_low:
        table.add_row("Mínima do Dia", format_currency(quote.day_low, quote.currency))
    if quote.volume:
        table.add_row("Volume de Negociação", f"{quote.volume:,}".replace(",", "."))

    console.print(table)


def process_ticker_query(service: FinanceAPIService, ticker: str, asset_type: AssetType):
    """Realiza a busca e exibição da cotação."""
    try:
        with console.status(f"[bold green]Consultando {ticker}...[/bold green]"):
            quote = service.fetch_quote(ticker=ticker, asset_type=asset_type)
        render_quote_table(quote)
    except AssetNotFoundError as e:
        console.print(f"[bold red]Erro:[/bold red] {e}")
    except FinanceAPIError as e:
        console.print(f"[bold red]Erro no serviço:[/bold red] {e}")


def select_ticker_from_options(asset_type: AssetType) -> str:
    """Exibe um menu estilizado com ativos sugeridos e opção de digitação manual."""
    options = PRESET_ASSETS.get(asset_type, [])

    console.print("\n[bold yellow]Opções de Ativos Disponíveis:[/bold yellow]")
    for idx, (ticker, name) in enumerate(options, 1):
        console.print(f"  [bold cyan]{idx}[/bold cyan]. [bold white]{ticker}[/bold white] - {name}")

    console.print(f"  [bold cyan]{len(options) + 1}[/bold cyan]. Outro ativo (Digitar manualmente)")

    valid_choices = [str(i) for i in range(1, len(options) + 2)]
    choice = Prompt.ask("\nEscolha um ativo da lista", choices=valid_choices, default="1")

    choice_idx = int(choice) - 1

    if choice_idx < len(options):
        return options[choice_idx][0]
    else:
        ticker = Prompt.ask("\nDigite o símbolo/ticker desejado (ex: WEGE3)").strip()
        return ticker


def main():
    parser = argparse.ArgumentParser(description="AssetPulse - Monitor de Investimentos no Terminal")
    parser.add_argument("-t", "--ticker", type=str, help="Ticker do ativo (ex: PETR4, VALE3, BTC-USD)")
    parser.add_argument(
        "-type",
        "--asset-type",
        choices=["stock", "fii", "crypto"],
        default="stock",
        help="Tipo do ativo (padrão: stock)",
    )

    args = parser.parse_args()
    service = FinanceAPIService()

    # Execução direta por argumentos de linha de comando
    if args.ticker:
        display_welcome()
        type_mapping = {
            "stock": AssetType.STOCK,
            "fii": AssetType.FII,
            "crypto": AssetType.CRYPTO,
        }
        process_ticker_query(service, args.ticker, type_mapping[args.asset_type])
        return

    # Execução via menu interativo
    display_welcome()

    while True:
        console.print("\n[bold]Menu Principal[/bold]")
        console.print("1. Consultar Ação / FII / Cripto")
        console.print("2. Instruções de Uso e Exemplos")
        console.print("3. Sair")

        choice = Prompt.ask("Escolha uma opção", choices=["1", "2", "3"], default="1")

        if choice == "3":
            console.print("[yellow]Encerrando aplicação.[/yellow]")
            sys.exit(0)

        if choice == "2":
            console.print(
                Panel(
                    "[bold yellow]💡 Como funcionam os Tickers:[/bold yellow]\n\n"
                    "• [bold]Ações B3:[/bold] PETR4, VALE3, ITUB4, WEGE3 (sufixo .SA automático)\n"
                    "• [bold]FIIs:[/bold] HGLG11, MXRF11, XPLG11\n"
                    "• [bold]Ações Internacionais:[/bold] AAPL, TSLA, MSFT\n"
                    "• [bold]Criptomoedas:[/bold] BTC-USD, ETH-USD, SOL-USD\n\n"
                    "[bold yellow]Comando Rápido via Terminal:[/bold yellow]\n"
                    "• `python -m app.cli -t PETR4`\n"
                    "• `python -m app.cli -t BTC-USD --asset-type crypto`",
                    title="Guia Rápido",
                    border_style="blue",
                )
            )
            continue

        console.print("\n[bold]Selecione a categoria do ativo:[/bold]")
        console.print("1. Ação (Nacional / Internacional)")
        console.print("2. Fundo Imobiliário (FII)")
        console.print("3. Criptomoeda")

        cat_choice = Prompt.ask("Opção", choices=["1", "2", "3"], default="1")
        cat_map = {
            "1": AssetType.STOCK,
            "2": AssetType.FII,
            "3": AssetType.CRYPTO,
        }
        selected_type = cat_map[cat_choice]

        ticker = select_ticker_from_options(selected_type)
        if not ticker:
            console.print("[red]O ticker não pode ser vazio.[/red]")
            continue

        process_ticker_query(service, ticker, selected_type)


if __name__ == "__main__":
    main()
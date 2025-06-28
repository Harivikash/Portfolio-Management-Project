import yfinance as yf

def get_latest_prices(symbols: list[str]) -> dict[str, float]:
    """
    Fetches the latest market price for each symbol.
    Returns a dict: { symbol: latest_price }
    """
    prices = {}
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d")
            if not data.empty:
                prices[symbol] = data['Close'].iloc[-1]
            else:
                prices[symbol] = None
        except Exception:
            prices[symbol] = None
    return prices

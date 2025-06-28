#price_fetcher 

import yfinance as yf

def get_current_price(symbol: str) -> float:
    """
    Get the latest close price for a given stock symbol.
    """
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period='1d')
    return todays_data['Close'].iloc[-1]

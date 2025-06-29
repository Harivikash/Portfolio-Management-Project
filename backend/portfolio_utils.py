import pandas as pd
from price_utils import get_latest_prices
from datetime import datetime

import numpy as np
from sklearn.datasets import load_iris
import yfinance as yf

# Loading irirs dataset
data = load_iris()
df = pd.DataFrame(data.data,
                  columns = data.feature_names)
# print(df)

import pandas as pd
from datetime import datetime
from price_fetcher import get_current_price


def calculate_portfolio_summary(df: pd.DataFrame) -> dict:
    df.columns = df.columns.str.strip().str.title()
    df['Date'] = pd.to_datetime(df['Fill Time'])

    symbols = df['Symbol'].unique().tolist()
    prices = get_latest_prices(symbols)

    total_cost_open = 0.0
    market_value_open = 0.0

    cashflows = []
    for _, row in df.iterrows():
        side = row['Side'].lower()
        amount = -row['Fill Amount'] if side == 'buy' else row['Fill Amount']
        cashflows.append((row['Date'], amount))

    for symbol in symbols:
        symbol_df = df[df['Symbol'] == symbol].copy()  # explicit copy

        symbol_df.loc[:, 'Signed Qty'] = symbol_df.apply(
        lambda row: row['Fill Qty'] if row['Side'].lower() == 'buy' else -row['Fill Qty'],
        axis=1
    )

        net_qty = symbol_df['Signed Qty'].sum()
        
        if net_qty <= 0:
            continue  # Position is fully closed, skip for unrealized
        
        # Calculate average cost basis for remaining qty
        buys = symbol_df[symbol_df['Side'].str.lower() == 'buy']
        total_buys_qty = buys['Fill Qty'].sum()
        total_buys_amt = buys['Fill Amount'].sum()
        
        avg_buy_price = total_buys_amt / total_buys_qty if total_buys_qty != 0 else 0
        cost_basis_open = net_qty * avg_buy_price
        latest_price = prices.get(symbol, 0)
        market_value = net_qty * latest_price

        total_cost_open += cost_basis_open
        market_value_open += market_value

    # Add final market value to cashflows for XIRR
    if market_value_open > 0:
        cashflows.append((datetime.today(), market_value_open))

    summary = {
        'total_invested_open': round(total_cost_open, 2),
        'current_value_open': round(market_value_open, 2),
        'unrealized_profit': round(market_value_open - total_cost_open, 2),
        'total_fees': round(df['Total Fees'].sum(), 2) if 'Total Fees' in df.columns else 0.0,
        'xirr': None,
        'cagr': None,
    }

    try:
        summary['xirr'] = round(xirr(cashflows) * 100, 2) if xirr(cashflows) else None
    except Exception:
        summary['xirr'] = None

    try:
        start_date = df['Date'].min()
        end_date = datetime.today()
        summary['cagr'] = round(calculate_cagr(total_cost_open, market_value_open, start_date, end_date) * 100, 2)
    except Exception:
        summary['cagr'] = None

    return summary

def calculate_cagr(start_value, end_value, start_date, end_date):
    duration_years = (end_date - start_date).days / 365.25
    if start_value <= 0 or duration_years <= 0:
        return 0.0
    return (end_value / start_value) ** (1 / duration_years) - 1

def xnpv(rate, cashflows):
    return sum([
        cf / (1 + rate) ** ((date - cashflows[0][0]).days / 365.0)
        for date, cf in cashflows
    ])

def xirr(cashflows, guess=0.1):
    tolerance = 1e-6
    max_iterations = 100
    rate = guess

    for _ in range(max_iterations):
        f_value = xnpv(rate, cashflows)
        f_derivative = (xnpv(rate + tolerance, cashflows) - f_value) / tolerance
        if f_derivative == 0:
            return None
        new_rate = rate - f_value / f_derivative
        if abs(new_rate - rate) < tolerance:
            return new_rate
        rate = new_rate
    return None

def get_quote_types(symbols):
    result = {}
    for sym in symbols:
        ticker = yf.Ticker(sym)
        info = ticker.info
        result[sym] = info.get("quoteType", "UNKNOWN")
    return result
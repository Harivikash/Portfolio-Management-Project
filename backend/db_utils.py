import pandas as pd

def records_to_df(records):
    """
    Convert list of SQLAlchemy model instances to pandas DataFrame.
    """
    if not records:
        return pd.DataFrame()

    data = []
    for rec in records:
        data.append({
            "Side": rec.side,
            "Symbol": rec.symbol,
            "Name": rec.name,
            "Fill Qty": rec.fill_qty,
            "Fill Price": rec.fill_price,
            "Fill Amount": rec.fill_amount,
            "Fill Time": rec.fill_time,
            "Markets": rec.markets,
            "Currency": rec.currency,
            "Total Fees": rec.total_fees,
        })
    df = pd.DataFrame(data)
    return df

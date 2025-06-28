# csv_parser.py

import pandas as pd
import io

REQUIRED_FIELDS = [
    'Side','Name', 'Symbol', 'Fill Qty', 'Fill Price', 'Fill Amount',
    'Fill Time', 'Markets', 'Currency'
]

FEE_FIELDS = [
    'Platform Fees', 'Commission', 'Trading Fees',
    'Clearing Fees', 'Settlement Fees'
]

def parse_and_validate_csv(file_content: bytes) -> pd.DataFrame:
    """
    Parses and validates the uploaded CSV content.
    Returns a cleaned DataFrame ready for DB insertion or analysis.
    Raises ValueError if there are issues.
    """
    try:
        df = pd.read_csv(io.StringIO(file_content.decode('utf-8')))
        df.columns = df.columns.str.strip().str.title()
    except Exception as e:
        raise ValueError(f"CSV parsing failed: {e}")

    # Validate required columns
    missing = [col for col in REQUIRED_FIELDS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Clean and normalize data
    # Remove unrecognized timezone suffix before parsing datetime
    df['Fill Time'] = df['Fill Time'].str.replace(r'\sET$', '', regex=True)
    df['Fill Time'] = pd.to_datetime(df['Fill Time'], errors='coerce')
    df['Fill Qty'] = pd.to_numeric(df['Fill Qty'], errors='coerce')
    df['Fill Price'] = pd.to_numeric(df['Fill Price'], errors='coerce')
    df['Fill Amount'] = pd.to_numeric(df['Fill Amount'], errors='coerce')

    # Basic cleaning
    df['Symbol'] = df['Symbol'].str.strip().str.upper()
    df['Name'] = df['Name'].str.strip().str.upper()
    df['Side'] = df['Side'].str.strip().str.capitalize()

    # Calculate Total Fees
    for col in FEE_FIELDS:
        if col not in df.columns:
            df[col] = 0
        else:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    df['Total Fees'] = df[FEE_FIELDS].sum(axis=1)

    # Drop invalid rows
    df = df.dropna(subset=['Fill Time', 'Fill Qty', 'Fill Price'])
    df = df[df['Fill Qty'] > 0]
    
    # Rename Fill Time to Date for consistency
    df['Date'] = df['Fill Time']
    # print(df.head())
    return df

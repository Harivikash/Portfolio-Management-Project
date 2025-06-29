from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from csv_parser import parse_and_validate_csv
from crud import save_transactions, get_all_transactions
from database import SessionLocal, engine
import models
from db_utils import records_to_df
from portfolio_utils import calculate_portfolio_summary 
from portfolio_utils import get_latest_prices, get_quote_types
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)  # Auto-create tables


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or limit to ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")

    content = await file.read()
    try:
        df = parse_and_validate_csv(content)
        save_transactions(df, db)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    return {"message": f"{len(df)} valid transactions stored successfully."}

@app.get("/summary")
def portfolio_summary(db: Session = Depends(get_db)):
    records = get_all_transactions(db)
    if not records:
        raise HTTPException(status_code=404, detail="No transactions found")

    df = records_to_df(records)

    summary = calculate_portfolio_summary(df)

    df['Side'] = df['Side'].str.lower()
    df['Quantity'] = df.apply(lambda row: row['Fill Qty'] if row['Side'] == 'buy' else -row['Fill Qty'], axis=1)

    symbols = df['Symbol'].unique().tolist()
    prices = get_latest_prices(symbols)
    quote_types = get_quote_types(symbols)   # ✅ NEW

    df['Current Price'] = df['Symbol'].map(prices)
    df['Quote Type'] = df['Symbol'].map(quote_types)  # ✅ NEW

    df['Current Value'] = df['Quantity'] * df['Current Price']
    total_value = df['Current Value'].sum()

    if total_value == 0:
        percentages = []
    else:
        percentages = (
            df.groupby('Symbol')['Current Value']
            .sum()
            .reset_index()
            .assign(percent=lambda x: (x['Current Value'] / total_value * 100).round(2))
            .to_dict(orient='records')
        )

    summary['holdings_percentages'] = percentages

    # ✅ Add the split for Pie chart:
    quote_split = (
        df.groupby('Quote Type')['Current Value'].sum().to_dict()
        if total_value != 0 else {}
    )
    summary['quote_type_split'] = quote_split

    return summary


@app.get("/data_json", response_class=JSONResponse)
def portfolio_data_json(db: Session = Depends(get_db)):
    records = get_all_transactions(db)
    if not records:
        raise HTTPException(status_code=404, detail="No transactions found")

    df = records_to_df(records)
    df.columns = df.columns.str.strip().str.title()

    symbols = df['Symbol'].unique().tolist()
    prices = get_latest_prices(symbols)
    quote_types = get_quote_types(symbols)

    def calc_unrealized(row):
        side = row['Side'].lower()
        qty = row['Fill Qty'] if side == 'buy' else -row['Fill Qty']
        price_now = prices.get(row['Symbol'], 0)
        return qty * (price_now - row['Fill Price'])

    df['Current Price'] = df['Symbol'].map(prices)
    df['Unrealized Profit'] = df.apply(calc_unrealized, axis=1)
    df['Quote Type'] = df['Symbol'].map(quote_types)   # ✅ Add this column!

    summary = calculate_portfolio_summary(df)

    # Convert Timestamp/date columns to string
    for col in df.select_dtypes(include=['datetime64[ns]', 'datetime64[ns, UTC]']).columns:
        df[col] = df[col].astype(str)

    transactions = df.to_dict(orient='records')

    return {
        "summary": summary,
        "transactions": transactions
    }

@app.get("/data", response_class=HTMLResponse)
def portfolio_data(db: Session = Depends(get_db)):
    records = get_all_transactions(db)
    if not records:
        raise HTTPException(status_code=404, detail="No transactions found")

    df = records_to_df(records)
    df.columns = df.columns.str.strip().str.title()

    symbols = df['Symbol'].unique().tolist()
    prices = get_latest_prices(symbols)

    def calc_unrealized(row):
        side = row['Side'].lower()
        qty = row['Fill Qty'] if side == 'buy' else -row['Fill Qty']
        price_now = prices.get(row['Symbol'], 0)
        return qty * (price_now - row['Fill Price'])

    df['Current Price'] = df['Symbol'].map(prices)
    df['Unrealized Profit'] = df.apply(calc_unrealized, axis=1)

    summary = calculate_portfolio_summary(df)

    html_table = df.to_html(index=False, classes="table table-striped table-bordered")

    # Format summary dict into a Bootstrap card with list-group for neatness
    summary_html = "<ul class='list-group'>"
    for key, value in summary.items():
        # Format floats nicely
        if isinstance(value, float):
            display_val = f"{value:,.2f}"
        elif value is None:
            display_val = "N/A"
        else:
            display_val = str(value)
        summary_html += f"<li class='list-group-item d-flex justify-content-between align-items-center'>{key.replace('_',' ').title()}<span class='badge bg-primary rounded-pill'>{display_val}</span></li>"
    summary_html += "</ul>"

    html_page = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Portfolio Data</title>
        <!-- Bootstrap CSS CDN -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" />
    </head>
    <body class="p-4">
        <div class="container">
            <h1 class="mb-4">Portfolio Summary</h1>
            <div class="card mb-5" style="max-width: 500px;">
                <div class="card-body">
                    {summary_html}
                </div>
            </div>

            <h2 class="mb-3">Transactions Table</h2>
            {html_table}
        </div>
    </body>
    </html>
    """

    return HTMLResponse(content=html_page)



@app.delete("/clear_transactions")
def clear_transactions(db: Session = Depends(get_db)):
    db.query(models.Transaction).delete()
    db.commit()
    return {"message": "All transactions cleared."}


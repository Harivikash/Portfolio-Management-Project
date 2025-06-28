from sqlalchemy.orm import Session
import models
import pandas as pd

def save_transactions(df: pd.DataFrame, db: Session):
    """
    Save each row of the dataframe as a Transaction record in DB.
    """
    for _, row in df.iterrows():
        txn = models.Transaction(
            side=row['Side'],
            symbol=row['Symbol'],
            name=row['Name'],
            fill_qty=row['Fill Qty'],
            fill_price=row['Fill Price'],
            fill_amount=row['Fill Amount'],
            fill_time=row['Fill Time'],
            markets=row['Markets'],
            currency=row['Currency'],
            total_fees=row.get('Total Fees', 0)
        )
        db.add(txn)
    db.commit()
    print("Saved markets from CSV:", df['Markets'].unique())  # Debug print here

def get_all_transactions(db: Session):
    """
    Retrieve all transaction records from the database.
    """
    return db.query(models.Transaction).all()

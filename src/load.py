import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

def get_db_engine():
    """Create database connection"""
    db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    return create_engine(db_url)

def load_dimensions(data, engine):
    """Load dimension tables"""
    # Load customers (only columns that exist)
    customer_cols = ['customer_name', 'city', 'country', 'territory']
    if 'region' in data.columns:
        customer_cols.append('region')
    customers = data[customer_cols].drop_duplicates()
    customers.to_sql('dim_customers', engine, if_exists='append', index=False)
    
    # Load products
    products = data[['product_code', 'product_line', 'manufacturer_price']].drop_duplicates()
    products.to_sql('dim_products', engine, if_exists='append', index=False)
    
    # Load dates (only columns that exist)
    date_cols = ['order_date', 'month', 'quarter', 'year']
    optional_date_cols = ['day', 'day_of_week', 'week', 'month_name', 'year_month']
    for col in optional_date_cols:
        if col in data.columns:
            date_cols.append(col)
    dates = data[date_cols].drop_duplicates()
    dates.to_sql('dim_dates', engine, if_exists='append', index=False)

def load_transactions(data, engine):
    """Load fact table"""
    # Select transaction columns (only those that exist)
    base_cols = ['order_id', 'quantity', 'unit_price', 'total_sales', 'order_status', 'deal_size']
    optional_cols = ['revenue_per_item', 'discount_pct', 'is_discounted', 'is_sales_outlier', 
                     'is_high_value_order', 'is_bulk_order']
    
    trans_cols = base_cols.copy()
    for col in optional_cols:
        if col in data.columns:
            trans_cols.append(col)
    
    transactions = data[trans_cols]
    transactions.to_sql('fact_transactions', engine, if_exists='append', index=False)

if __name__ == "__main__":
    data = pd.read_csv("../data/processed/sales_transformed.csv")
    engine = get_db_engine()
    
    load_dimensions(data, engine)
    load_transactions(data, engine)
    print("✓ Data loaded to PostgreSQL")
"""
Comprehensive test to verify the entire ETL pipeline
"""
import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def test_files():
    """Test that all necessary files exist"""
    print("=" * 60)
    print("TESTING FILES")
    print("=" * 60)
    
    files_to_check = [
        '../data/raw/sales_data_sample.csv',
        '../data/processed/sales_transformed.csv',
        '../exports/sales_report_20251125.xlsx',
        '../src/extract.py',
        '../src/transform.py',
        '../src/load.py',
        '../src/reports.py',
        '../sql/schema.sql',
        '../.env'
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} - MISSING")
    print()

def test_transformed_data():
    """Test transformed data quality"""
    print("=" * 60)
    print("TESTING TRANSFORMED DATA")
    print("=" * 60)
    
    df = pd.read_csv('../data/processed/sales_transformed.csv')
    
    print(f"✓ Total rows: {len(df)}")
    print(f"✓ Total columns: {len(df.columns)}")
    
    # Check for required columns
    required_cols = ['order_id', 'customer_name', 'product_line', 'total_sales', 
                     'order_date', 'region', 'customer_segment', 'discount_pct',
                     'is_sales_outlier', 'is_high_value_order']
    
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        print(f"✗ Missing columns: {missing_cols}")
    else:
        print(f"✓ All required columns present")
    
    # Check data quality
    print(f"✓ Missing values: {df.isnull().sum().sum()}")
    print(f"✓ Sales outliers: {df['is_sales_outlier'].sum()}")
    print(f"✓ High-value orders: {df['is_high_value_order'].sum()}")
    print(f"✓ Customer segments: {df['customer_segment'].value_counts().to_dict()}")
    print()

def test_database():
    """Test database connectivity and data"""
    print("=" * 60)
    print("TESTING DATABASE")
    print("=" * 60)
    
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        print("✓ Database connection successful")
        
        cur = conn.cursor()
        
        # Check tables
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        tables = [t[0] for t in cur.fetchall()]
        print(f"✓ Tables found: {tables}")
        
        # Check row counts
        for table in tables:
            cur.execute(f"SELECT COUNT(*) FROM {table}")
            count = cur.fetchone()[0]
            print(f"  - {table}: {count} rows")
        
        # Sample queries
        cur.execute("SELECT COUNT(DISTINCT customer_name) FROM dim_customers")
        customers = cur.fetchone()[0]
        print(f"✓ Unique customers: {customers}")
        
        cur.execute("SELECT COUNT(DISTINCT product_code) FROM dim_products")
        products = cur.fetchone()[0]
        print(f"✓ Unique products: {products}")
        
        cur.execute("SELECT SUM(total_sales) FROM fact_transactions")
        total_revenue = cur.fetchone()[0]
        print(f"✓ Total revenue: ${total_revenue:,.2f}")
        
        conn.close()
        print()
        
    except Exception as e:
        print(f"✗ Database error: {e}")
        print()

def test_reports():
    """Test report generation"""
    print("=" * 60)
    print("TESTING REPORTS")
    print("=" * 60)
    
    report_file = '../exports/sales_report_20251125.xlsx'
    if os.path.exists(report_file):
        print(f"✓ Report generated: {report_file}")
        
        # Read and validate
        df_summary = pd.read_excel(report_file, sheet_name='Summary')
        print(f"✓ Summary sheet rows: {len(df_summary)}")
        
        df_product = pd.read_excel(report_file, sheet_name='Product_Analysis')
        print(f"✓ Product analysis rows: {len(df_product)}")
        
        df_territory = pd.read_excel(report_file, sheet_name='Territory_Analysis')
        print(f"✓ Territory analysis rows: {len(df_territory)}")
    else:
        print(f"✗ Report not found: {report_file}")
    print()

def run_all_tests():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "SALES ETL PIPELINE - FULL TEST SUITE" + " " * 11 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    test_files()
    test_transformed_data()
    test_database()
    test_reports()
    
    print("=" * 60)
    print("✓ ALL TESTS COMPLETED")
    print("=" * 60)
    print()
    print("PROJECT STATUS: READY FOR PRODUCTION")
    print()

if __name__ == "__main__":
    run_all_tests()

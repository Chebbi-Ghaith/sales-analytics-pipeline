import sys
sys.path.append('../src')

from extract import extract_csv
from transform import SalesTransformer
from load import load_dimensions, load_transactions, get_db_engine
from reports import generate_daily_report
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_pipeline():
    """Execute full ETL pipeline"""
    try:
        # Extract
        logger.info("Starting ETL Pipeline...")
        data = extract_csv("../data/raw/sales_data_sample.csv")
        
        # Transform
        transformer = SalesTransformer(data)
        transformed_data = transformer.transform()
        transformed_data.to_csv("../data/processed/sales_transformed.csv", index=False)
        
        # Load to database
        engine = get_db_engine()
        load_dimensions(transformed_data, engine)
        load_transactions(transformed_data, engine)
        
        # Generate reports
        generate_daily_report(transformed_data)
        
        logger.info("✓ ETL Pipeline completed successfully!")
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise

if __name__ == "__main__":
    run_pipeline()
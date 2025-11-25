import pandas as pd
import logging

logger = logging.getLogger(__name__)

def extract_csv(file_path, encoding='latin-1'):
    """Extract data from CSV file"""
    try:
        logger.info(f"Extracting data from {file_path}")
        df = pd.read_csv(file_path, encoding=encoding)
        logger.info(f"Extracted {len(df)} rows, {len(df.columns)} columns")
        return df
    except Exception as e:
        logger.error(f"Failed to extract data: {e}")
        raise

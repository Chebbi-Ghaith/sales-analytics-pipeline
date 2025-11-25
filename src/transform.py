import pandas as pd
import numpy as np
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SalesTransformer:
    """Transform and clean sales data"""
    
    def __init__(self, df):
        self.df = df.copy()
    
    def rename_columns(self):
        """Rename columns to snake_case"""
        logger.info("Renaming columns...")
        column_rename = {
            'ORDERNUMBER': 'order_id',
            'ORDERDATE': 'order_date',
            'STATUS': 'order_status',
            'QUANTITYORDERED': 'quantity',
            'PRICEEACH': 'unit_price',
            'SALES': 'total_sales',
            'YEAR_ID': 'year',
            'MONTH_ID': 'month',
            'QTR_ID': 'quarter',
            'PRODUCTLINE': 'product_line',
            'PRODUCTCODE': 'product_code',
            'MSRP': 'manufacturer_price',
            'CUSTOMERNAME': 'customer_name',
            'CITY': 'city',
            'COUNTRY': 'country',
            'TERRITORY': 'territory',
            'DEALSIZE': 'deal_size'
        }
        self.df = self.df.rename(columns=column_rename)
        return self
    
    def parse_dates(self):
        """Convert ORDERDATE to datetime"""
        logger.info("Parsing dates...")
        self.df['order_date'] = pd.to_datetime(self.df['order_date'], errors='coerce')
        return self
    
    def handle_missing_values(self):
        """Handle missing values in key columns"""
        logger.info("Handling missing values...")
        
        # Drop rows with critical missing values
        critical_cols = ['order_id', 'total_sales', 'customer_name', 'product_code']
        before = len(self.df)
        self.df.dropna(subset=critical_cols, inplace=True)
        after = len(self.df)
        
        if before != after:
            logger.warning(f"Dropped {before - after} rows due to missing critical values")
        
        return self
    
    def add_date_components(self):
        """Extract date parts for time-series analysis"""
        logger.info("Adding date components...")
        self.df['day'] = self.df['order_date'].dt.day
        self.df['day_of_week'] = self.df['order_date'].dt.day_name()
        self.df['week'] = self.df['order_date'].dt.isocalendar().week
        self.df['month_name'] = self.df['order_date'].dt.month_name()
        self.df['year_month'] = self.df['order_date'].dt.to_period('M').astype(str)
        return self
    
    def add_derived_columns(self):
        """Add calculated fields"""
        logger.info("Adding derived columns...")
        
        # Revenue per item
        self.df['revenue_per_item'] = (self.df['total_sales'] / self.df['quantity']).round(2)
        
        # Discount percentage
        self.df['discount_pct'] = ((self.df['manufacturer_price'] - self.df['unit_price']) / self.df['manufacturer_price'] * 100).round(2)
        
        # Flag discounted items
        self.df['is_discounted'] = self.df['discount_pct'] > 0
        
        return self
    
    def detect_anomalies(self):
        """Flag anomalous transactions"""
        logger.info("Detecting anomalies...")
        
        # Flag negative quantities
        self.df['is_negative_qty'] = self.df['quantity'] < 0
        
        # Flag outliers in SALES using IQR method
        Q1 = self.df['total_sales'].quantile(0.25)
        Q3 = self.df['total_sales'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        self.df['is_sales_outlier'] = (self.df['total_sales'] < lower_bound) | (self.df['total_sales'] > upper_bound)
        
        # Log anomaly counts
        neg_qty = self.df['is_negative_qty'].sum()
        outliers = self.df['is_sales_outlier'].sum()
        logger.info(f"Found {neg_qty} negative quantities and {outliers} sales outliers")
        
        return self
    
    def standardize_text(self):
        """Standardize text fields"""
        logger.info("Standardizing text...")
        self.df['customer_name'] = self.df['customer_name'].str.strip().str.title()
        self.df['city'] = self.df['city'].str.strip().str.title()
        self.df['country'] = self.df['country'].str.strip().str.upper()
        self.df['product_line'] = self.df['product_line'].str.strip().str.title()
        self.df['deal_size'] = self.df['deal_size'].str.strip().str.title()
        self.df['order_status'] = self.df['order_status'].str.strip().str.title()
        return self
    
    def add_customer_segmentation(self):
        """Calculate customer lifetime value and segmentation"""
        logger.info("Adding customer segmentation...")
        
        customer_metrics = self.df.groupby('customer_name').agg({
            'total_sales': 'sum',
            'order_id': 'nunique',
            'order_date': 'max'
        }).rename(columns={
            'total_sales': 'customer_lifetime_value',
            'order_id': 'order_count',
            'order_date': 'last_order_date'
        })
        
        # Merge back to main dataset
        self.df = self.df.merge(customer_metrics, on='customer_name', how='left')
        
        # Segment customers by value
        self.df['customer_segment'] = pd.cut(
            self.df['customer_lifetime_value'],
            bins=[0, 50000, 150000, float('inf')],
            labels=['Low Value', 'Medium Value', 'High Value']
        )
        
        return self
    
    def add_business_flags(self):
        """Add business categorization flags"""
        logger.info("Adding business flags...")
        
        # Flag high-value orders (top 25%)
        high_value_threshold = self.df['total_sales'].quantile(0.75)
        self.df['is_high_value_order'] = self.df['total_sales'] >= high_value_threshold
        
        # Flag bulk orders
        self.df['is_bulk_order'] = self.df['quantity'] >= 40
        
        # Create region mapping
        region_map = {
            'NA': 'North America',
            'EMEA': 'Europe/Middle East/Africa',
            'APAC': 'Asia Pacific'
        }
        self.df['region'] = self.df['territory'].map(region_map)
        
        return self
    
    def transform(self):
        """Execute all transformations"""
        logger.info("Starting transformation pipeline...")
        
        self.rename_columns()
        self.parse_dates()
        self.handle_missing_values()
        self.add_date_components()
        self.add_derived_columns()
        self.detect_anomalies()
        self.standardize_text()
        self.add_customer_segmentation()
        self.add_business_flags()
        
        logger.info(f"Transformation complete. Final shape: {self.df.shape}")
        return self.df

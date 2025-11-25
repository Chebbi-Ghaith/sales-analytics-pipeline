import pandas as pd
import matplotlib.pyplot as plt

# Load transformed data
data = pd.read_csv("../data/processed/sales_transformed.csv")
data['order_date'] = pd.to_datetime(data['order_date'])

## KPI 1: Monthly Revenue Trends
monthly_revenue = data.groupby('year_month')['total_sales'].sum().reset_index()
monthly_revenue.columns = ['month', 'revenue']

## KPI 2: Top-Selling Products
top_products = data.groupby('product_line')['total_sales'].sum().sort_values(ascending=False)

## KPI 3: Customer Segmentation
segment_analysis = data.groupby(['customer_segment', 'territory'])['total_sales'].sum()

## KPI 4: Year-over-Year Growth
yoy_growth = data.groupby('year')['total_sales'].sum().pct_change() * 100

## KPI 5: Order Status Distribution
status_distribution = data['order_status'].value_counts()
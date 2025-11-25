import pandas as pd
from datetime import datetime

def generate_daily_report(data):
    """Generate daily aggregated report"""
    report = data.groupby(['year_month', 'product_line', 'territory']).agg({
        'total_sales': 'sum',
        'quantity': 'sum',
        'order_id': 'nunique'
    }).reset_index()
    
    report.columns = ['month', 'product_line', 'territory', 'revenue', 'units_sold', 'num_orders']
    
    # Export to Excel with multiple sheets
    timestamp = datetime.now().strftime("%Y%m%d")
    filename = f"../exports/sales_report_{timestamp}.xlsx"
    
    with pd.ExcelWriter(filename) as writer:
        report.to_excel(writer, sheet_name='Summary', index=False)
        
        # Add pivot tables for Power BI
        pivot_product = data.pivot_table(values='total_sales', index='product_line', columns='year', aggfunc='sum')
        pivot_product.to_excel(writer, sheet_name='Product_Analysis')
        
        pivot_territory = data.pivot_table(values='total_sales', index='territory', columns='year', aggfunc='sum')
        pivot_territory.to_excel(writer, sheet_name='Territory_Analysis')
    
    print(f"✓ Report exported: {filename}")

if __name__ == "__main__":
    data = pd.read_csv("../data/processed/sales_transformed.csv")
    generate_daily_report(data)
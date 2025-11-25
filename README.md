# Sales Data ETL & Analytics Pipeline

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-336791.svg)](https://www.postgresql.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A production-ready ETL pipeline that processes sales transaction data, performs comprehensive data quality checks, computes business KPIs, and exports analytics-ready datasets for BI tools.

## 🎯 Project Overview

This project demonstrates a complete data engineering workflow:

- **Extract**: Ingest raw CSV sales data (2,823 transactions, 2003-2005)
- **Transform**: Clean, normalize, and enrich data with 25+ derived features
- **Load**: Store in normalized PostgreSQL database (star schema)
- **Analyze**: Compute KPIs including revenue trends, customer segmentation, anomaly detection
- **Report**: Generate Excel reports with pivot tables for Power BI/Tableau

### Key Metrics
- 📊 **$10M+** total revenue processed
- 👥 **92** unique customers across 19 countries
- 🏷️ **109** unique products in 7 product lines
- 🚨 **81** anomalies detected and flagged

---

## 🚀 Features

### Data Processing
- ✅ Automated data extraction with encoding detection
- ✅ Date parsing and time-series feature engineering
- ✅ Missing value handling and data validation
- ✅ Anomaly detection using IQR method
- ✅ Text standardization and normalization

### Analytics
- 📈 **Customer Segmentation**: RFM analysis (Low/Medium/High value)
- 💰 **Revenue Analytics**: Monthly trends, YoY growth
- 🎯 **Product Performance**: Top sellers, discount analysis
- 🌍 **Geographic Analysis**: Territory and region breakdowns
- ⚠️ **Data Quality Monitoring**: Outlier detection, validation checks

### Database Design
- 🗄️ Dimensional modeling (star schema)
- 🔗 Normalized tables (customers, products, dates, transactions)
- ⚡ Optimized indexes for query performance
- 🔄 Incremental load support

---

## 📁 Project Structure

```
sales_project/
├── src/                        # Core ETL modules
│   ├── extract.py             # Data extraction logic
│   ├── transform.py           # Transformation pipeline
│   ├── load.py                # Database loading
│   └── reports.py             # Report generation
├── scripts/                    # Executable scripts
│   ├── run_etl.py             # Main ETL orchestrator
│   ├── init_db.py             # Database initialization
│   ├── test_pipeline.py       # Comprehensive tests
│   └── check_db.py            # Database validation
├── sql/                        # Database schema
│   └── schema.sql             # Table definitions
├── data/                       # Data storage
│   ├── raw/                   # Original CSV files
│   └── processed/             # Transformed datasets
├── exports/                    # Generated reports (Excel)
├── logs/                       # Application logs
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
├── .gitignore                # Git exclusions
└── README.md                 # This file
```

---

## 🛠️ Setup Instructions

### Prerequisites
- **Python 3.9+** ([Download](https://www.python.org/downloads/))
- **PostgreSQL 13+** ([Download](https://www.postgresql.org/download/))
- **pip** (included with Python)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd sales_project
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   .\venv\Scripts\Activate.ps1
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   # Copy example config
   cp .env.example .env
   
   # Edit .env with your PostgreSQL credentials
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=sales_analytics
   DB_USER=postgres
   DB_PASSWORD=your_password
   ```

5. **Initialize database**
   ```bash
   python scripts/init_db.py
   ```

---

## 🎮 Usage

### Run Full ETL Pipeline
```bash
cd scripts
python run_etl.py
```

**Output:**
- Transformed CSV: `data/processed/sales_transformed.csv`
- Excel Report: `exports/sales_report_YYYYMMDD.xlsx`
- Database tables populated

### Test the Pipeline
```bash
python scripts/test_pipeline.py
```

### Check Database Status
```bash
python scripts/check_db.py
```

---

## 📊 Database Schema

### Dimension Tables
- **dim_customers**: Customer master data (92 customers)
- **dim_products**: Product catalog (109 products)
- **dim_dates**: Date dimension for time-series analysis

### Fact Table
- **fact_transactions**: Sales transactions (2,823 records)

### Sample Query
```sql
-- Monthly revenue by product line
SELECT 
    d.year,
    d.month_name,
    p.product_line,
    SUM(t.total_sales) as revenue
FROM fact_transactions t
JOIN dim_products p ON t.product_code = p.product_code
JOIN dim_dates d ON t.order_date = d.order_date
GROUP BY d.year, d.month_name, p.product_line
ORDER BY d.year, d.month, revenue DESC;
```

---

## 📈 Key Insights

### Customer Segmentation
- **High Value**: 870 orders (31%)
- **Medium Value**: 1,840 orders (65%)
- **Low Value**: 113 orders (4%)

### Geographic Distribution
- **EMEA**: Europe/Middle East/Africa
- **APAC**: Asia Pacific
- **NA**: North America

### Data Quality
- **0** missing critical values
- **81** sales outliers detected (2.9%)
- **707** high-value orders flagged (25%)

---

## 🧪 Testing

Run comprehensive test suite:
```bash
python scripts/test_pipeline.py
```

**Tests include:**
- ✅ File existence validation
- ✅ Data quality checks
- ✅ Database connectivity
- ✅ Report generation
- ✅ Row count verification

---

## 🛡️ Data Quality Checks

The pipeline implements multiple validation layers:

1. **Schema Validation**: Column names, data types
2. **Business Rules**: Negative prices, zero sales detection
3. **Anomaly Detection**: Statistical outliers (IQR method)
4. **Referential Integrity**: Foreign key constraints
5. **Completeness**: Missing value analysis

---

## 🔧 Technology Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.9+ |
| **Database** | PostgreSQL 13+ |
| **Data Processing** | Pandas, NumPy |
| **Database ORM** | SQLAlchemy, psycopg2 |
| **Configuration** | python-dotenv |
| **Reports** | openpyxl, xlsxwriter |
| **Version Control** | Git |

---

## 📦 Dependencies

See [`requirements.txt`](requirements.txt) for complete list:
- pandas>=2.0.0
- sqlalchemy>=2.0.0
- psycopg2-binary>=2.9.0
- python-dotenv>=1.0.0
- openpyxl>=3.1.0

---

## 🗺️ Roadmap

### Phase 1: Core ETL ✅
- [x] Data extraction
- [x] Transformation pipeline
- [x] Database loading
- [x] Report generation

### Phase 2: Enhancement (Future)
- [ ] Add data visualization dashboards
- [ ] Implement incremental loads
- [ ] Add REST API endpoints
- [ ] Schedule automated runs (cron/Airflow)
- [ ] Add unit tests (pytest)
- [ ] Containerization (Docker)

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- Dataset: Sales transaction data (2003-2005)
- Tools: Python, PostgreSQL, Pandas
- Inspiration: Real-world data engineering best practices

---

## 📞 Support

For questions or issues:
1. Check existing [Issues](https://github.com/yourusername/sales_project/issues)
2. Create a new issue with detailed description
3. Contact via email

---

**⭐ If you find this project helpful, please give it a star!**

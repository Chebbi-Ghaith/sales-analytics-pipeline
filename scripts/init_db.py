# filepath: c:\Users\ghait\Desktop\sales_project\scripts\init_db.py
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def init_database():
    """Initialize database schema"""
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    cursor = conn.cursor()
    
    # Read and execute schema
    with open('../sql/schema.sql', 'r') as f:
        cursor.execute(f.read())
    
    conn.commit()
    cursor.close()
    conn.close()
    print("✓ Database schema initialized")

if __name__ == "__main__":
    init_database()
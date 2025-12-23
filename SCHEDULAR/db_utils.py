# db_utils.py
import mysql.connector
from config import DB_CONFIG

def get_all_tables():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return tables

def fetch_table_data(table):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM `{table}`")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

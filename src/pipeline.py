import duckdb
import pandas as pd
import os
from datetime import datetime
import uuid

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "warehouse", "hr_analytics.duckdb")


def get_connection():
    return duckdb.connect(DB_PATH)


def generate_lineage_id():
    return f"hr_pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}"


def load_csv(file_path):
    df = pd.read_csv(file_path)
    return df


def process_data(df, file_name):
    # Convert hire_date to proper format
    df["hire_date"] = pd.to_datetime(df["hire_date"], dayfirst=True)

    # Convert timestamp column properly
    df["source_updated_timestamp"] = pd.to_datetime(df["source_updated_timestamp"], dayfirst=True)
    
    # Add metadata columns
    df["ingestion_timestamp"] = datetime.now()
    df["file_id"] = file_name
    df["lineage_id"] = generate_lineage_id()

    return df


def insert_raw_history(conn, df):
    conn.execute("INSERT INTO employee_raw_history SELECT * FROM df")


def upsert_current(conn, df):
    conn.execute("""
        CREATE OR REPLACE TEMP TABLE staging AS SELECT * FROM df
    """)

    conn.execute("""
        INSERT INTO employee_current
        SELECT 
            employee_id,
            first_name,
            last_name,
            gender,
            department,
            salary,
            location,
            performance_score,
            hire_date,
            employee_status,
            CURRENT_TIMESTAMP,
            source_updated_timestamp,
            file_id,
            lineage_id
        FROM staging
        ON CONFLICT (employee_id) DO UPDATE SET
            first_name = excluded.first_name,
            last_name = excluded.last_name,
            gender = excluded.gender,
            department = excluded.department,
            salary = excluded.salary,
            location = excluded.location,
            performance_score = excluded.performance_score,
            employee_status = excluded.employee_status,
            last_updated_timestamp = excluded.last_updated_timestamp,
            file_id = excluded.file_id,
            lineage_id = excluded.lineage_id;
    """)


def run_pipeline(file_path):
    conn = get_connection()

    print("Loading CSV...")
    df = load_csv(file_path)

    print("Processing data...")
    df = process_data(df, os.path.basename(file_path))

    print("Inserting into raw history...")
    insert_raw_history(conn, df)

    print("Upserting into current table...")
    upsert_current(conn, df)

    print("Pipeline run complete.")

    conn.close()


if __name__ == "__main__":
    file_path = os.path.join(BASE_DIR, "data", "employee_day1.csv")
    run_pipeline(file_path)
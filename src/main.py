import duckdb
import os

DB_PATH = "data/warehouse/hr_analytics.duckdb"
SCHEMA_FILE = "sql/create_schema.sql"


def initialize_database():
    os.makedirs("data/warehouse", exist_ok=True)

    print("Connecting to DuckDB...")
    conn = duckdb.connect(DB_PATH)

    print("Executing schema...")
    with open(SCHEMA_FILE, "r") as f:
        schema_sql = f.read()
        conn.execute(schema_sql)

    print("Schema initialized successfully.")

    conn.close()


if __name__ == "__main__":
    initialize_database()

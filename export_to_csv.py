import psycopg2
import csv
import os

DB_CONFIG = {
    "host": "172.31.0.1",
    "database": "market_pipeline",
    "user": "postgres",
    "password": os.getenv("DB_PASSWORD")
}

# Naya folder banao agar exist nahi karta
OUTPUT_FOLDER = "spark_export"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def export_table_to_csv(table_name, output_filename):
    """Ek table ka poora data CSV file mein likh deta hai."""
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    # column names nikalo header ke liye
    column_names = [desc[0] for desc in cursor.description]

    filepath = os.path.join(OUTPUT_FOLDER, output_filename)
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(column_names)   # header row
        writer.writerows(rows)          # actual data

    print(f"Exported {len(rows)} rows from '{table_name}' to '{filepath}'")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    export_table_to_csv("raw_prices", "raw_prices.csv")
    export_table_to_csv("daily_summary", "daily_summary.csv")
    print("Export complete. Check the 'spark_export' folder.")
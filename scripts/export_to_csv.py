import sqlite3
import csv

conn = sqlite3.connect("price_tracker.db")
cursor = conn.cursor()

cursor.execute("""
    SELECT
        retailers.name AS retailer,
        products.name AS product_name,
        products.brand,
        products.unit_weight_text,
        price_entries.price,
        price_entries.currency,
        price_entries.was_promo,
        price_entries.discount_percent,
        price_entries.observed_at
    FROM price_entries
    JOIN products ON price_entries.product_id = products.id
    JOIN retailers ON products.retailer_id = retailers.id
    ORDER BY retailers.name, products.name, price_entries.observed_at
""")

rows = cursor.fetchall()
column_names = [description[0] for description in cursor.description]

with open("price_tracker_export.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(column_names)
    writer.writerows(rows)

print(f"Exported {len(rows)} rows to price_tracker_export.csv")

conn.close()
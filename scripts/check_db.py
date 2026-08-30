import sqlite3

conn = sqlite3.connect("price_tracker.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM price_entries")
count = cursor.fetchone()[0]
print(f"Total price_entries rows: {count}")

cursor.execute("""
    SELECT products.name, price_entries.price, price_entries.currency, price_entries.observed_at
    FROM price_entries
    JOIN products ON price_entries.product_id = products.id
    LIMIT 5
""")
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()
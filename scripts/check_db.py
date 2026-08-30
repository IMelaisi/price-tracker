import sqlite3

conn = sqlite3.connect("price_tracker.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM price_entries")
count = cursor.fetchone()[0]
print(f"Total price_entries rows: {count}")

cursor.execute("""
    SELECT retailers.name, COUNT(*)
    FROM price_entries
    JOIN products ON price_entries.product_id = products.id
    JOIN retailers ON products.retailer_id = retailers.id
    GROUP BY retailers.name
""")
rows = cursor.fetchall()
for row in rows:
    print(row)

cursor.execute("""
    SELECT retailers.name, products.name, price_entries.price, price_entries.currency
    FROM price_entries
    JOIN products ON price_entries.product_id = products.id
    JOIN retailers ON products.retailer_id = retailers.id
    WHERE retailers.name = 'mr_bricolage'
    LIMIT 3
""")
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()
import psycopg2

conn = psycopg2.connect("dbname=website_db user=maxx")
cur = conn.cursor()
cur.execute("""SELECT name FROM products WHERE (name = '3') """)
z = cur.fetchall()
print(bool(z))
for x in cur.fetchall():
    print(x)
conn.commit()
cur.close()
conn.close()

import psycopg2 as psql

import config as cfg

conn = psql.connect(dbname=cfg.DATABASE_NAME, port=cfg.DB_PORT, host=cfg.DB_HOST,
                    user=cfg.DB_USER, password=cfg.DB_PASSWORD)

with conn.cursor() as cur:
    try:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS books(
        id SERIAL PRIMARY KEY,
        title VARCHAR(200)
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS pages(
        id SERIAL PRIMARY KEY,
        content text,
        book_id INTEGER REFERENCES books (id) ON DELETE RESTRICT
        )""")
        conn.commit()
        print('Tables created successfully')
    except:
        print('Error')




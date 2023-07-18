import psycopg2 as psql

import config as cfg

conn = psql.connect(dbname=cfg.DATABASE_NAME, port=cfg.DB_PORT, host=cfg.DB_HOST,
                    user=cfg.DB_USER, password=cfg.DB_PASSWORD)


# Checks if the book in table already
def _already_in_table(title):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT * FROM books WHERE title = %s
        """, (title, ))
        return cur.fetchone()


# Adds book to the table, raise exception if it in already
def add_book(title):
    if not _already_in_table(title):
        with conn.cursor() as cur:
            cur.execute("""
            INSERT INTO books (title) 
            VALUES (%(title)s)
            """,
                        {'title': title})
            conn.commit()
            print('Book added successfully')
    else:
        print('Book already in table')


# Adds book pages
def add_pages(content, book_id):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO pages (content, book_id) VALUES (%(content)s, %(book_id)s)
        """, {'content': content, 'book_id': book_id})
        conn.commit()
        print('Page(s) successfully added')


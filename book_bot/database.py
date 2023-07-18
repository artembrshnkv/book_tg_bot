import psycopg2 as psql

import config as cfg

conn = psql.connect(dbname=cfg.DATABASE_NAME, port=cfg.DB_PORT, host=cfg.DB_HOST,
                    user=cfg.DB_USER, password=cfg.DB_PASSWORD)


# # Checks if the book in table already
# def _already_in_table(title):
#     with conn.cursor() as cur:
#         cur.execute("""
#         SELECT * FROM books WHERE title = %s
#         """, (title, ))
#         return cur.fetchone()
#
#
# # Gets book id by title
# def gget_book_id_by_title(title):
#     try:
#         with conn.cursor() as cur:
#             cur.execute("""
#             SELECT * FROM books WHERE title = %s
#             """, (title, ))
#             return cur.fetchone()[0]
#     except:
#         print('No books with this title')


def select_book(title, already_in_table=False, get_book_id_by_title=False):
    """Select book from books table.
     If already_in_book = True returns boolean if book in table.
     If get_book_id_by_title = True returns book id.
     If both False or both True returns None
     """
    try:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT * FROM books WHERE title = %s 
            """, (title,))
            if already_in_table and get_book_id_by_title or \
                    not already_in_table and not get_book_id_by_title:
                return None
            elif already_in_table:
                return bool(cur.fetchone())
            elif get_book_id_by_title:
                return cur.fetchone()[0]
    except:
        print('No book with this title')


#
def add_book(title):
    """Adds book to the table, raise exception if it in already"""
    if not select_book(title, already_in_table=True):
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


#
def add_pages(content, book_id):
    """Adds book pages"""
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO pages (content, book_id) VALUES (%(content)s, %(book_id)s)
        """, {'content': content, 'book_id': book_id})
        conn.commit()
        print('Page(s) successfully added')

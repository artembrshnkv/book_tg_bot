import psycopg2 as psql

import config as cfg

conn = psql.connect(dbname=cfg.DATABASE_NAME, port=cfg.DB_PORT, host=cfg.DB_HOST,
                    user=cfg.DB_USER, password=cfg.DB_PASSWORD)



def select_book(title, already_in_table=False, get_book_id_by_title=False):
    """Select book from books table.
     If already_in_table = True returns boolean if book in table.
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


def add_book(title):
    """Adds book to the table, raise exception if its in already"""
    message = ''
    if not select_book(title, already_in_table=True):
        with conn.cursor() as cur:
            cur.execute("""
            INSERT INTO books (title) 
            VALUES (%(title)s)
            """,
                        {'title': title})
            conn.commit()
            print('Book added successfully')
            message = 'Book added successfully'
    else:
        print('Book already in table')
        message = 'Book already in table'


def add_pages(page_number, content, book_id):
    """Adds book pages"""
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO pages (page_number, content, book_id) VALUES (%(page_number)s, %(content)s, %(book_id)s)
        """, {'page_number': page_number, 'content': content, 'book_id': book_id})
        conn.commit()
        print('Page(s) successfully added')


def add_user(state, user_tg_id):
    """Adds users to the table by fsm registration data"""
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO users (first_name, second_name, email, wish_news, tg_id)
        VALUES (%(first_name)s, %(second_name)s, %(email)s, %(wish_news)s, %(tg_id)s)
        """, {'first_name': state['first_name'],
              'second_name': state['last_name'],
              'email': state['email'],
              'wish_news': state['wish_news'],
              'tg_id': user_tg_id
              }
                    )
        conn.commit()


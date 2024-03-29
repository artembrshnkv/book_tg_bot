import psycopg2 as psql

import config as cfg

conn = psql.connect(dbname=cfg.DATABASE_NAME, port=cfg.DB_PORT, host=cfg.DB_HOST,
                    user=cfg.DB_USER, password=cfg.DB_PASSWORD)


# with conn.cursor() as cur:
#     cur.execute("""
#     DROP TABLE IF EXISTS users_books_pages
#     """)
#     conn.commit()

#
# with conn.cursor() as cur:
#     cur.execute("""
#     CREATE TABLE IF NOT EXISTS users_books_pages(
#     user_tg_id INTEGER REFERENCES users(tg_id),
#     book_id INTEGER,
#     page_number INTEGER NOT NULL,
#     FOREIGN KEY (book_id, page_number) REFERENCES pages(book_id, page_number),
#     PRIMARY KEY (user_tg_id, book_id)
#     )
#     """)
#     conn.commit()


def select_book(title, already_in_table=False, get_book_id_by_title=False):
    """
    Select book from books table.
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
    except():
        print('No book with this title')


def add_book(title):
    """Adds book to the table, raise exception if its in already"""
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


def add_pages(page_number, content, book_id):
    """Adds book pages"""
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO pages (page_number, content, book_id) VALUES (%(page_number)s, %(content)s, %(book_id)s)
        """, {'page_number': page_number, 'content': content, 'book_id': book_id})
        conn.commit()
        print('Page(s) successfully added')


def add_user(data, user_tg_id):
    """Adds users to the table by fsm registration data"""
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO users (first_name, second_name, email, wish_news, tg_id)
        VALUES (%(first_name)s, %(second_name)s, %(email)s, %(wish_news)s, %(tg_id)s)
        """, {'first_name': data['first_name'],
              'second_name': data['last_name'],
              'email': data['email'],
              'wish_news': data['wish_news'],
              'tg_id': user_tg_id
              }
                    )
        conn.commit()


def user_is_registered(user_tg_id):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT * FROM users
        WHERE tg_id = %(user_tg_id)s
        """, {'user_tg_id': user_tg_id}
                    )
        return bool(cur.fetchone())


def get_books():
    """Get all books from table"""
    with conn.cursor() as cur:
        cur.execute("""
        SELECT * FROM books;
        """)
        return cur.fetchall()


def _select_actual_page(user_tg_id, book_id):
    """
    Selects actual page of books that user read.
    Works only if required row already in table users_books_pages.
    Only for in module use.
    """
    with conn.cursor() as cur:
        cur.execute("""
        SELECT (page_number) FROM users_books_pages
        WHERE (user_tg_id = %(user_tg_id)s and book_id = %(book_id)s)
        """, {'user_tg_id': user_tg_id,
              'book_id': book_id,
              }
                    )
        return cur.fetchone()
        # if cur.fetchone()[0] and cur.fetchone() is not None:
        #     return cur.fetchone()[0]


def chose_books_page(user_tg_id, book_id):
    """
    Selects actual page of book that user read.
    Creates row if it is not in table yet.
    """
    with conn.cursor() as cur:
        page = _select_actual_page(user_tg_id=user_tg_id, book_id=book_id)
        if page is not None:
            return page[0]
        else:
            cur.execute("""
            INSERT INTO users_books_pages(user_tg_id, book_id, page_number)
            VALUES (%(user_tg_id)s, %(book_id)s, %(page_number)s)
            """, {'user_tg_id': user_tg_id,
                  'book_id': book_id,
                  'page_number': 1
                  }
                        )
            conn.commit()
            return _select_actual_page(user_tg_id=user_tg_id, book_id=book_id)[0]

    # try:
        #     cur.execute("""
        #     SELECT (page_number) FROM users_books_pages
        #     WHERE (user_tg_id = %(user_tg_id)s and book_id = %(book_id)s)
        #     """, {'user_tg_id': user_tg_id,
        #           'book_id': book_id,
        #           }
        #                 )
        # except():
        #     cur.execute("""
        #     INSERT INTO users_books_pages(user_tg_id, book_id, page_number)
        #     VALUES (%(user_tg_id)s, %(book_id)s, %(page_number)s)
        #     """, {'user_tg_id': user_tg_id,
        #           'book_id': book_id,
        #           'page_number': 1
        #           }
        #                 )
        #     conn.commit()
        # finally:
        #     cur.execute("""
        #     SELECT (page_number) FROM users_books_pages
        #     WHERE (user_tg_id = %(user_tg_id)s and book_id = %(book_id)s)
        #     """, {'user_tg_id': user_tg_id,
        #           'book_id': book_id,
        #           }
        #     )
        # return cur.fetchone()[0]


def get_actual_page_content(book_id, page_number):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT content FROM pages 
        WHERE (book_id = %(book_id)s and page_number = %(page_number)s)
        """, {'book_id': book_id,
              'page_number': page_number
              }
                    )
        return cur.fetchone()[0]


def update_actual_page_number(user_tg_id, book_id, page_number):
    with conn.cursor() as cur:
        cur.execute("""
        UPDATE users_books_pages
        SET page_number = %(page_number)s
        WHERE (user_tg_id = %(user_tg_id)s and book_id = %(book_id)s)
        """, {'user_tg_id': user_tg_id,
              'book_id': book_id,
              'page_number': page_number
              }
                    )
        conn.commit()


def get_min_max_page_number(book_id, get_max_page=False, get_min_page=False):
    if get_max_page and get_min_page or \
            not get_max_page and not get_min_page:
        return None
    try:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT page_number
            FROM pages
            WHERE book_id = %(book_id)s
            """, {'book_id': book_id}
                        )
            if get_max_page:
                return cur.fetchall()[-1][0]
            elif get_min_page:
                return cur.fetchall()[0][0]
    except():
        return None


def get_page_numbers_for_menu(book_id, page_number, thresholds):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT page_number FROM pages
        WHERE (book_id = %(book_id)s and %(lower_threshold)s < page_number and page_number < %(upper_threshold)s)
        """, {'book_id': book_id,
              'page_number': page_number,
              'lower_threshold': thresholds['lower_threshold'],
              'upper_threshold': thresholds['upper_threshold']}
                    )
        return [n[0] for n in cur.fetchall()]


def get_my_books(user_tg_id):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT title, page_number FROM users_books_pages
        JOIN books ON books.id = users_books_pages.book_id
        WHERE users_books_pages.user_tg_id = %(user_tg_id)s 
        """, {'user_tg_id': user_tg_id}
                    )
        return cur.fetchall()


if __name__ == '__main__':
    print(get_my_books(user_tg_id=890681558))
    # print(chose_books_page(user_tg_id=890681558, book_id=13))
    # print(_select_actual_page(user_tg_id=890681558, book_id=11))
    # print(chose_books_page(user_tg_id=890681558, book_id=11))
    # add_book(title="Тарас Бульба")
    # print(user_is_registered(user_tg_id=890681551))

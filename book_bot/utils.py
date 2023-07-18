import config as cfg
import database as db

file = 'books/Над_пропасть_во_ржи.pdf'
book_title = file[6:-4]
punctuation_marks = ('.', ',', '!', '?', ':', ';')

print(type(db.select_book(book_title, already_in_table=True)))


# def get_pages():
#     with open(file, 'r') as f:
#         while f >= cfg.PAGE_SIZE:
#             print(f.tell())



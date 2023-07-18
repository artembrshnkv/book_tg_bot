import config as cfg
import database as db

file = 'books/Над_пропасть_во_ржи.pdf'
punctuation_marks = ('.', ',', '!', '?', ':', ';')


db.add_book(file[6:-4])

# def get_parts():
#     with open(file, 'r') as f:
#         while f >= cfg.PAGE_SIZE:
#             print(f.tell())




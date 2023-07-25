import database as db

file_path = 'books/Над_пропасть_во_ржи.txt'
# book_title = file_path[6:-4]
punctuation_marks = ('.', ',', '!', '?', ':', ';')

# with open(file, 'r', encoding='utf-8') as f:
#     page_size = 1000
#     read_file = f.read()
#     start_index = 0
#     total_len = 0
#     count = 1
#     while total_len != len(read_file):
#         try:
#             read_file[start_index + page_size]
#         except IndexError:
#             read_file = read_file[start_index:]
#
#         while read_file[start_index+page_size] not in punctuation_marks or not read_file[start_index+page_size]:
#             page_size -= 1
#         print(f'{count}.' + read_file[start_index:start_index+page_size+1] + '\n\n')
#         total_len += len(read_file[start_index:start_index+page_size+1])
#         count += 1
#         start_index += page_size+1
#         page_size = 1000


def get_pages(file, max_page_size, book_title):
    if not db.select_book(title=book_title, already_in_table=True):
        with open(file, 'r', encoding='utf-8') as f:
            page_size = max_page_size
            read_file = f.read()
            start_index = 0
            total_len = 0
            page_number = 1
            while total_len != len(read_file):
                try:
                    while read_file[start_index + page_size] not in punctuation_marks:
                        page_size -= 1
                        content = read_file[start_index:start_index + page_size + 1]
                    # print(f'{page_number}.' + content + '\n\n')
                    if not db.select_book(title=book_title, already_in_table=True):
                        db.add_pages(page_number=page_number, content=content,
                                     book_id=db.select_book(title=book_title, get_book_id_by_title=True))
                    else:
                        print('book already in table')
                    total_len += len(read_file[start_index:start_index + page_size + 1])
                    page_number += 1
                    start_index += page_size + 1
                    page_size = max_page_size

                except IndexError:
                    print(f'{page_number}.' + read_file[start_index:])
                    break

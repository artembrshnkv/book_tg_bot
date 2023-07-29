import database as db

import os

file_path = 'books/Над_пропасть_во_ржи.txt'
punctuation_marks = ('.', ',', '!', '?', ':', ';')


def get_pages(file, max_page_size, book_title):
    # if not db.select_book(title=book_title, already_in_table=True):
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
                    db.add_pages(page_number=page_number, content=content,
                                 book_id=db.select_book(title=book_title, get_book_id_by_title=True))
                    total_len += len(read_file[start_index:start_index + page_size + 1])
                    page_number += 1
                    start_index += page_size + 1
                    page_size = max_page_size

                except IndexError:
                    # print(f'{page_number}.' + read_file[start_index:])
                    db.add_pages(page_number=page_number, content=read_file[start_index:],
                                 book_id=db.select_book(title=book_title, get_book_id_by_title=True))
                    break



if __name__ == '__main__':
    print(get_pages(file=file_path, max_page_size=1000, book_title="Над пропастью во ржи"))

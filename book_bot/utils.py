import database as db

file_path = 'books/Над_пропасть_во_ржи.txt'
punctuation_marks = ('.', ',', '!', '?', ':', ';')


def get_correct_page_range(book_id, page_number):
    if db.get_min_max_page_number(book_id=book_id, get_min_page=True) < page_number < \
            db.get_min_max_page_number(book_id=book_id, get_max_page=True):
        return page_number
    else:
        return min(db.get_min_max_page_number(book_id=book_id, get_max_page=True),
                   max(db.get_min_max_page_number(book_id=book_id, get_min_page=True), page_number))
    # return db.get_min_page_number(book_id=book_id) < page_number < db.get_max_page_number(book_id=book_id)


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
    print(get_correct_page_range(book_id=10, page_number=43))

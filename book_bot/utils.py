import copy

file = 'books/Над_пропасть_во_ржи.txt'
book_title = file[6:-4]
punctuation_marks = ('.', ',', '!', '?', ':', ';')
copied_file = copy.deepcopy(file)


def get_char(size):
    with open(file, 'r',  encoding='utf-8') as f:
        read_file = f.read()
        copied_size = copy.deepcopy(size)
        start = 0
        while True:
            if read_file[start:copied_size+1][copied_size] not in punctuation_marks:
                copied_size -= 1
            else:
                print(read_file[start:copied_size+1])
                start += copied_size+1

        print(size)


get_char(1100)


# size = 1100
# with open(file, 'r', encoding='utf-8') as f:
#     read_file = f.read()
#     copied_size = copy.deepcopy(size)
#     start = 0
#     while size <= len(read_file):
#         if read_file[start+copied_size] not in punctuation_marks:
#             copied_size -= 1
#         else:
#             print(read_file[start:copied_size+1])
#             start += copied_size
#             read_file = read_file[start:]
#     print(size)


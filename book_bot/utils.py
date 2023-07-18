import config as cfg

file = 'books/selindzher-d.-d.-nad-propastyu-vo-rzhi-getlib.ru.pdf'
punctuation_marks = ('.', ',', '!', '?', ':', ';')


def get_parts():
    with open(file, 'r') as f:
        while f >= cfg.PAGE_SIZE:
            print(f.tell())


get_parts()


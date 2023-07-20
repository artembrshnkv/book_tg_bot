from aiogram.filters import BaseFilter


class IsNameOrSurname(BaseFilter):
    def __init__(self, name):
        self.name = name

    def __call__(self):
        return 2 < len(self.name) < 30 and self.name.isalpha()


from aiogram.filters import BaseFilter

import config as cfg


class IsNameOrSurname(BaseFilter):
    def __init__(self, name):
        self.name = name

    def __call__(self):
        return 2 < len(self.name) < 30 and self.name.isalpha()


class IsAdmin(BaseFilter):
    def __init__(self, user_id):
        self.user_id = user_id

    def __call__(self):
        return self.user_id in cfg.ADMINS_ID_LIST

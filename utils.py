from aiogram.utils.helper import Helper, HelperMode, ListItem



class States(Helper):
    mode = HelperMode.snake_case

    STATE_MENU = ListItem()
    STATE_NEW_WORD = ListItem()
    STATE_PICK_WORD = ListItem()
    STATE_STATISTIC = ListItem()
    STATE_CHAT = ListItem()


if __name__ == '__main__':
    print(States.all())
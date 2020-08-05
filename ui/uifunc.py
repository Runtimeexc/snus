import fastdb
from classes import Position


def format_text_tocatpos(pos: Position, opis: bool):
    text = f'{pos.name}\n' \
           f'Цена за единицу: {pos.cost}₽'
    if opis:
        text += '\n' + pos.definition
    return text

def get_settings_text():
    text = "1. Цена доставки: " + fastdb.DOSTAVKA_COST
    text += "\n2. Накопление баллов: " + fastdb.BONUS_PERCENT + '%'


import dbfunc
from aiogram import types
from classes import Position


CURRENT_RED_POSITION = Position
CURRENT_RED_POSITION_OLDNAME = str
# ☻



def get_pos_for_mark(string: str):
    result = []
    for pos in POSITIONS:
        if pos.fsection == string:
            result.append(pos)
    return result


def get_position_names():
    list_names = []
    for position in POSITIONS:
        list_names.append(position.name)
    return list_names


def refresh_position_sections():
    global SECTIONS
    global POSITIONS
    print('ref sections')
    for position in POSITIONS:
        isad = True
        for section in SECTIONS:
            if position.section == section:
                print(position.section+' - повтор, отмена')
                isad = False
        if isad:
            print(position.section + " + обновлено")
            SECTIONS.append(position.section)


def refresh_position_brands():
    global BRANDS
    global POSITIONS
    print("ref brands")
    for position in POSITIONS:
        isad = True
        for brand in BRANDS:
            if position.fsection == brand:
                print(position.fsection + ' - повтор, отмена')
                isad = False
        if isad:
            print(position.fsection + " + обновлено")
            BRANDS.append(position.fsection)



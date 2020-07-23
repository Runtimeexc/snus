import dbfunc
from classes import Position, CatalogBuf

# 777027968
# 244432423 Паша
# 538011007 Колян
ALL_ADMINS = [777027968]

ALL_POSITIONS = []
ALL_SECTIONS = []
ALL_FSECTIONS = []
CATALOG_BUFFER = CatalogBuf()
DOSTAVKA_COST = 200

##############
# refreshers #
##############
def refresh_all_fastdb():
    refresh_positions()
    refresh_sections()
    refresh_fsections()
    CATALOG_BUFFER.refresh(ALL_FSECTIONS, ALL_POSITIONS)

def refresh_positions():
    global ALL_POSITIONS
    ALL_POSITIONS = []
    for str in dbfunc.get_positions():
        ALL_POSITIONS.append(Position(str[0], str[2], str[1], str[3], str[4], str[6], str[5]))

def refresh_sections():
    global ALL_POSITIONS
    global ALL_SECTIONS
    ALL_SECTIONS = []
    for pos in ALL_POSITIONS:
        isad = True
        for section in ALL_SECTIONS:
            if pos.section == section:
                isad = False
        if isad:
            ALL_SECTIONS.append(pos.section)

def refresh_fsections():
    global ALL_POSITIONS
    global ALL_FSECTIONS
    ALL_FSECTIONS = []
    for pos in ALL_POSITIONS:
        isad = True
        for fsection in ALL_FSECTIONS:
            if pos.fsection == fsection:
                isad = False
        if isad:
            ALL_FSECTIONS.append(pos.fsection)


def is_admin(tid: int):
    return tid in ALL_ADMINS


def is_section(section: str):
    return section in ALL_SECTIONS


def is_fsection(fsection: str):
    return fsection in ALL_FSECTIONS



##############
# getters    #
##############
def get_colcost_sklad():
    colsklad = 0
    costsklad = 0
    for pos in ALL_POSITIONS:
        colsklad += pos.col
        costsklad += pos.col * pos.cost
    return [colsklad, costsklad]


def get_fsections_from_section(section: str):
    notsort_fsections = []
    for pos in ALL_POSITIONS:
        if pos.section == section:
            notsort_fsections.append(pos.fsection)
    print(notsort_fsections)
    print([set(notsort_fsections)])
    return set(notsort_fsections)


def get_adminposliststr():
    iter = 0
    text = ''
    for position in ALL_POSITIONS:
        iter += 1
        text += str(iter) + '. ' + position.name + '\n'

    print(text)
    return text

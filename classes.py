

class Position:
    name = ''
    cost = 0
    col = 0
    section = ''
    fsection = ''
    cap = ''
    definition = ''

    def __init__(self, name, cost, col, section, brand, cap, definition):
        self.name = name
        self.cost = cost
        self.col = col
        self.section = section
        self.fsection = brand
        self.cap = cap
        self.definition = definition

class PossInBrand:
    brand = str
    lst = []

    def __init__(self, brand, poslst):
        self.brand = brand
        self.lst = poslst

class CatalogBuf:
    pos_for_brand = []

    def refresh(self, fseclist, postlist):
        self.pos_for_brand = []
        for fsection in fseclist:
            poslist = []
            for pos in postlist:
                if pos.fsection == fsection:
                    poslist.append(pos)
            self.pos_for_brand.append(PossInBrand(fsection, poslist))

    def get_next_pos(self, fsection: str, step: int):
        print('get next pos')
        for pib in self.pos_for_brand:
            if pib.brand == fsection:
                return pib.lst[step+1]

    def get_undo_pos(self, fsection: str, step: int):
        for pib in self.pos_for_brand:
            if pib.brand == fsection:
                return pib.lst[step-1]

    def get_pos(self, fsection: str, step: int):
        for pib in self.pos_for_brand:
            if pib.brand == fsection:
                return pib.lst[step]

    def get_colpos_from_fsection(self, fsection: str):
        for pib in self.pos_for_brand:
            if pib.brand == fsection:
                return len(pib.lst)-1
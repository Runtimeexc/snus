import dbfunc


def send_card(uid: int):
    data = dbfunc.get_card(uid)
    mes_text = 'Корзина\n=========\n'
    iter = 0
    for card_pos in data:
        iter +=1
        # mes_text += f'{str(iter)}. {card_pos[1]} {card_pos[2]}шт. ({}р.) '

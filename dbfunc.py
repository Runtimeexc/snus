import pymysql

import fastdb
from classes import Position


def connect_db():
    return pymysql.connect('45.12.19.144', 'admin_admin',
    'lJ3XsEzv6c', 'admin_dsb_db')


def get_positions():
    print("FUNC: get_positions###########################")
    con = connect_db()
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM position")
        rows = cur.fetchall()
    print(rows)
    return rows


def get_users():
    con = connect_db()
    with con:
        cur = con.cursor("SELECT * FROM user")
        cur.execute()
        rows = cur.fetchall()
    return rows


def get_sotrudnik():
    con = connect_db()
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM sotrudnik ")
        rows = cur.fetchall()
    return rows

# def add_user():
# def add_sotrudnik():

def add_user(uid, name, fullname, bonus, tel):
    con = connect_db()
    with con:
        sqlin = ''
        sqlin += "INSERT INTO " + "user "
        sqlin += "(useruid, " \
               "username, " \
               "userfullname, " \
               "userbonus, " \
               "usertelnum) "
        sqlin += f"VALUES ({str(uid)}, \'{name}\', \'{fullname}\', {str(bonus)}, \'{tel}\')"
        print(sqlin)
        cur = con.cursor()
        cur.execute(sqlin)
        con.commit()

def is_new_user(uid: str):
    con = connect_db()
    with con:
        sqlin = "SELECT * FROM user "
        sqlin += "WHERE useruid = " + uid + ";"
        print(sqlin)
        cur = con.cursor(sqlin)
        cur.execute()
        rows = cur.fetchall()
    return bool(rows)

def edit_user_tel(uid, tel):
    con = connect_db()
    with con:
        sqlin = ''
        sqlin += "UPDATE " + "user " + "SET "
        sqlin += "usertelnum=\'" + tel + "\' "
        sqlin += "WHERE useruid = " + str(uid) + ";"
        print(sqlin)
        cur = con.cursor()
        cur.execute(sqlin)
        con.commit()

def is_usertel_added(uid: int):
    con = connect_db()
    with con:
        sqlin = "SELECT * FROM user "
        sqlin += "WHERE useruid = " + str(uid) + ";"
        print(sqlin)
        cur = con.cursor()
        cur.execute(sqlin)
        rows = cur.fetchall()
        print(rows)
        if rows[0][5] != '0':
            return True
        else:
            return False
    return bool(rows)

def edit_user_bonus(uid, bonus):
    con = connect_db()
    with con:
        sqlin = ''
        sqlin += "UPDATE " + "user " + "SET "
        sqlin += "userbonus=" + bonus + " "
        sqlin += "WHERE useruid = " + uid + ";"
        print(sqlin)
        cur = con.cursor()
        cur.execute(sqlin)
        con.commit()

def get_user(uid):
    con = connect_db()
    with con:
        sqlin = 'SELECT * FROM user '
        sqlin += f"WHERE useruid={str(uid)}"
        print(sqlin)
        cur = con.cursor()
        cur.execute(sqlin)
        con.commit()
        rows = cur.fetchall()
    return rows

def add_zakaz(uid, stat, dost):
    con = connect_db()
    with con:
        sqlin = ''
        sqlin += "INSERT INTO " + "zakaz "
        sqlin += "(zakazuid, zakazstat, zakazdost) "
        sqlin += f"VALUES ({str(uid)}, \'{stat}\', \'{dost}\')"
        print(sqlin)
        cur = con.cursor()
        cur.execute(sqlin)
        con.commit()
        last_id = cur.execute('select last_insert_id() from zakaz')
        for card in get_card(uid):
            add_zakazcom(last_id, card, con)
        return last_id

def get_zakazcom(zid):
    con = connect_db()
    with con:
        sqlin = 'SELECT * FROM zakazcom '
        sqlin += f"WHERE zakazunicid={str(zid)}"
        print(sqlin)
        cur = con.cursor()
        cur.execute(sqlin)
        con.commit()
        rows = cur.fetchall()
        print(rows)
    return rows

def get_zakazcom_cost(zid):
    con = connect_db()
    with con:
        sqlin = 'SELECT * FROM zakazcom '
        sqlin += f"WHERE idzakazcom={str(zid)}"
        print(sqlin)
        cur = con.cursor()
        cur.execute(sqlin)
        con.commit()
        rows = cur.fetchall()
        cost = 0
        for zakel in rows:
            cost += int(zakel[3]) * int(zakel[4])
    return cost

def add_zakazcom(zid, card, con):
    with con:
        sqlin = ''
        sqlin += "INSERT INTO " + "zakazcom "
        sqlin += "(zakazunicid, " \
               "zakazpos, " \
               "zakazposcol, " \
               "zakazcost) "
        sqlin += f"VALUES ({str(zid)}, \'{card[2]}\', \'{card[3]}\', {card[4]})"
        print(sqlin)
        cur = con.cursor()
        cur.execute(sqlin)
        con.commit()


def get_zakaz(idz):
    con = connect_db()
    with con:
        sqlin = 'SELECT * FROM zakaz '
        sqlin += f"WHERE idzakaz={str(idz)}"
        print(sqlin)
        cur = con.cursor()
        cur.execute(sqlin)
        con.commit()
        rows = cur.fetchall()
    return rows

def get_zakaz_fromuser(uid: int):
    con = connect_db()
    with con:
        sqlin = 'SELECT * FROM zakaz '
        sqlin += f"WHERE zakazuid={str(uid)}"
        print(sqlin)
        cur = con.cursor()
        cur.execute(sqlin)
        con.commit()
        rows = cur.fetchall()
    return rows

def get_ballszakfrom_idzakaz(zid):
    balls = 0
    con = connect_db()
    with con:
        sqlin = 'SELECT * FROM zakaz '
        sqlin += f"WHERE idzakaz={str(zid)} and zakazstat='завершен'"
        print(sqlin)
        cur = con.cursor()
        cur.execute(sqlin)
        con.commit()
        rows = cur.fetchall()
        for zak in get_zakazcom(zid):
            balls += int(zak[3])*int(zak[4])
        balls = balls//100*5
    return balls

def add_position(pos: Position):
    con = connect_db()
    with con:
        sqlin = ''
        sqlin += "INSERT INTO " + "position "
        sqlin += "(positionname, " \
               "positioncol, " \
               "positioncost, " \
               "positionsection, " \
               "positionbrand, " \
               "positiondefinition, " \
               "positioncap) "
        sqlin += "VALUES (\'%s\', %s, %s, \'%s\', \'%s\', \'%s\', \'%s\')" % (pos.name, str(pos.col), str(pos.cost), pos.section, pos.fsection, pos.definition, pos.cap)
        print(sqlin)
        cur = con.cursor()
        cur.execute(sqlin)
        con.commit()
        fastdb.refresh_all_fastdb()

def add_to_card(uid, pos, col):
    con = connect_db()
    coln = col
    with con:
        sqlin = 'SELECT * FROM card '
        sqlin += f"WHERE carduid={str(uid)} AND cardposname=\'{pos.name}\'"
        cur = con.cursor()
        cur.execute(sqlin)
        rows = cur.fetchall()
        if len(rows):
            coln += int(rows[0][3])
            sqlin = ''
            sqlin += "UPDATE " + "card " + "SET "
            sqlin += "cardcolpos=" + str(coln) + ' '
            sqlin += "WHERE carduid=" + str(uid) + " and cardposname=\'"+pos.name+'\''
            print(sqlin)
            cur = con.cursor()
            cur.execute(sqlin)
            con.commit()
        else:
            sqlin = ''
            sqlin += "INSERT INTO " + "card "
            sqlin += "(carduid, " \
                     "cardposname, " \
                     "cardcolpos, " \
                     "cardcost) "
            sqlin += f"VALUES ({str(uid)},\'{pos.name}\',{str(coln)},{str(pos.cost)});"
            print(sqlin)
            cur = con.cursor()
            cur.execute(sqlin)
            con.commit()

def get_balls_fromuser(uid: int):
    con = connect_db()
    with con:
        sqlin = 'SELECT * FROM user '
        sqlin += f"WHERE useruid={str(uid)}"
        print(sqlin)
        cur = con.cursor()
        cur.execute(sqlin)
        con.commit()
        rows = cur.fetchall()
    return rows[0][4]

def get_num_fromuser(uid: int):
    con = connect_db()
    with con:
        sqlin = 'SELECT * FROM user '
        sqlin += f"WHERE useruid={str(uid)}"
        print(sqlin)
        cur = con.cursor()
        cur.execute(sqlin)
        con.commit()
        rows = cur.fetchall()
    return rows[0][5]

def get_card(uid):
    con = connect_db()
    with con:
        sqlin = 'SELECT * FROM card '
        sqlin += f"WHERE carduid={str(uid)}"
        print(sqlin)
        cur = con.cursor()
        cur.execute(sqlin)
        con.commit()
        rows = cur.fetchall()
    return rows


# uyh87yh8uhj8j8u
def red_position(pos: Position, oldname: str):
    con = connect_db()
    with con:
        sqlin = ''
        sqlin += "UPDATE " + "position " + "SET "
        sqlin += "positionname=\'" + pos.name + "\', " +\
                 "positioncol=" + str(pos.col) + ", " +\
                 "positioncost=" + str(pos.cost) + ", " +\
                 "positionsection=\'" + pos.section + "\', " +\
                 "positionbrand=\'" + pos.fsection + "\', " +\
                 "positiondefinition=\'" + pos.definition + "\', " + \
                 "positioncap=\'" + pos.cap + "\' "
        sqlin += "WHERE positionname = \'" + oldname + "\';"
        print(sqlin)
        cur = con.cursor()
        cur.execute(sqlin)
        con.commit()
        fastdb.refresh_all_fastdb()


def get_activezakazes_text(uid):
    zaklist = get_zakaz_fromuser(uid)
    mes_text = ''
    iter = 1
    cost = 0
    if len(zaklist):
        for zak in zaklist:
            cost = 0
            if str(zak[2]) != 'завершен':
                mes_text += f"№ {str(zak[0])}\nСтатус: {str(zak[2])}\nПолучение: {str(zak[3])}"
                if str(zak[3]) == "курьером": cost += fastdb.DOSTAVKA_COST
                mes_text += "\n"
                print(str(zak[0]))
                zaks = get_zakazcom(zak[0])
                iter = 0
                print(zaks)
                for line in zaks:
                    iter += 1
                    cost += int(line[3])*int(line[4])
                    mes_text +=f"{str(iter)}. {line[2]} {str(line[3])}шт.({str(int(line[3])*int(line[4]))}р.)\n"
                if str(zak[3]) == "курьером": mes_text += 'Доставка: ' + str(fastdb.DOSTAVKA_COST) + 'р.\n'
                mes_text += f"Общая стоимость: {str(cost)}"
                mes_text += f"\n============\n"
    else:
        mes_text += "Новых заказов не поступало :("
    return mes_text


def delete_position(posname: str):
    print("удаление")
    con = connect_db()
    with con:
        sqlin = 'DELETE ' + 'FROM position WHERE positionname=\'' + posname + '\';'
        print(sqlin)
        cur = con.cursor()
        cur.execute(sqlin)
        con.commit()
        fastdb.refresh_all_fastdb()
        print('позиция успешно удалена')


def delete_card(uid: int):
    print("удаление карды")
    con = connect_db()
    with con:
        sqlin = 'DELETE ' + 'FROM card WHERE carduid=' + str(uid) + ';'
        print(sqlin)
        cur = con.cursor()
        cur.execute(sqlin)
        con.commit()
        print('карта успешно удалена')
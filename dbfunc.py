import pymysql

import fastdb
import globalset
from classes import Position


def connect_db():
    return pymysql.connect('localhost', 'root',
    'Qapplication#@#Error', 'dsb_db')


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
        globalset.refresh_position_sections()


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
        globalset.refresh_position_sections()


def delete_position(posname: str):
    print("удаление")
    con = connect_db()
    with con:
        sqlin = 'DELETE ' + 'FROM position WHERE positionname=\'' + posname + '\';'
        print(sqlin)
        cur = con.cursor()
        cur.execute(sqlin)
        con.commit()
        globalset.refresh_position_sections()
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
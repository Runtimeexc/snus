from aiogram import types
from aiogram.types import ReplyKeyboardMarkup

import dbfunc
import fastdb
from ui import keyboards, strings
from handlers.allstat import MainMenu, OrderKatalog, StateAdminMenu, Card
from misc import dp
import misc


@dp.message_handler(commands=['start'], state='*')
async def cmd_start(message: types.Message):
    userinfo = dbfunc.get_user(message.from_user.id)
    is_admin = fastdb.is_admin(message.from_user.id)
    if is_admin:
        mes_text = "Привет, админ\nИнфа десериализируется, лаве инкрементируется"
    else:
        if userinfo:
            mes_text = f"Уже здоровались, {userinfo[0][2]}"
        else:
            mes_text = f"Будем знакомы, {message.from_user.first_name}"
            dbfunc.add_user(message.from_user.id, message.from_user.first_name,
                            message.from_user.full_name, 0, '0')
            print(message.from_user.id, message.from_user.first_name,
                  message.from_user.full_name, 0, '0')
    print(mes_text)
    await message.answer(mes_text, reply_markup=keyboards.get_main_menu_rkeyb(is_admin))


@dp.message_handler(lambda message: message.text == "админ панель", state='*')
async def send_admin_main_menu(message: types.Message):
    if fastdb.is_admin(message.from_user.id):
        in_sklad = fastdb.get_colcost_sklad()
        mes_text = f"Единиц на складе: {in_sklad[0]}\nНа сумму: {in_sklad[1]}"
        await message.answer(mes_text, reply_markup=keyboards.get_admin_inline_ikeyb())
        await StateAdminMenu.admin_main_menu.set()
    else:
        mes_text = "Увы, эта функция доступна только администратору :("
        await message.answer(mes_text)


@dp.message_handler(lambda message: message.text == "каталог", state='*')
async def send_catalog(message: types.Message):
    await message.answer(strings.KATALOG_SELECT_RAZDEL, reply_markup=keyboards.get_catalog_section_rkeyb())
    await OrderKatalog.waiting_katalog_section.set()


@dp.message_handler(lambda message: message.text == "корзина", state='*')
async def send_catalog(message: types.Message):
    mes_text = ''
    iter = 0
    cash = 0
    rows = dbfunc.get_card(message.from_user.id)
    if len(rows):
        for elem in rows:
            iter += 1
            cash += int(elem[3]) * int(elem[4])
            mes_text += f'{str(iter)}. {elem[2]}: {str(elem[3])}шт. ({str(int(elem[3]) * int(elem[4]))})\n'
        mes_text += f'\nОбщая сумма: {str(cash)}р.'
        await message.answer(mes_text, reply_markup=keyboards.get_card_ikeyb())
    else:
        mes_text += 'Корзина пуста'
        mes_text += f'\nОбщая сумма: {str(cash)}р.'
        await message.answer(mes_text)
    await Card.card_wait.set()


@dp.message_handler(lambda message: message.text == "акции", state='*')
async def send_catalog(message: types.Message):
    balls = dbfunc.get_balls_fromuser(message.from_user.id)
    mes_text = "5% с каждого заказа возвращается вам в виде балов!\n\n" \
               "Баллов на вашем счету: " + str(balls)
    await message.answer(mes_text)


@dp.message_handler(lambda message: message.text == "активные заказы", state='*')
async def send_zaklist(message: types.Message):
    mes_text = dbfunc.get_activezakazes_text(message.from_user.id)
    await message.answer(mes_text)


@dp.message_handler(content_types=['photo'], state='*')
async def step_getphoto(message: types.InputMediaPhoto):
    print(message.photo[0].file_id)

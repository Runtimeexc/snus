from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import dbfunc
import fastdb
import misc
from handlers.allstat import Card
from misc import dp
from ui import keyboards
from ui.keyboards import get_card_ikeyb


@dp.callback_query_handler(lambda query: query.data == 'add', state='*')
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    mes_text = "Выбери способ получения: "
    await Card.card_wait.set()
    await callback_query.message.edit_text(mes_text, reply_markup=keyboards.get_dostavka_ikeyb())


@dp.callback_query_handler(lambda query: query.data == 'clear', state='*')
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    mes_text = 'Корзина пуста'
    mes_text += f'\nОбщая сумма: 0р.'
    dbfunc.delete_card(callback_query.from_user.id)
    await callback_query.message.edit_text(mes_text)

    
@dp.callback_query_handler(lambda query: query.data == 'kura', state=Card.card_wait)
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(dostavka=True)
    if dbfunc.is_usertel_added(callback_query.from_user.id):
        mes_text = "Заказ оформлен.\nВ ближайшее время с вами свяжется оператор\n\n"
        nzak = dbfunc.add_zakaz(callback_query.from_user.id, "Ожидает подтверждения", 'курьером')
        mes_text += f"№ {str(nzak)}\nСпособ получения: курьером\nСтатус: обрабатывается\n=======\n"
        iter = 0
        cash = 0
        rows = dbfunc.get_card(callback_query.from_user.id)
        if len(rows):
            for elem in rows:
                iter += 1
                cash += int(elem[3]) * int(elem[4])
                mes_text += f'{str(iter)}. {elem[2]}: {str(elem[3])}шт. ({str(int(elem[3]) * int(elem[4]))})\n'
            cash += fastdb.DOSTAVKA_COST

        mes_text += "=======\n"
        mes_text += "Доставка: " + str(fastdb.DOSTAVKA_COST) + 'р.'
        mes_text += f"\nК оплате: {str(cash)}р."
        await callback_query.message.answer(mes_text)
        admin_text = "Номер телефона: " + str(dbfunc.get_num_fromuser(callback_query.from_user.id))
        admin_text += mes_text
        await misc.bot.send_message(chat_id=538011007, text=admin_text, reply_markup=keyboards.get_admin_zakazcontrol_ikeyb())
    else:
        mes_text = "Для подтверждения заказа понадобится ваш ваш номер телефона. Нажмите на кнопку"
        keyb = ReplyKeyboardMarkup(resize_keyboard=True)
        keyb.add(KeyboardButton("отправить мой номер", request_contact=True))
        await callback_query.message.answer(mes_text, reply_markup=keyb)
    dbfunc.delete_card(callback_query.from_user.id)



@dp.callback_query_handler(lambda query: query.data == 'samov', state=Card.card_wait)
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    if dbfunc.is_usertel_added(callback_query.from_user.id):
        await state.update_data(dostavka=False)
        mes_text = "Заказ оформлен.\nВ ближайшее время с вами свяжется оператор\n\n"
        nzak = dbfunc.add_zakaz(callback_query.from_user.id, "Ожидает подтверждения", 'самовывоз')
        mes_text += f"Номер заказа: {str(nzak)}\nСпособ получения: самовывоз\nСтатус: обрабатывается\n=======\n"
        iter = 0
        cash = 0
        rows = dbfunc.get_card(callback_query.from_user.id)
        print(rows)
        if rows:
            for elem in rows:
                iter += 1
                cash += int(elem[3]) * int(elem[4])
                mes_text += f'{str(iter)}. {elem[2]}: {str(elem[3])}шт. ({str(int(elem[3]) * int(elem[4]))})\n'
        mes_text += "=======\n"
        mes_text += f"\nК оплате: {str(cash)}р."
        await callback_query.message.edit_text(mes_text)
        admin_text = "Номер телефона: " + str(dbfunc.get_num_fromuser(callback_query.from_user.id))
        admin_text += mes_text
        await misc.bot.send_message(chat_id=538011007, text=admin_text, reply_markup=keyboards.get_admin_zakazcontrol_ikeyb())
    else:
        mes_text = "Для подтверждения заказа понадобится ваш ваш номер телефона. Нажмите на кнопку"
        keyb = ReplyKeyboardMarkup(resize_keyboard=True)
        keyb.add(KeyboardButton("отправить мой номер", request_contact=True))
        await callback_query.message.answer(mes_text, reply_markup=keyb)
    dbfunc.delete_card(callback_query.from_user.id)


@dp.message_handler(state=Card.card_wait, content_types=types.ContentTypes.CONTACT)
async def step_getcost(message: types.Message, state: FSMContext):
    number = message.contact.phone_number
    dbfunc.edit_user_tel(message.from_user.id, number)
    data = await state.get_data()
    if data['dostavka']:
        dost = "курьером"
    else: dost = "самовывоз"
    mes_text = "Заказ оформлен.\nВ ближайшее время с вами свяжется оператор\n\n"
    nzak = dbfunc.add_zakaz(message.from_user.id, "Ожидает подтверждения", dost)
    mes_text += f"Номер заказа: {str(nzak)}\nСпособ получения: {dost}\nСтатус: обрабатывается\n=======\n"
    iter = 0
    cash = 0
    rows = dbfunc.get_card(message.from_user.id)
    if len(rows):
        for elem in rows:
            iter += 1
            cash += int(elem[3]) * int(elem[4])
            mes_text += f'{str(iter)}. {elem[2]}: {str(elem[3])}шт. ({str(int(elem[3]) * int(elem[4]))})\n'
        cash += fastdb.DOSTAVKA_COST
    mes_text += "=======\n"
    mes_text += "Доставка: " + str(fastdb.DOSTAVKA_COST) + 'р.'
    mes_text += f"\nК оплате: {str(cash)}р."
    await message.answer(mes_text,
                         reply_markup=keyboards.get_main_menu_rkeyb(fastdb.is_admin(message.from_user.id)))
    admin_text = "Номер телефона: " + str(dbfunc.get_num_fromuser(message.from_user.id))
    admin_text += mes_text
    await misc.bot.send_message(chat_id=538011007, text=admin_text, reply_markup=keyboards.get_admin_zakazcontrol_ikeyb())
    dbfunc.delete_card(message.from_user.id)
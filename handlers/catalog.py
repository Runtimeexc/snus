import types
from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto

import dbfunc
import fastdb
from handlers.allstat import OrderAddPos, OrderRedPos, MainMenu, StateAdminMenu, OrderKatalog, Card
from misc import dp, bot

from aiogram.types import ReplyKeyboardMarkup

from misc import dp
from aiogram import types

from ui import keyboards, strings
from ui.uifunc import format_text_tocatpos



@dp.callback_query_handler(lambda query: query.data, state=OrderKatalog.waiting_katalog_section)
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text("выберите подраздел", reply_markup=keyboards.get_catalog_fsection_rkeyb(callback_query.data))
    await OrderKatalog.waiting_katalog_fsection.set()

@dp.callback_query_handler(lambda query: query.data, state=OrderKatalog.waiting_katalog_fsection)
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "back":
        await OrderKatalog.waiting_katalog_section.set()
        await callback_query.message.edit_text("выберите раздел",reply_markup=keyboards.get_catalog_section_rkeyb())
    else:
        pos = fastdb.CATALOG_BUFFER.get_pos(callback_query.data, 0)
        await callback_query.message.edit_text("выберите подраздел", reply_markup=keyboards.get_catalog_fsection_rkeyb(callback_query.data))
        print(callback_query.data)
        await OrderKatalog.katalog_use.set()
        await state.update_data(catalog_step=0,
                                catalog_maxstep=fastdb.CATALOG_BUFFER.get_colpos_from_fsection(callback_query.data),
                                catalog_fsection=callback_query.data,
                                isopisopen=False)
        await bot.send_photo(callback_query.from_user.id,
                             pos.cap,
                             caption=format_text_tocatpos(pos, False),
                             reply_markup=keyboards.get_catalog_interactive_ikeyb(False, True, False))



@dp.callback_query_handler(lambda query: query.data == "back", state=OrderKatalog.katalog_use)
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    print(data['catalog_fsection'])
    await OrderKatalog.waiting_katalog_fsection.set()
    await callback_query.message.answer("выберите подраздел", reply_markup=keyboards.get_catalog_fsection_rkeyb(fastdb.get_fsection_from_section(data['catalog_fsection'])))


@dp.callback_query_handler(lambda query: query.data == "prew", state=OrderKatalog.katalog_use)
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    print('кнопка вперед нажата')
    data = await state.get_data()
    print('каталог шаг = ' + str(data['catalog_step']))
    prewbtn = True
    nextbtn = True
    if int(data['catalog_step']) == 0:
        prewbtn = False
        await callback_query.message.edit_reply_markup(
            reply_markup=keyboards.get_catalog_interactive_ikeyb(prewbtn, nextbtn, bool(data['isopisopen'])))
        return
    else:
        if int(data['catalog_step']) - 1 == 0:
           prewbtn = False
        pos = fastdb.CATALOG_BUFFER.get_pos(data['catalog_fsection'], data['catalog_step'] - 1)
        await callback_query.message.edit_media(
            media=InputMediaPhoto(media=pos.cap, caption=format_text_tocatpos(pos, bool(data['isopisopen']))),
            reply_markup=keyboards.get_catalog_interactive_ikeyb(prewbtn, nextbtn, bool(data['isopisopen'])))
        await state.update_data(catalog_step=data['catalog_step'] - 1)


@dp.callback_query_handler(lambda query: query.data == "next", state=OrderKatalog.all_states)
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    print('кнопка вперед нажата')
    data = await state.get_data()
    print('каталог шаг = ' + str(data['catalog_step']))
    prewbtn = True
    nextbtn = True
    if int(data['catalog_step']) == int(data['catalog_maxstep']):
        nextbtn = False
        await callback_query.message.edit_reply_markup(
            reply_markup=keyboards.get_catalog_interactive_ikeyb(prewbtn, nextbtn, bool(data['isopisopen'])))
        return
    else:
        if int(data['catalog_step']) + 1 == int(data['catalog_maxstep']):
            nextbtn = False
        pos = fastdb.CATALOG_BUFFER.get_pos(data['catalog_fsection'], data['catalog_step'] + 1)
        # await callback_query.message.photo.append(pos.cap)
        await callback_query.message.edit_media(
            media=InputMediaPhoto(media=pos.cap, caption=format_text_tocatpos(pos, bool(data['isopisopen']))), reply_markup=keyboards.get_catalog_interactive_ikeyb(prewbtn, nextbtn, bool(data['isopisopen'])))
        await state.update_data(catalog_step=data['catalog_step'] + 1)


@dp.callback_query_handler(lambda query: query.data == 'showopis', state=OrderKatalog.all_states)
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    print('описание нажато')
    data = await state.get_data()
    pos = fastdb.CATALOG_BUFFER.get_pos(data['catalog_fsection'], data['catalog_step'])
    print('было'+str(data['isopisopen']))
    prewbtn = True
    nextbtn = True
    showopis = True
    if bool(data['isopisopen']) == True:
        showopis = False
    else:
        showopis = True
    print('стало: '
          + str(showopis))
    if int(data['catalog_step']) == int(data['catalog_maxstep']):
        nextbtn = False
    if int(data['catalog_step']) == 0:
        prewbtn = False
    await callback_query.message.edit_caption(caption=format_text_tocatpos(pos, showopis),
                                              reply_markup=keyboards.get_catalog_interactive_ikeyb(prewbtn, nextbtn, showopis))
    await state.update_data(isopisopen=showopis)


@dp.callback_query_handler(lambda query: query.data == 'cash', state=OrderKatalog.katalog_use)
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(coltoadd=1)
    data = await state.get_data()
    pos = fastdb.CATALOG_BUFFER.get_pos(data['catalog_fsection'], data['catalog_step'])
    await callback_query.message.answer(f'\nСколько штук \'{pos.name}\' добавить в корзину?',
                                        reply_markup=keyboards.get_addtocard_ikeyb())
    await OrderKatalog.katalog_cash_pick.set()


@dp.message_handler(state=OrderKatalog.katalog_cash_pick, content_types=types.ContentTypes.TEXT)
async def step_getbrand(message: types.Message, state: FSMContext):
    mes_text = ''
    if message.text.isnumeric():
        data = await state.get_data()
        pos = fastdb.CATALOG_BUFFER.get_pos(data['catalog_fsection'], data['catalog_step'])
        dbfunc.add_to_card(message.from_user.id,
                           pos,
                           int(message.text))
        mes_text = f"{message.text}шт. \'{pos.name}\' добавлено в корзину."
        await OrderRedPos.waiting_pos_definition.set()
        await message.answer(mes_text, keyboards.get_card_ikeyb())
    else:
        mes_text = "Введите число"
        await message.answer(mes_text)

@dp.callback_query_handler(lambda query: query.data == 'nextcash', state=OrderKatalog.katalog_use)
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer(strings.KATALOG_SELECT_RAZDEL, reply_markup=keyboards.get_catalog_section_rkeyb())
    await OrderKatalog.waiting_katalog_section.set()

@dp.callback_query_handler(lambda query: query.data == 'gocard', state=OrderKatalog.katalog_use)
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    mes_text = ''
    iter = 0
    cash = 0
    rows = dbfunc.get_card(callback_query.from_user.id)
    if len(rows):
        for elem in rows:
            iter += 1
            cash += int(elem[3]) * int(elem[4])
            mes_text += f'{str(iter)}. {elem[2]}: {str(elem[3])}шт. ({str(int(elem[3]) * int(elem[4]))})\n'
        mes_text += f'\nОбщая сумма: {str(cash)}р.'
        await callback_query.answer(mes_text, reply_markup=keyboards.get_card_ikeyb())
    else:
        mes_text += 'Корзина пуста'
        mes_text += f'\nОбщая сумма: {str(cash)}р.'
        await callback_query.answer(mes_text)
    await Card.card_wait.set()

# todo: продолжить покупки или перейти в корзину
# todo: статус оповещение



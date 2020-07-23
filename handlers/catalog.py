import types
from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto

import dbfunc
import fastdb
import globalset
from handlers.allstat import OrderAddPos, OrderRedPos, MainMenu, StateAdminMenu, OrderKatalog
from misc import dp, bot

from aiogram.types import ReplyKeyboardMarkup

import globalset
from misc import dp
from aiogram import types

from ui import keyboards
from ui.uifunc import format_text_tocatpos


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=OrderKatalog.waiting_katalog_section)
async def get_section(message: types.Message):
    if fastdb.is_section(message.text):
        mes_text = f'Вот что есть по категории \"{message.text}\"'
        await message.answer(mes_text, reply_markup=keyboards.get_catalog_fsection_rkeyb(message.text))
        await OrderKatalog.waiting_katalog_fsection.set()
    else:
        mes_text = f'{message.text}? Такой категории нет. Просто нажми на кнопку'
        await message.answer(mes_text)


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=OrderKatalog.waiting_katalog_fsection)
async def get_brand(message: types.Message, state: FSMContext):
    if fastdb.is_fsection(message.text):
        pos = fastdb.CATALOG_BUFFER.get_pos(message.text, 0)
        print(message.text)
        print(pos.cap)
        await message.answer(f'Тут весь снюс марки \'{message.text}\', что есть в наличии', reply_markup=keyboards.get_main_menu_rkeyb(fastdb.is_admin(message.from_user.id)))

        await state.update_data(catalog_step=0,
                                catalog_maxstep=fastdb.CATALOG_BUFFER.get_colpos_from_fsection(message.text),
                                catalog_fsection=message.text,
                                isopisopen=False)
        await bot.send_photo(message.from_user.id,
                             pos.cap,
                             caption=format_text_tocatpos(pos, False),
                             reply_markup=keyboards.get_catalog_interactive_ikeyb(False, True, False))
        await OrderKatalog.katalog_use.set()
    else:
        mes_text = f'{message.text}? Такой подкатегории нет. Просто нажми на кнопку'
        await message.answer(mes_text)


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
    if int(data['catalog_step']) + 1 == int(data['catalog_maxstep']):
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
    await callback_query.message.edit_caption(format_text_tocatpos(pos, data['isopisopen']) +
                                           f'\nСколько штук \'{pos.name}\' добавить в корзину?\n'+
                                              f'\nВыбрано: {str(data["coltoadd"]) + " из " + str(pos.col)}',
                                        reply_markup=keyboards.get_addtocard_ikeyb())
    await OrderKatalog.katalog_cash_pick.set()


@dp.callback_query_handler(lambda query: query.data == 'small', state=OrderKatalog.katalog_cash_pick)
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    pos = fastdb.CATALOG_BUFFER.get_pos(data['catalog_fsection'], data['catalog_step'])
    if int(data['coltoadd']) == 1:
        mes_txt = format_text_tocatpos(pos, data['isopisopen'])
        mes_txt += '\nКоличество не может быть меньше 1\n'
    else:
        await state.update_data(coltoadd=data['coltoadd']-1)
        mes_txt = format_text_tocatpos(pos, data['isopisopen'])
    await callback_query.message.edit_caption(f'Сколько штук \'{pos.name}\' добавить в корзину?' +
                                        f'\nВыбрано: {str(data["coltoadd"]) + " из " + str(pos.col)}',
                                        reply_markup=keyboards.get_addtocard_ikeyb())



@dp.callback_query_handler(lambda query: query.data == 'big', state=OrderKatalog.katalog_cash_pick)
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    pos = fastdb.CATALOG_BUFFER.get_pos(data['catalog_fsection'], data['catalog_step'])
    mes_txt = ''
    if int(data['coltoadd']) == int(pos.col):
        mes_txt = format_text_tocatpos(pos, data['isopisopen'])
        mes_txt += f'\nКоличество не может быть больше {str(pos.col)}\n'
    else:
        await state.update_data(coltoadd=data['coltoadd'] + 1)
        mes_txt = format_text_tocatpos(pos, data['isopisopen'])
    await callback_query.message.edit_caption(f'Сколько штук \'{pos.name}\' добавить в корзину?' +
                                              f'\nВыбрано: {str(data["coltoadd"]) + " из " + str(pos.col)}',
                                              reply_markup=keyboards.get_addtocard_ikeyb())


@dp.callback_query_handler(lambda query: query.data == 'ok', state=OrderKatalog.katalog_cash_pick)
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    pos = fastdb.CATALOG_BUFFER.get_pos(data['catalog_fsection'], data['catalog_step'])
    dbfunc.add_to_card(callback_query.from_user.id,
                       pos,
                       int(data['coltoadd']))
    print(str(callback_query.from_user.id) + ' - айдишник добавления')
    prewbtn = True
    nextbtn = True
    if int(data['catalog_step']) + 1 == int(data['catalog_maxstep']):
        nextbtn = False
    if int(data['catalog_step']) == 0:
        prewbtn = False
    await callback_query.message.edit_media(
        media=InputMediaPhoto(media=pos.cap, caption=format_text_tocatpos(pos, bool(data['isopisopen']))),
        reply_markup=keyboards.get_catalog_interactive_ikeyb(prewbtn, nextbtn, bool(data['isopisopen'])))
    await OrderKatalog.katalog_use.set()




from aiogram import types
from aiogram.dispatcher import FSMContext

import dbfunc
from misc import dp
from ui import keyboards
from ui.keyboards import get_card_ikeyb


@dp.callback_query_handler(lambda query: query.data == 'add', state='*')
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    mes_text = "Выбери способ получения: "
    await callback_query.message.edit_text(mes_text, reply_markup=keyboards.get_dostavka_ikeyb())


@dp.callback_query_handler(lambda query: query.data == 'clear', state='*')
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    mes_text = 'Корзина пуста'
    mes_text += f'\nОбщая сумма: 0р.'
    dbfunc.delete_card(callback_query.from_user.id)
    await callback_query.message.edit_text(mes_text, reply_markup=get_card_ikeyb())

    
@dp.callback_query_handler(lambda query: query.data == 'kura', state='*')
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    mes_text = "Выбери способ получения: "
    await callback_query.message.edit_text(mes_text, reply_markup=keyboards.get_dostavka_ikeyb())


@dp.callback_query_handler(lambda query: query.data == 'samov', state='*')
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    mes_text = "Выбери способ получения: "
    await callback_query.message.edit_text(mes_text, reply_markup=keyboards.get_dostavka_ikeyb())
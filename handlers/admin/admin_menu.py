from aiogram import types
from aiogram.dispatcher import FSMContext

import fastdb
from handlers.allstat import StateAdminMenu, OrderRedPos, OrderAddPos, OrderDelPos
from misc import dp
from ui import keyboards


@dp.callback_query_handler(lambda query: query.data == "adminmain1", state='*')
async def send_admin_menu(callback_query: types.CallbackQuery):
    mes_text = fastdb.get_adminposliststr()
    await callback_query.message.edit_text(mes_text, reply_markup=keyboards.get_admin_redactpos_ikeyb())
    await StateAdminMenu.waiting_redadd.set()


@dp.callback_query_handler(lambda query: query.data == "adminmain2", state='*')
async def send_admin_menu(callback_query: types.CallbackQuery):
    mes_text = fastdb.get_adminposliststr()
    await callback_query.message.edit_text(mes_text, reply_markup=keyboards.get_admin_redactpos_ikeyb())
    await StateAdminMenu.waiting_redadd.set()


@dp.callback_query_handler(lambda query: query.data == "adminmain3", state='*')
async def send_admin_menu(callback_query: types.CallbackQuery):
    mes_text = fastdb.get_admin_settings()
    await callback_query.message.edit_text(mes_text, reply_markup=keyboards.get_admin_redactsettings_ikeyb())
    await StateAdminMenu.waiting_num_sett.set()


@dp.callback_query_handler(lambda query: query.data == 'adminsred', state=StateAdminMenu.waiting_num_sett)
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    mes_text = "Выберите пункт меню:\n" + fastdb.get_admin_settings()
    await callback_query.message.edit_text(mes_text)
    await StateAdminMenu.waiting_num_sett.set()

@dp.message_handler(state=StateAdminMenu.waiting_num_sett, content_types=types.ContentTypes.TEXT)
async def step_getdefinition(message: types.Message, state: FSMContext):
    mes_text = ''
    if message.text.isnumeric():
        if int(message.text) == 1:
            await StateAdminMenu.waiting_newnum_sett.set()
            await state.update_data(num=1)
            mes_text = "Ведите новую стоимость доставки"
            await message.answer(mes_text)
        elif int(message.text) == 2:
            await StateAdminMenu.waiting_newnum_sett.set()
            await state.update_data(num=2)
            mes_text = "Ведите новый процент бонуса"
            await message.answer(mes_text)


@dp.message_handler(state=StateAdminMenu.waiting_newnum_sett, content_types=types.ContentTypes.TEXT)
async def step_getdefinition(message: types.Message, state: FSMContext):
    data = state.get_data()
    if int(data['num']) == 1:
        fastdb.DOSTAVKA_COST = message.text
    else: fastdb.BONUS_PERCENT = message.text
    await StateAdminMenu.waiting_newnum_sett.set()


@dp.message_handler(state=StateAdminMenu.waiting_num_sett, content_types=types.ContentTypes.TEXT)
async def step_getdefinition(message: types.Message, state: FSMContext):
    mes_text = ''
    if message.text.isnumeric():
        if int(message.text) == 1:
            mes_text = "Ведите новую стоимость доставки"
            await message.answer(mes_text)
        elif int(message.text) == 2:
            mes_text = "Ведите новый процент бонуса"
            await message.answer(mes_text)
    await StateAdminMenu.waiting_newnum_sett.set()



@dp.callback_query_handler(lambda query: query.data == 'adminredactpos1', state=StateAdminMenu.waiting_redadd)
async def start_redpos(callback_query: types.CallbackQuery):
    mes_text = "Введите номер позиции, подлежащей редактированию: \n\n"
    mes_text += fastdb.get_adminposliststr()
    await callback_query.message.edit_text(mes_text)
    await OrderRedPos.waiting_pos_selection.set()


@dp.callback_query_handler(lambda query: query.data == 'adminredactpos2', state=StateAdminMenu.waiting_redadd)
async def start_addpos(callback_query: types.CallbackQuery):
    mes_text = "Шаг 1 из 7\nВведите название позиции"
    await callback_query.message.edit_text(mes_text)
    await OrderAddPos.waiting_pos_name.set()


@dp.callback_query_handler(lambda query: query.data == 'adminredactpos3', state=StateAdminMenu.waiting_redadd)
async def start_delpos(callback_query: types.CallbackQuery, state: FSMContext):
    mes_text = "Введите номер позиции, подлежащей удалению: \n\n"
    mes_text += fastdb.get_adminposliststr()
    await callback_query.message.edit_text(mes_text)
    await state.update_data(message_id=callback_query.message.message_id)
    await OrderDelPos.waiting_del_selection.set()


@dp.callback_query_handler(lambda query: query.data == 'adminredactpos4', state=StateAdminMenu.waiting_redadd)
async def start_addpos(callback_query: types.CallbackQuery):
    in_sklad = fastdb.get_colcost_sklad()
    mes_text = f"Единиц на складе: {in_sklad[0]}\nНа сумму: {in_sklad[1]}"
    await callback_query.message.edit_text(mes_text, reply_markup=keyboards.get_admin_inline_ikeyb())
    await StateAdminMenu.admin_main_menu.set()
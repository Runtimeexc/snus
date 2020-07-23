from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import misc
from handlers.allstat import MainMenu
from misc import dp
import globalset
import fastdb

current_mess: int
current_id: int


# @dp.message_handler(content_types=['photo'])
# async def handle_docs_photo(message):
#
#     raw = await message.photo[0].download()
#
#     b.write(raw.raw)
#     with open('testfile.jpg', 'wb') as f:
#         f.write(b.getvalue())


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=MainMenu.Wait_menu_pick)
async def all_other_messages(message: types.Message):
    print(message.from_user.id)
    if globalset.is_user(message):
        global current_mess
        global current_id
        current_mess = message.text
        current_id = message.from_user.id
        mes_text = 'Вы хотите отправить свой вопрос оператору?'
        inline_keyb = InlineKeyboardMarkup()
        inline_keyb.add(InlineKeyboardButton('отправить', callback_data='send'))
        inline_keyb.insert(InlineKeyboardButton('не отправлять', callback_data='notsend'))
        await message.answer(mes_text, reply_markup=inline_keyb, reply=True)

   # else:
        # await message.answer('test. to be continue', reply=True)


@dp.callback_query_handler(lambda query: query.data == "send", state='*')
async def process_callback(callback_query: types.CallbackQuery):
    global current_mess
    mes_text = 'Отправлено'
    await callback_query.message.edit_text(mes_text)

    id_user = callback_query.message.from_user.id
    mes_text = str(id_user) + ' Отправл вам сообщение:\n\n' + current_mess
    await misc.bot.send_message(chat_id=538011007, text=mes_text)


@dp.callback_query_handler(lambda query: query.data == "обратная связь")
async def send_admin_menu(callback_query: types.CallbackQuery):
    mes_text = 'Чтобы связаться с администрацией, напиши мне свой вопрос'

    await callback_query.message.edit_text(mes_text)


@dp.callback_query_handler(lambda query: query.data == "notsend")
async def process_callback(callback_query: types.CallbackQuery):
    mes_text = 'Ок'
    await callback_query.message.edit_text(mes_text)
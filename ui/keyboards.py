from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

import fastdb
from classes import Position

admin_inline_main = ['Редактирование позиций', 'Контроль остатков', 'Редактирование сотрудников',
                     'Просмотр базы пользователей']
admin_inline_redactpos = ["редактировать", "добавить", "Удалить", "вернуться назад"]

menu_reply_main = [['каталог', 'корзина'], ['акции', 'заказы']]



def get_admin_inline_ikeyb():
    inline_keyb = InlineKeyboardMarkup()
    callback_num = 0
    for text_btn in admin_inline_main:
        callback_num += 1
        inline_keyb.add(InlineKeyboardButton(text_btn, callback_data='adminmain' + str(callback_num)))
    return inline_keyb


def get_admin_redactpos_ikeyb():
    inline_keyb = InlineKeyboardMarkup()
    iter = 0
    for text_btn in admin_inline_redactpos:
        iter += 1
        inline_btn = InlineKeyboardButton(text_btn, callback_data='adminredactpos' + str(iter))
        inline_keyb.add(inline_btn)
    return inline_keyb


def get_admin_sectionpick_rkeyb():
    text_btns = fastdb.ALL_SECTIONS
    for text_btn in text_btns:
        text_btns.append([text_btn])
    return ReplyKeyboardMarkup(text_btns, resize_keyboard=True)


def get_admin_fsectionpick_rkeyb():
    text_btns = fastdb.ALL_FSECTIONS
    for text_btn in text_btns:
        text_btns.append([text_btn])
    return ReplyKeyboardMarkup(text_btns, resize_keyboard=True)


def get_main_menu_rkeyb(isadmin: bool):
    text_btns = menu_reply_main
    print(text_btns)
    if isadmin:
        text_btns.append(['админ панель'])
    return ReplyKeyboardMarkup(text_btns, resize_keyboard=True)


def get_catalog_section_rkeyb():
    text_btns = []
    for text_btn in fastdb.ALL_SECTIONS:
        text_btns.append([text_btn])
    return ReplyKeyboardMarkup(text_btns, resize_keyboard=True)


def get_catalog_fsection_rkeyb(section: str):
    text_btns = []
    for text_btn in fastdb.get_fsections_from_section(section):
        text_btns.append([text_btn])
    return ReplyKeyboardMarkup(text_btns, resize_keyboard=True)


def get_catalog_interactive_ikeyb(prew: bool, next: bool, isopisopen: bool):
    nextcall = 'next'
    prewcall = 'prew'
    if isopisopen:
        opisbtntext = 'скрыть описание'
    else:
        opisbtntext = 'показать описание'
    if prew:
        prewtext = '⬅️'
    else:
        prewcall = 'noprew'
        prewtext = '❌'
    if next:
        nexttext = '➡️'
    else:
        nextcall = 'nonext'
        nexttext = '❌'
    inline_keyb = InlineKeyboardMarkup(row_width=3)
    btnprew = InlineKeyboardButton(prewtext, callback_data=prewcall)
    btnnext = InlineKeyboardButton(nexttext, callback_data=nextcall)
    btnopis = InlineKeyboardButton(opisbtntext, callback_data='showopis')
    btncash = InlineKeyboardButton('добавить в корзину', callback_data='cash')
    inline_keyb.add(btnprew, btnopis, btnnext)
    inline_keyb.add(btncash)
    return inline_keyb


def get_addtocard_ikeyb():
    inline_keyb = InlineKeyboardMarkup(row_width=3)
    btnsmall = InlineKeyboardButton('-', callback_data='small')
    btnbig = InlineKeyboardButton('+', callback_data='big')
    btnok = InlineKeyboardButton('➡️', callback_data='ok')
    inline_keyb.add(btnsmall, btnok, btnbig)
    return inline_keyb


def get_card_ikeyb():
    inline_keyb = InlineKeyboardMarkup(row_width=1)
    btnsmall = InlineKeyboardButton('оформить заказ', callback_data='add')
    btnbig = InlineKeyboardButton('очистить корзину', callback_data='clear')
    inline_keyb.add(btnsmall)
    inline_keyb.add(btnbig)
    return inline_keyb


def get_dostavka_ikeyb():
    inline_keyb = InlineKeyboardMarkup(row_width=1)
    btnsmall = InlineKeyboardButton(f'курьером (+{str(fastdb.DOSTAVKA_COST)}р.)', callback_data='kura')
    btnbig = InlineKeyboardButton('самовывоз (пушкинаколотушкина дом 77)', callback_data='samov')
    inline_keyb.add(btnsmall)
    inline_keyb.add(btnbig)
    return inline_keyb



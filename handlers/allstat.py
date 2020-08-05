from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from misc import dp


class StateAdminMenu(StatesGroup):
    admin_main_menu = State()
    waiting_redadd = State()
    waiting_admin_redset = State()
    waiting_num_sett = State()
    waiting_newnum_sett = State()


class OrderAddPos(StatesGroup):
    waiting_pos_name = State()
    waiting_pos_cost = State()
    waiting_pos_section = State()
    waiting_pos_brand = State()
    waiting_pos_definition = State()
    waiting_pos_col = State()
    waiting_pos_cap = State()


class OrderDelPos(StatesGroup):
    waiting_del_selection = State()


class OrderRedPos(StatesGroup):
    waiting_pos_selection = State()
    waiting_pos_name = State()
    waiting_pos_cost = State()
    waiting_pos_section = State()
    waiting_pos_brand = State()
    waiting_pos_definition = State()
    waiting_pos_col = State()
    waiting_pos_cap = State()


class MainMenu(StatesGroup):
    Wait_menu_pick = State()

class Card(StatesGroup):
    card_wait = State()

class OrderKatalog(StatesGroup):
    waiting_katalog_section = State()
    waiting_katalog_fsection = State()
    katalog_use = State()
    katalog_cash_pick = State()
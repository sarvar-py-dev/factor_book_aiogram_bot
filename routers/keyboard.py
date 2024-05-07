from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardBuilder, InlineKeyboardBuilder

from routers.cons import database

admin_panel_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Product qoshish'), KeyboardButton(text='Category qoshish')],
              [KeyboardButton(text='Delete category'), KeyboardButton(text='Delete product')],
              [KeyboardButton(text='📚 Kitoblar')]
              ],
    resize_keyboard=True)


def show_categories(user_id):
    ikb = InlineKeyboardBuilder()
    for k, v in database['categories'].items():
        ikb.add(InlineKeyboardButton(text=v, callback_data=k))
    ikb.add(InlineKeyboardButton(text='🔍 Qidirish', switch_inline_query_current_chat=''))
    if str(user_id) in database['basket']:
        ikb.add(InlineKeyboardButton(text=f'🛒 Savat ({len(database["basket"][str(user_id)])})', callback_data='savat'))
    ikb.adjust(2, repeat=True)
    return ikb


def make_plus_minus(quantity, product_id):
    ikb = InlineKeyboardBuilder()
    ikb.row(InlineKeyboardButton(text="➖", callback_data="change-" + product_id),
            InlineKeyboardButton(text=str(quantity), callback_data="number"),
            InlineKeyboardButton(text="➕", callback_data="change+" + product_id)
            )
    ikb.row(InlineKeyboardButton(text="◀️Orqaga", callback_data="categoryga"),
            InlineKeyboardButton(text='🛒 Savatga qo\'shish', callback_data="savatga" + product_id + str(quantity)))
    return ikb


main_keyboard = ReplyKeyboardBuilder()
main_keyboard.row(KeyboardButton(text='📚 Kitoblar'))
main_keyboard.row(KeyboardButton(text='📃 Mening buyurtmalarim'))
main_keyboard.row(KeyboardButton(text='🔵 Biz ijtimoyi tarmoqlarda'), KeyboardButton(text='📞 Biz bilan bog\'lanish'))

import requests
from aiogram import F, Bot, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart, Filter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, Message, CallbackQuery, KeyboardButton, ReplyKeyboardRemove, \
    InlineQueryResultArticle, InlineQuery, InputTextMessageContent
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.utils.i18n import gettext as _

import routers.keyboard as kb

from routers.cons import ADMIN_LIST, database
from routers.keyboard import show_categories, make_plus_minus, main_keyboard

main_router = Router()


@main_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    rkb = main_keyboard
    msg = 'Assalomu alaykum! Tanlang.'
    if str(message.from_user.id) not in database['users']:
        msg = 'Assalomu alaykum! \nXush kelibsiz!'
        users = database['users']
        users[str(message.from_user.id)] = True
        database['users'] = users
    await message.answer(text=msg, reply_markup=rkb.as_markup(resize_keyboard=True))


@main_router.message(Command(commands='help'))
async def help_command(message: Message) -> None:
    await message.answer('''Buyruqlar:
/start - Botni ishga tushirish
/help - Yordam''')


@main_router.message(F.text == '🔵 Biz ijtimoyi tarmoqlarda')
async def our_social_network(message: Message) -> None:
    ikb = InlineKeyboardBuilder()
    ikb.row(InlineKeyboardButton(text='IKAR | Factor Books', url='https://t.me/ikar_factor'))
    ikb.row(InlineKeyboardButton(text='Factor Books', url='https://t.me/factor_books'))
    ikb.row(InlineKeyboardButton(text='\"Factor Books\" nashiryoti', url='https://t.me/factorbooks'))
    await message.answer('Biz ijtimoiy tarmoqlarda', reply_markup=ikb.as_markup())


@main_router.message(F.text == '📚 Kitoblar')
async def books(message: Message) -> None:
    ikb = show_categories(message.from_user.id)
    await message.answer('Kategoriyalardan birini tanlang', reply_markup=ikb.as_markup())


@main_router.callback_query(F.data.startswith('orqaga'))
async def back_handler(callback: CallbackQuery):
    await callback.message.edit_text('Kategoriyalardan birini tanlang',
                                     reply_markup=show_categories(callback.from_user.id).as_markup())


@main_router.message(F.text == "📞 Biz bilan bog'lanish")
async def message(message: Message) -> None:
    text = f"""\n
\n
Telegram: @sarvar_py_dev\n
📞  +{998994312269}\n
🤖 Bot Davranbekov Sarvarbek (@sarvar_py_dev) tomonidan tayorlandi.\n"""
    await message.answer(text=text, parse_mode=ParseMode.HTML)


@main_router.message(lambda msg: msg.text[-36:] in database['products'])
async def answer_inline_query(message: Message):
    msg = message.text[-36:]
    product = database['products'][msg]
    ikb = make_plus_minus(1, msg)
    await message.delete()
    await message.answer_photo(photo=product['image'], caption=product['text'], reply_markup=ikb.as_markup())


@main_router.callback_query()
async def product_handler(callback: CallbackQuery):
    if callback.data in database['categories']:
        ikb = InlineKeyboardBuilder()
        for k, v in database['products'].items():
            if v['category_id'] == callback.data:
                ikb.add(InlineKeyboardButton(text=v['name'], callback_data=k))
        if str(callback.from_user.id) in database['basket']:
            ikb.add(InlineKeyboardButton(text=f'🛒 Savat ({len(database["basket"][str(callback.from_user.id)])})',
                                         callback_data='savat'))
        ikb.add(InlineKeyboardButton(text="◀️ orqaga", callback_data='orqaga'))
        ikb.adjust(2, repeat=True)
        await callback.message.edit_text(database['categories'][callback.data], reply_markup=ikb.as_markup())
    elif callback.data in database['products']:
        product = database['products'][callback.data]
        ikb = make_plus_minus(1, callback.data)
        await callback.message.delete()
        await callback.message.answer_photo(photo=product['image'], caption=product['text'],
                                            reply_markup=ikb.as_markup())

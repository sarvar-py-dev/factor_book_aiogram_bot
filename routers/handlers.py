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
from routers.keyboard import show_categories, make_plus_minus

main_router = Router()


@main_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    rkb = ReplyKeyboardBuilder()
    rkb.row(KeyboardButton(text=_('📚 Kitoblar')))
    rkb.row(KeyboardButton(text=_('📃 Mening buyurtmalarim')))
    rkb.row(KeyboardButton(text=_('🔵 Biz ijtimoyi tarmoqlarda')), KeyboardButton(text=_('📞 Biz bilan bog\'lanish')))
    msg = _('Assalomu alaykum! Tanlang.')
    if str(message.from_user.id) not in database['users']:
        msg = _('Assalomu alaykum! \nXush kelibsiz!')
        users = database['users']
        users[str(message.from_user.id)] = True
        database['users'] = users
    await message.answer(text=msg, reply_markup=rkb.as_markup(resize_keyboard=True))


@main_router.message(Command(commands='help'))
async def help_command(message: Message) -> None:
    await message.answer(_('''Buyruqlar:
/start - Botni ishga tushirish
/help - Yordam'''))


@main_router.message(F.text == _('🔵 Biz ijtimoyi tarmoqlarda'))
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


@main_router.callback_query(F.data.startswith('categoryga'))
async def to_category(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Kategoriyalardan birini tanlang',
                                  reply_markup=show_categories(callback.from_user.id).as_markup())


@main_router.callback_query(F.data.startswith('savatga'))
async def to_basket(callback: CallbackQuery):
    basket_ = database['basket']
    user = basket_.get(str(callback.from_user.id))
    product_id = callback.data[7:43]
    product = database['products'][product_id]
    if user:
        if user.get(product_id):
            user[product_id]['quantity'] += int(callback.data[43:])
        else:
            user[product_id] = {
                'product_name': product['name'],
                'quantity': callback.data[43:],
                'price': product['price']
            }
    else:
        basket_[str(callback.from_user.id)] = {
            product_id: {
                'product_name': product['name'],
                'quantity': int(callback.data[43:]),
                'price': product['price']
            }
        }
    database['basket'] = basket_
    await to_category(callback)


quantity = 1


@main_router.callback_query(F.data.startswith("change"))
async def change_plus(callback: CallbackQuery):
    global quantity
    if callback.data.startswith("change+"):
        quantity += 1
    elif quantity < 2:
        await callback.answer('Eng kamida 1 ta kitob buyurtma qilishingiz mumkin! 😊', show_alert=True)
        return
    else:
        quantity -= 1
    ikb = make_plus_minus(quantity, callback.data[7:])
    await callback.message.edit_reply_markup(str(callback.message.message_id), reply_markup=ikb.as_markup())


@main_router.message(F.text == "📞 Biz bilan bog'lanish")
async def message(message: Message) -> None:
    text = f"""\n
\n
Telegram: @sarvar_py_dev\n
📞  +{998994312269}\n
🤖 Bot Davranbekov Sarvarbek (@sarvar_py_dev) tomonidan tayorlandi.\n"""
    await message.answer(text=text, parse_mode=ParseMode.HTML)


@main_router.callback_query(F.data.startswith('savat'))
async def basket(callback: CallbackQuery):
    basket_of_user = database['basket'][str(callback.from_user.id)]
    msg = f'🛒 Savat \n\n'
    all_sum = 0
    for i, v in enumerate(basket_of_user.values()):
        summa = int(v['quantity']) * int(v['price'])
        msg += f'{i + 1}. {v["product_name"]} \n{v["quantity"]} x {v["price"]} = {str(summa)} so\'m\n\n'
        all_sum += summa
    msg += f'Jami: {all_sum} so\'m'
    ikb = InlineKeyboardBuilder()
    ikb.row(InlineKeyboardButton(text='❌ Savatni tozalash', callback_data='clear'))
    ikb.row(InlineKeyboardButton(text='✅ Buyurtmani tasdiqlash', callback_data='confirm'))
    ikb.row(InlineKeyboardButton(text='◀️ orqaga', callback_data='categoryga'))
    await callback.message.edit_text(msg, reply_markup=ikb.as_markup())


@main_router.callback_query(F.data.startswith('clear'))
async def clear(callback: CallbackQuery):
    basket_ = database['basket']
    basket_.pop(str(callback.from_user.id))
    database['basket'] = basket_
    await to_category(callback)


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
        ikb = make_plus_minus(quantity, callback.data)
        await callback.message.delete()
        await callback.message.answer_photo(photo=product['image'], caption=product['text'],
                                            reply_markup=ikb.as_markup())


@main_router.message(F.text == 'confirm')
async def confirm(callback: CallbackQuery):
    pass


def make_url():
    with open('for_url.jpg', 'rb') as f:
        response = requests.post('https://telegra.ph/upload', files={'file': f})
        data = response.json()
        url = "https://telegra.ph" + data[0].get('src').replace(r"\\", '')
    return url

# @main_router.inline_query()
# async def command_start_handler(inline_query: InlineQuery) -> None:
#     iqr = []
#     products = database['products']
#     for i, v in enumerate(products.values()):
#         iqr.append(InlineQueryResultArticle(
#             id=str(i),
#             title=v['name'],
#             input_message_content=InputTextMessageContent(
#                 message_text=f"{v['name']} \n\n<i>{v['text']}</i>\nBuyurtma qilish uchun  : @facror_book_bot\n\n"
#             ),
#             thumbnail_url=make_url(),
#             description=f"Factor Books\n💵 Narxi: {v['price']} so'm",
#         ))
#         if i >= 49:
#             break
#
#     await inline_query.answer(iqr)

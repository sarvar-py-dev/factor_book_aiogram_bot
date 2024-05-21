import datetime

from aiogram import F, Router, Bot
from aiogram.enums import ContentType, ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, InlineKeyboardButton, ReplyKeyboardMarkup, \
    KeyboardButton, Message, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _, lazy_gettext as __

from routers.basket import to_category, basket_msg
from routers.cons import database, ADMIN_LIST
from routers.keyboard import main_keyboard_btn

order_router = Router()


class BasketState(StatesGroup):
    phone_number = State()


def order_msg(user_id, order_num):
    user_order = database['orders'][str(user_id)][str(order_num)]
    msg = f'🔢 Buyurtma raqami: <b>{order_num}</b>\n📆 Buyurtma qilingan sana: <b>{user_order["date_time"]}</b>\n🟣 Buyurtma holati: <b>{user_order["order_status"]}</b>\n'
    all_sum = 0
    for i, v in enumerate(user_order['products'].values()):
        summa = int(v['quantity']) * int(v['price'])
        msg += f'\n{i + 1}. 📕 Kitob nomi: {v["product_name"]} \n{v["quantity"]} x {v["price"]} = {str(summa)} so\'m\n'
        all_sum += summa
    msg += f'\n💸 Umumiy narxi: {all_sum} so\'m'
    return msg


def clear_users_basket(user_id):
    basket_ = database['basket']
    basket_.pop(str(user_id))
    database['basket'] = basket_


@order_router.callback_query(F.data.startswith('clear'))
async def clear(callback: CallbackQuery):
    clear_users_basket(callback.from_user.id)
    await to_category(callback)


@order_router.callback_query(F.data.endswith('confirm'))
async def confirm(callback: CallbackQuery, state: FSMContext):
    rkb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=_('📞 Telefon raqam'), request_contact=True)]], resize_keyboard=True)
    await callback.message.delete()
    await callback.message.answer(_('Telefon raqamingizni qoldiring (📞 Telefon raqam tugmasini bosing)🔽:'),
                                  reply_markup=rkb)
    await state.set_state(BasketState.phone_number)


@order_router.message(F.content_type == ContentType.CONTACT, BasketState.phone_number)
async def phone_number(message: Message):
    msg = basket_msg(message.from_user.id)
    msg += f'\nTelefon raqamingiz: {message.contact.phone_number}\n\n<i>Buyurtma berasizmi?</i>'
    ikb = InlineKeyboardBuilder()
    ikb.row(InlineKeyboardButton(text=_("❌ Yo'q"), callback_data='canceled_order'),
            InlineKeyboardButton(text=_('✅ Ha'), callback_data='confirm_order' + str(message.contact.phone_number)))
    await message.answer(msg, reply_markup=ikb.as_markup())


@order_router.callback_query(F.data.endswith('canceled_order'))
async def canceled_order(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(_('❌ Bekor qilindi'))
    rkb = main_keyboard_btn()
    await callback.message.answer(_('Asosiy menyu'), reply_markup=rkb.as_markup(resize_keyboard=True))


@order_router.callback_query(F.data.startswith('confirm_order'))
async def confirm_order(callback: CallbackQuery, bot: Bot):
    await callback.message.delete()
    orders = database['orders']
    if not orders.get('order_num'):
        orders['order_num'] = 0
    orders['order_num'] += 1
    if not orders.get(str(callback.from_user.id)):
        orders[str(callback.from_user.id)] = {}
    orders[str(callback.from_user.id)][str(orders['order_num'])] = {
        'date_time': str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        'order_status': '🔄 kutish holatida',
        'products': database['basket'][str(callback.from_user.id)],
        'phone_number': callback.data[13:]
    }
    database['orders'] = orders
    ikb = InlineKeyboardBuilder()
    ikb.row(
        InlineKeyboardButton(text=_("❌ Yo'q"),
                             callback_data='from_admin_canceled_order-' + str(callback.from_user.id) + '-' + str(
                                 orders[
                                     'order_num'])),
        InlineKeyboardButton(text=_('✅ Ha'),
                             callback_data='from_admin_order_accept-' + str(callback.from_user.id) + '-' + str(
                                 orders[
                                     'order_num'])))
    await bot.send_message(ADMIN_LIST[0], order_msg(callback.from_user.id,
                                                    orders[
                                                        'order_num']) + f"\n\nKlient: +{int(callback.data[13:])} <a href='tg://user?id={callback.from_user.id}'>{callback.from_user.full_name}</a>\n Buyurtmani qabul qilasizmi",
                           parse_mode=ParseMode.HTML, reply_markup=ikb.as_markup())
    await callback.message.answer(
        _('✅ Hurmatli mijoz! Buyurtmangiz uchun tashakkur.\nBuyurtma raqami: {orders_num}').format(
            orders_num=orders["order_num"]),
        reply_markup=main_keyboard_btn().as_markup(resize_keyboard=True))
    clear_users_basket(callback.from_user.id)


@order_router.callback_query(F.data.startswith('from_admin'))
async def order_accept_canceled(callback: CallbackQuery, bot: Bot):
    user_order = callback.data.split('-')[1:]
    orders = database['orders']
    users_orders = orders[user_order[0]]
    if callback.data.startswith('from_admin_order_accept'):
        users_orders[user_order[1]]['order_status'] = '✅ Zakaz qqabul qilingan'
        await bot.send_message(user_order[0],
                               _('<i>🎉 Sizning {order_num} raqamli buyurtmangizni admin qabul qildi.</i>').format(
                                   order_num=user_order[1]))
        await callback.message.edit_reply_markup()
    else:
        await callback.message.delete()
        users_orders.pop(user_order[1])
    database['orders'] = orders


@order_router.message(F.text == __('📃 Mening buyurtmalarim'))
async def my_orders(message: Message):
    if str(message.from_user.id) not in database['orders'] or not database['orders'][str(message.from_user.id)]:
        await message.answer(_('🤷‍♂️ Sizda hali buyurtmalar mavjud emas. Yoki bekor qilingan'))
    else:
        for order in database['orders'][str(message.from_user.id)].keys():
            ikb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=_('❌ bekor qilish'), callback_data='from_user_canceled_order' + order)]])
            await message.answer(order_msg(message.from_user.id, order), reply_markup=ikb)


@order_router.callback_query(F.data.startswith('from_user_canceled_order'))
async def canceled_order(callback: CallbackQuery, bot: Bot):
    await callback.message.delete()
    orders = database['orders']
    order_num = callback.data.split('from_user_canceled_order')[-1]
    orders[str(callback.from_user.id)].pop(order_num)
    database['orders'] = orders
    await callback.message.answer(f'{order_num} raqamli buyurtmangiz bekor qilindi')
    await bot.send_message(ADMIN_LIST[0],
                           f'{order_num} raqamli buyurtma bekor qilindi\n\nZakaz egasi {callback.from_user.mention_markdown(callback.from_user.full_name)}',
                           parse_mode=ParseMode.MARKDOWN_V2)

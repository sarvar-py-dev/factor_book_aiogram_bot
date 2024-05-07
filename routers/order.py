from aiogram import F, Router
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, InlineKeyboardButton, ReplyKeyboardMarkup, \
    KeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from routers.basket import to_category, basket_msg
from routers.cons import database
from routers.keyboard import main_keyboard

order_router = Router()


class BasketState(StatesGroup):
    phone_number = State()


@order_router.callback_query(F.data.startswith('clear'))
async def clear(callback: CallbackQuery):
    basket_ = database['basket']
    basket_.pop(str(callback.from_user.id))
    database['basket'] = basket_
    await to_category(callback)


@order_router.callback_query(F.data.startswith('confirm'))
async def confirm(callback: CallbackQuery, state: FSMContext):
    rkb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='📞 Telefon raqam', request_contact=True)]], resize_keyboard=True)
    await callback.message.delete()
    await callback.message.answer('Telefon raqamingizni qoldiring (📞 Telefon raqam tugmasini bosing)🔽:',
                                  reply_markup=rkb)
    await state.set_state(BasketState.phone_number)


@order_router.message(F.content_type == ContentType.CONTACT, BasketState.phone_number)
async def phone_number(message: Message):
    msg = basket_msg(message.from_user.id)
    msg += f'\nTelefon raqamingiz: {message.contact.phone_number}\n\n<i>Buyurtma berasizmi?</i>'
    ikb = InlineKeyboardBuilder()
    ikb.row(InlineKeyboardButton(text="❌ Yo'q", callback_data='canceled_order'),
            InlineKeyboardButton(text='✅ Ha', callback_data='confirm_order'))
    await message.answer(msg, reply_markup=ikb.as_markup())


@order_router.callback_query(F.data.startswith('canceled_order'))
async def canceled_order(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('❌ Bekor qilindi')
    rkb = main_keyboard
    await callback.message.answer('Asosiy menyu', reply_markup=rkb.as_markup(resize_keyboard=True))


@order_router.message(F.text == '📃 Mening buyurtmalarim')
async def my_orders(message: Message):
    if message.from_user.id in database['orders']:
        await message.answer('🤷‍♂️ Sizda hali buyurtmalar mavjud emas.')
    else:
        pass

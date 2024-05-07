from uuid import uuid4

from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove, Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from routers.cons import database, ADMIN_LIST
import routers.keyboard as kb
from routers.filters import ChatTypeFilter
from routers.keyboard import show_categories
from routers.filters import IsAdmin
from routers.utils import make_url

save_product = {}

admin_router = Router()
admin_router.message.filter(ChatTypeFilter([ChatType.PRIVATE]), IsAdmin())


class FormState(StatesGroup):
    category = State()
    product_name = State()
    product_price = State()
    product_image = State()
    product_text = State()
    product_category = State()
    delete_category = State()
    show_category = State()
    delete_product = State()


@admin_router.message(F.text == 'Category qoshish')
async def add_category(message: Message, state: FSMContext):
    await state.set_state(FormState.category)
    await message.answer('Category nomini kiriting', reply_markup=ReplyKeyboardRemove())


@admin_router.message(FormState.category)
async def add_category(message: Message, state: FSMContext):
    category = database['categories']
    category[str(uuid4())] = message.text
    database['categories'] = category
    await state.clear()
    await message.answer('Category qoshildi', reply_markup=kb.admin_panel_keyboard)


@admin_router.message(F.text == 'Delete category')
async def delete_category(message: Message, state: FSMContext):
    ikb = show_categories(message.from_user.id)
    await message.answer('Tanlang', reply_markup=ReplyKeyboardRemove())
    await message.answer('Category tanlang', reply_markup=ikb.as_markup())
    await state.set_state(FormState.delete_category)


@admin_router.callback_query(FormState.delete_category)
async def delete_category(callback: CallbackQuery, state: FSMContext):
    products = database['products']
    new_products = {}
    for k, v in products.items():
        if v['category_id'] != callback.data:
            new_products[k] = v
    database['products'] = new_products
    category = database['categories']
    category.pop(callback.data)
    database['categories'] = category
    await state.clear()
    await callback.message.delete()
    await callback.message.answer('Category va unga tegishli productlar o\'chirlidi',
                                  reply_markup=kb.admin_panel_keyboard)


@admin_router.message(F.text == 'Delete product')
async def delete_category(message: Message, state: FSMContext):
    ikb = show_categories(message.from_user.id)
    await message.answer('Tanlang', reply_markup=ReplyKeyboardRemove())
    await message.answer('Category tanlang', reply_markup=ikb.as_markup())
    await state.set_state(FormState.show_category)


@admin_router.callback_query(FormState.show_category)
async def show_product(callback: CallbackQuery, state: FSMContext):
    ikb = InlineKeyboardBuilder()
    for k, v in database['products'].items():
        if v['category_id'] == callback.data:
            ikb.add(InlineKeyboardButton(text=v['name'], callback_data=k))
    ikb.adjust(2, repeat=True)
    await callback.message.edit_text(database['categories'][callback.data], reply_markup=ikb.as_markup())
    await state.set_state(FormState.delete_product)


@admin_router.callback_query(FormState.delete_product)
async def delete_product(callback: CallbackQuery, state: FSMContext):
    products = database['products']
    products.pop(callback.data)
    database['products'] = products
    await state.clear()
    await callback.message.delete()
    await callback.message.answer('Product deleted', reply_markup=kb.admin_panel_keyboard)


@admin_router.message(F.text == 'Product qoshish')
async def add_product(message: Message, state: FSMContext):
    save_product = {}
    if not database['categories']:
        await message.answer('Avval category qoshing')
        return
    await state.set_state(FormState.product_name)
    await message.answer('Product nomini kiriting', reply_markup=ReplyKeyboardRemove())


@admin_router.message(FormState.product_name)
async def add_product(message: Message, state: FSMContext):
    save_product['name'] = message.text
    await state.set_state(FormState.product_text)
    await message.answer('Product description(text) kiriting: ')


@admin_router.message(FormState.product_text)
async def add_product(message: Message, state: FSMContext):
    save_product['text'] = message.text
    await state.set_state(FormState.product_image)
    await message.answer('Product rasmini kiriting: ')


@admin_router.message(FormState.product_image)
async def add_product(message: Message, state: FSMContext):
    file = await message.bot.get_file(message.photo[-1].file_id)
    img_byte = (await message.bot.download(file.file_id)).read()
    url = await make_url(img_byte)

    save_product['image'] = message.photo[0].file_id
    save_product['thumbnail_url'] = url
    await state.set_state(FormState.product_price)
    await message.answer('Product narxini kiriting: ')


@admin_router.message(FormState.product_price)
async def add_product(message: Message, state: FSMContext):
    save_product['price'] = message.text
    ikb = show_categories(message.from_user.id)
    await state.set_state(FormState.product_category)
    await message.answer('Kategoriyalardan birini tanlang', reply_markup=ikb.as_markup())


@admin_router.callback_query(FormState.product_category)
async def add_product(callback: CallbackQuery, state: FSMContext):
    if callback.data not in database['categories']:
        await callback.answer('Categoryda hatolik')
        return

    save_product['category_id'] = callback.data
    products_ = database['products']
    products_[str(uuid4())] = save_product
    database['products'] = products_
    await state.clear()
    await callback.message.delete()
    await callback.message.answer('Saqlandi', reply_markup=kb.admin_panel_keyboard)


@admin_router.message(CommandStart())
async def start_for_admin(message: Message):
    await message.answer('Tanlang', reply_markup=kb.admin_panel_keyboard)

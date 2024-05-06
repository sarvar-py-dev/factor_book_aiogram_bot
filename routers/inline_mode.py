from aiogram import Router, html, F
from aiogram.enums import ChatType
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, message, InlineQuery, InlineQueryResultArticle, \
    InputTextMessageContent, InlineQueryResult
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_get_categories, orm_get_category, orm_get_products, orm_get_product, orm_add_user, \
    orm_add_to_cart, orm_get_user_cart, orm_clear_cart, orm_get_all_products, orm_get_all_products_by_startswith
from filters import ChatTypeFilter
from keyboards.inline_keyboards import get_inline_keyboard
from keyboards.reply_keyboards import get_reply_keyboard

inline_router = Router()


@inline_router.shipping_query()
async def user_inline_handler(inline_query: InlineQuery, session: AsyncSession) -> InlineQueryResult:
    if inline_query.query == "":
        products = await orm_get_all_products(session)
        inline_list = []
        for product in products[:50]:
            inline_list.append(InlineQueryResultArticle(
                id=str(product.id),
                title=product.nomi,
                input_message_content=InputTextMessageContent(
                    message_text=product.nomi
                ),
                thumbnail_url="https://telegra.ph/file/8006558d9ff33ced877d2.png",
                description=str(product.narxi)
            ))

        await inline_query.answer(inline_list)
    else:
        products = await orm_get_all_products_by_startswith(session, inline_query.query)
        inline_list = []
        for product in products[:50]:
            inline_list.append(InlineQueryResultArticle(
                id=str(product.id),
                title=product.nomi,
                input_message_content=InputTextMessageContent(
                    message_text=product.nomi
                ),
                thumbnail_url="https://telegra.ph/file/8006558d9ff33ced877d2.png",
                description=str(product.narxi)
            ))

        await inline_query.answer(inline_list)

from mailbox import Message

from aiogram import Router, F
from aiogram.types import InlineQuery, InlineQueryResultArticle, \
    InputTextMessageContent

from routers.cons import database

inline_router = Router()


@inline_router.inline_query()
async def user_inline_handler(inline_query: InlineQuery):
    if inline_query.query == "":
        products = database['products']
        inline_list = []
        for i, (product_k, product_v) in enumerate(products.items()):
            inline_list.append(InlineQueryResultArticle(
                id=product_k,
                title=product_v['name'],
                input_message_content=InputTextMessageContent(
                    message_text=f"<i>{product_v['text'][2:]}</i>Buyurtma qilish uchun  : @facror_book_bot\n\nbook_id: {product_k}"
                ),
                thumbnail_url=product_v['thumbnail_url'],
                description=f"Factor Books\n💵 Narxi: {product_v['price']} so'm",
            ))
            if i == 50:
                break

        await inline_query.answer(inline_list)
    else:
        products = {k: v for k, v in database['products'].items() if inline_query.query.lower() in v['name'].lower()}
        inline_list = []
        for i, (product_k, product_v) in enumerate(products.items()):
            inline_list.append(InlineQueryResultArticle(
                id=product_k,
                title=product_v['name'],
                input_message_content=InputTextMessageContent(
                    message_text=f"<i>{product_v['text'][2:]}</i>Buyurtma qilish uchun  : @facror_book_bot\n\nbook_id: {product_k}"
                ),
                thumbnail_url=product_v['thumbnail_url'],
                description=f"Factor Books\n💵 Narxi: {product_v['price']} so'm",
            ))
            if i == 50:
                break

        await inline_query.answer(inline_list)

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, BotCommandScopeAllChatAdministrators, BotCommandScopeChat

from routers.cons import TOKEN, database, ADMIN_LIST
from aiogram.utils.i18n import I18n, FSMI18nMiddleware
from aiogram.utils.i18n import gettext as _
from routers import main_router, order_router, basket_router, inline_router, admin_router

dp = Dispatcher()


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    database['categories'] = database.get('categories', {})
    database['products'] = database.get('products', {})
    database['basket'] = database.get('basket', {})
    database['orders'] = database.get('orders', {'order_num': 0})
    database['users'] = database.get('users', {})
    command_list = [
        BotCommand(command='start', description='Botni boshlash'),
        BotCommand(command='help', description='Yordam'),
    ]
    await bot.set_my_commands(command_list)

    admin_commands = [
        BotCommand(command='start', description='Botni boshlash'),
        BotCommand(command='exel', description='exel orders'),
    ]
    scope = BotCommandScopeAllChatAdministrators()
    for admin_id in ADMIN_LIST:
        await bot.set_my_commands(admin_commands, BotCommandScopeChat(chat_id=admin_id))


async def on_shutdown(dispatcher: Dispatcher, bot: Bot):
    await bot.delete_my_commands()


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    i18n = I18n(path='locales')
    dp.update.outer_middleware.register(FSMI18nMiddleware(i18n))
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.include_routers(
        inline_router,
        admin_router,
        basket_router,
        order_router,
        main_router,
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

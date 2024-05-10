import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from routers.cons import TOKEN, database
from aiogram.utils.i18n import I18n, FSMI18nMiddleware
from aiogram.utils.i18n import gettext as _
from routers import main_router, order_router, basket_router, inline_router, admin_router

dp = Dispatcher()


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    if not (database.get('categories')):
        database['categories'] = {}
    if not database.get('products'):
        database['products'] = {}
    command_list = [
        BotCommand(command='start', description='Botni boshlash(봇 시작)'),
        BotCommand(command='help', description='Yordam(돕다)'),
    ]
    await bot.set_my_commands(command_list)


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

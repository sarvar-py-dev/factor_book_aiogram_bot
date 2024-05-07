from aiogram import Router

from routers.admin import admin_router
from routers.basket import basket_router
from routers.handlers import main_router
from routers.inline_mode import inline_router
from routers.order import order_router

start_routers = Router()

start_routers.include_routers(
    inline_router,
    admin_router,
    basket_router,
    order_router,
    main_router,
)

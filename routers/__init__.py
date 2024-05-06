from aiogram import Router

from routers.admin import admin_router
from routers.handlers import main_router

start_routers = Router()

start_routers.include_routers(
    admin_router,
    main_router,
)

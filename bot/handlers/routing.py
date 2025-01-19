from aiogram import Router

from .start import router as start_router
from .menu import router as menu_router
from .chats import router as chats_router

def get_main_router():
    main_router = Router()

    main_router.include_router(start_router)
    main_router.include_router(menu_router)
    main_router.include_router(chats_router)

    return main_router
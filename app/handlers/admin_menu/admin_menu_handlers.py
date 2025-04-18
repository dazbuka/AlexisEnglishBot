from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from app.utils.admin_utils import message_answer
import data.admin_messages as amsg
from app.handlers.admin_menu.admin_menu_states import MenuState, MenuCallSet
from app.handlers.admin_menu.admin_setting.setting_scheme_handlers import setting_scheme_router
from app.handlers.admin_menu.admin_adding.adding_word_handlers import adding_word_router

from app.handlers.common_settings import *

admin_menu_router = Router()
admin_menu_router.include_router(adding_word_router)
admin_menu_router.include_router(setting_scheme_router)


@admin_menu_router.callback_query(F.data == amsg.ADMIN_MENU_BUTTON_TEXT)
@admin_menu_router.callback_query(F.data == C_ADM_MENU_ADDING)
@admin_menu_router.callback_query(F.data == C_ADM_MENU_SETTING)

async def admin_menu_setting_button(call: CallbackQuery, state: FSMContext):
    # создаем экземпляр класса меню
    current_menu = MenuCallSet()
    # обрабатываем экземпляра класса, который анализирует какой меню колл пришел и выдает сообщение и клавиатуру
    await current_menu.set(call, state)
    await message_answer(source=call, message_text=current_menu.message_text, reply_markup=current_menu.reply_kb)
    await call.answer()

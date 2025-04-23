from aiogram.filters.command import Command, CommandStart
from aiogram.types import Message, CallbackQuery
import app.keyboards.user_keyboards as ukb
from app.database.requests import set_user

from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from app.utils.admin_utils import message_answer
from app.handlers.admin_menu.states.menu_states import MenuStateParams
from app.handlers.admin_menu.admin_setting.setting_scheme_handlers import setting_scheme_router
from app.handlers.admin_menu.admin_setting.setting_colls_handlers import setting_colls_router
from app.handlers.admin_menu.admin_adding.adding_word_handlers import adding_word_router
from app.handlers.admin_menu.admin_adding.adding_coll_handlers import adding_coll_router
from app.handlers.admin_menu.admin_adding.adding_group_handlers import adding_group_router
from app.handlers.admin_menu.admin_adding.adding_homework_handlers import adding_homework_router

from app.handlers.common_settings import *

admin_menu_router = Router()
admin_menu_router.include_router(adding_word_router)
admin_menu_router.include_router(adding_coll_router)
admin_menu_router.include_router(adding_group_router)
admin_menu_router.include_router(adding_homework_router)
admin_menu_router.include_router(setting_scheme_router)
admin_menu_router.include_router(setting_colls_router)

from app.keyboards.menu_buttons import *

from app.keyboards.keyboard_builder import keyboard_builder

class MenuState(StatesGroup):
    current_menu_params = State()

main_menu_params = MenuStateParams(curr_call=CALL_MAIN_MENU,
                                   curr_menu=[[button_study_menu],
                                              [button_revision_menu],
                                              [button_homework_menu],
                                              [button_config_menu],
                                              [button_admin_menu]],
                                   curr_main_mess=MESS_MAIN_MENU)

study_menu_params = MenuStateParams(curr_call=CALL_STUDY_MENU,
                                    curr_menu=[[button_adding_menu],
                                               [button_setting_menu],
                                               [button_adm_menu_editing],
                                               [button_main_menu]],
                                    curr_main_mess=MESS_ADMIN_MENU)

admin_menu_params = MenuStateParams(curr_call=CALL_ADMIN_MENU,
                                    curr_menu=[[button_adding_menu],
                                               [button_setting_menu],
                                               [button_adm_menu_editing],
                                               [button_main_menu]],
                                    curr_main_mess=MESS_ADMIN_MENU)

setting_menu_params = MenuStateParams(curr_call=CALL_SETTING_MENU,
                                      curr_menu=[[button_set_scheme],
                                                 [button_set_coll],
                                                 [button_admin_menu, button_main_menu]],
                                      curr_main_mess=MESS_SETTING_MENU)


adding_menu_params = MenuStateParams(curr_call=CALL_ADDING_MENU,
                                     curr_menu=[[button_add_word],
                                                [button_add_coll],
                                                [button_add_test],
                                                [button_add_group],
                                                [button_add_homework],
                                                [button_admin_menu, button_main_menu]],
                                     curr_main_mess=MESS_ADDING_MENU)

@admin_menu_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext):

    print('start new')
    print('в экзекьюторе фсм сделать функцию вытаскивания колла в зависимости от способа кодировки колла клавиатуры')
    print('добавь обратный обрабочик чтобы группы тоже показывались при объединении ползователей, а может и не надо')
    print('сделай нормальный репрезент экзекютора')
    print('сделай проверку наличия кваргсов экзекьютора')
    print('сделать енум или множество карусельки, в который еще можно и функцию засунуть по листанию')
    print('поработай с функцией добавления элементов в принимающее множество, нужно объединить все 3')
    print('сделай проверку на наличие слова в базе')
    print('доработай прием текста')
    print('убери проверку на команду старт, настрой роутеры')
    print('закрой доступ к админке')
    # чистим стейт
    await state.clear()
    # проверяем пользователя и регистрируем при необходимости
    await set_user(message)

    message_text = main_menu_params.curr_main_mess
    reply_kb = await keyboard_builder(menu_pack=main_menu_params.curr_menu, buttons_base_call="")
    await message_answer(source=message, message_text=message_text, reply_markup=reply_kb)

@admin_menu_router.callback_query(F.data == CALL_MAIN_MENU)
@admin_menu_router.callback_query(F.data == CALL_ADMIN_MENU)
@admin_menu_router.callback_query(F.data == CALL_ADDING_MENU)
@admin_menu_router.callback_query(F.data == CALL_SETTING_MENU)
async def admin_menu_setting_button(call: CallbackQuery, state: FSMContext):

    if call.data == CALL_MAIN_MENU:
        current_state_params = main_menu_params
    elif call.data == CALL_ADMIN_MENU:
        current_state_params = admin_menu_params
    elif call.data == CALL_SETTING_MENU:
        current_state_params = setting_menu_params
    elif call.data == CALL_ADDING_MENU:
        current_state_params = adding_menu_params
    else:
        current_state_params = main_menu_params

    await state.clear()
    await state.update_data(current_menu_params=current_state_params)
    await state.set_state(MenuState.current_menu_params)

    message_text = current_state_params.curr_main_mess
    reply_kb = await keyboard_builder(menu_pack=current_state_params.curr_menu, buttons_base_call="")

    await message_answer(source=call, message_text=message_text, reply_markup=reply_kb)
    await call.answer()


@admin_menu_router.message(F.text, MenuState.current_menu_params)
async def admin_menu_setting_button(message: Message, state: FSMContext):

    current_state_params: MenuStateParams = await state.get_value('current_menu_params')
    message_text = f'{message.text}?\n{current_state_params.curr_main_mess}'
    reply_kb = await keyboard_builder(menu_pack=current_state_params.curr_menu, buttons_base_call="")
    await message_answer(source=message, message_text=message_text, reply_markup=reply_kb)

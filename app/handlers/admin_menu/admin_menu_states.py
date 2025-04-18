from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from app.keyboards.keyboard_builder import keyboard_builder
import data.admin_messages as amsg

from app.keyboards.menu_buttons import *

from app.handlers.common_settings import *

class MenuState(StatesGroup):
    set_task_menu = State()
    admin_menu = State()
    add_any_menu = State()
    menu = State()

class MenuCallSet:
    def __init__(self):
        self.message_text = None
        self.reply_kb = None

    # здесь по сути решается движуха по меню
    async def set(self, fsm_call: CallbackQuery, fsm_state: FSMContext):
        fsm_state_str = await fsm_state.get_state()
        if fsm_call.data == amsg.ADMIN_MENU_BUTTON_TEXT:
            await fsm_state.set_state(MenuState.admin_menu)
            self.message_text = M_ADM_MENU
            menu_adm_menu = [[button_adm_menu_adding],
                                [button_adm_menu_setting],
                                [button_adm_menu_editing],
                                [button_common_main_menu]]
            self.reply_kb = await keyboard_builder(menu_pack=menu_adm_menu, buttons_base_call="")

        elif fsm_call.data == C_ADM_MENU_SETTING:
            await fsm_state.set_state(MenuState.set_task_menu)
            self.message_text = M_ADM_SETTING
            menu_adm_setting = [[button_adm_set_scheme],
                                [button_adm_set_coll],
                                [button_common_main_menu]]
            self.reply_kb = await keyboard_builder(menu_pack=menu_adm_setting, buttons_base_call="")

        elif fsm_call.data == C_ADM_MENU_ADDING:
            await fsm_state.set_state(MenuState.add_any_menu)
            self.message_text = M_ADM_ADDING
            menu_adm_setting = [[button_adm_add_word]]
            self.reply_kb = await keyboard_builder(menu_pack=menu_adm_setting, buttons_base_call="")


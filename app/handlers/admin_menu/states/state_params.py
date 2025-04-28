from typing import List, Optional
from aiogram.types import InlineKeyboardButton
from typing import Any
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
# import app.utils.admin_utils as aut
from app.keyboards.keyboard_builder import keyboard_builder
from app.handlers.common_settings import *
from app.handlers.common_settings import *
from app.utils.admin_utils import (update_button_list_with_check, get_new_carousel_page_num,
                                   get_current_carousel_page_num, add_item_in_aim_set_plus_minus,
                                   add_item_in_only_one_aim_set)
# , update_state_params_with_input_message)
from app.database.requests import set_group, get_users_by_filters

class InputStateParams:
    def __init__(self, self_state: State,
                 menu_add : list,
                 call_base: str = None,
                 call_add_capture: str = None,
                 state_main_mess: str = None,
                 but_change_text: str = None,
                 is_last_state_with_changing_mode: bool = False,
                 # необязательные
                 is_can_be_empty: bool = False,
                 next_state: State = None,
                 items_kb_list : list = None,
                 buttons_kb_list: Optional[List[InlineKeyboardButton]] = None,
                 items_kb_cols : int = None,
                 items_kb_rows : int = None,
                 items_kb_check : str = None,
                 is_only_one : bool = False,
                 is_input: bool = False
                 ):

        # это вводимые значения - либо элемент либо множество для кнопок выбора, изначально - пусто
        self.input_text : str | None = None
        self.captured_items_set = set()
        self.media_id : str | None = None
        self.media_type : str | None = None
        self.is_input: bool = is_input
        self.self_state : State = self_state #
        self.call_base : str = call_base #
        self.call_add_capture : str = call_add_capture #
        self.is_last_state_with_changing_mode: bool = is_last_state_with_changing_mode  #
        self.menu_add : list = menu_add #
        # это тексты основного сообщения при вводе, текст кнопки изменения и текст кнопки подтверждения ввода
        self.state_main_mess: str = state_main_mess #
        self.but_change_text: str = but_change_text #
        # может ли быть пустое значение при вводе
        self.is_can_be_empty: bool = is_can_be_empty
        # какой стейт будет следующим и последним при вводе
        self.next_state: State = next_state
        # конец блока - какой стейт будет следующим и последним при вводе
        # для клавиатуры выбора - необязательные
        self.items_kb_list : list = items_kb_list
        self.buttons_kb_list: List[InlineKeyboardButton] = buttons_kb_list
        self.items_kb_cols : int = items_kb_cols
        self.items_kb_rows : int = items_kb_rows
        self.items_kb_check : str = items_kb_check
        self.is_only_one : bool = is_only_one # выбор только одного элемента
        self.is_input : bool = is_input

    def change_call_to_changing(self):
        pass
        # self.call_add_capture = self.call_add_change
        # return self

    def __repr__(self):
        presentation = (f'$$$$$$$\n'
                f'текущий стейт - - {self.self_state}\n'
                f'введенный элемент - {self.input_text}\n'
                f'набор элементов - {self.captured_items_set}\n'
                f'$$$$$$$')

        return presentation


class ShowWordsStateParams(InputStateParams):
    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.call_add_capture : str = CALL_SHOW_WORDS
        self.state_main_mess : str = MESS_SHOW_WORDS
        self.items_kb_cols : int = NUM_SHOW_WORDS_COLS
        self.items_kb_rows : int = NUM_SHOW_WORDS_ROWS
        self.items_kb_check : str = CHECK_CAPTURE_WORDS


class CaptureWordsStateParams(InputStateParams):
    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.call_add_capture : str = CALL_CAPTURE_WORDS
        self.state_main_mess : str = MESS_CAPTURE_WORDS
        self.but_change_text : str  = BTEXT_CHANGE_WORDS
        self.items_kb_cols : int = NUM_CAPTURE_WORDS_COLS
        self.items_kb_rows : int = NUM_CAPTURE_WORDS_ROWS
        self.items_kb_check : str = CHECK_CAPTURE_WORDS


class CaptureCollsStateParams(InputStateParams):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.call_add_capture : str = CALL_CAPTURE_COLLS
        self.state_main_mess : str = MESS_CAPTURE_COLLS
        self.but_change_text : str  = BTEXT_CHANGE_COLLS
        self.items_kb_cols : int = NUM_CAPTURE_COLLS_COLS
        self.items_kb_rows : int = NUM_CAPTURE_COLLS_ROWS
        self.items_kb_check : str = CHECK_CAPTURE_COLLS


class CaptureGroupsStateParams(InputStateParams):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.call_add_capture : str = CALL_CAPTURE_GROUPS
        self.state_main_mess : str = MESS_CAPTURE_GROUPS
        self.but_change_text : str  = BTEXT_CHANGE_GROUPS
        self.items_kb_cols : int = NUM_CAPTURE_GROUPS_COLS
        self.items_kb_rows : int = NUM_CAPTURE_GROUPS_ROWS
        self.items_kb_check : str = CHECK_CAPTURE_GROUPS

class CaptureHomeworksStateParams(InputStateParams):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.call_add_capture : str = CALL_CAPTURE_HOMEWORKS
        self.state_main_mess : str = MESS_CAPTURE_HOMEWORKS
        self.but_change_text : str  = BTEXT_CHANGE_HOMEWORKS
        self.items_kb_cols : int = NUM_CAPTURE_HOMEWORKS_COLS
        self.items_kb_rows : int = NUM_CAPTURE_HOMEWORKS_ROWS
        self.items_kb_check : str = CHECK_CAPTURE_HOMEWORKS

    async def update_state_kb_with_all_users(self, call_base):
        users_list = await get_users_by_filters()
        users_kb = []
        for user in users_list:
            curr_button = InlineKeyboardButton(text=f'{user.ident_name}',
                                               callback_data=f'{call_base}{user.id}')
            users_kb.append(curr_button)
        self.buttons_kb_list = users_kb

class CaptureUsersStateParams(InputStateParams):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.call_add_capture : str = CALL_CAPTURE_USERS
        self.state_main_mess : str = MESS_CAPTURE_USERS
        self.but_change_text : str  = BTEXT_CHANGE_USERS
        self.items_kb_cols : int = NUM_CAPTURE_USERS_COLS
        self.items_kb_rows : int = NUM_CAPTURE_USERS_ROWS
        self.items_kb_check : str = CHECK_CAPTURE_USERS

    async def update_state_call_base_and_kb_with_all_users(self, call_base):
        users_list = await get_users_by_filters()
        users_kb = []
        for user in users_list:
            curr_button = InlineKeyboardButton(text=f'{user.ident_name}',
                                               callback_data=f'{call_base}{user.id}')
            users_kb.append(curr_button)
        self.buttons_kb_list = users_kb
        self.call_base = call_base


class CaptureDatesStateParams(InputStateParams):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.call_add_capture : str = CALL_CAPTURE_DATES
        self.state_main_mess : str = MESS_CAPTURE_DATES
        self.but_change_text : str  = BTEXT_CHANGE_DATES
        self.items_kb_cols : int = NUM_CAPTURE_DATES_COLS
        self.items_kb_rows : int = NUM_CAPTURE_DATES_ROWS
        self.items_kb_check : str = CHECK_CAPTURE_DATES

class CapturePriorityStateParams(InputStateParams):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.call_add_capture : str = CALL_CAPTURE_PRIRITY
        self.state_main_mess : str = MESS_CAPTURE_PRIRITY
        self.but_change_text : str  = BTEXT_CHANGE_PRIRITY
        self.items_kb_cols : int = NUM_CAPTURE_PRIRITY_COLS
        self.items_kb_rows : int = NUM_CAPTURE_PRIRITY_ROWS
        self.items_kb_check : str = CHECK_CAPTURE_PRIRITY

class CaptureDaysStateParams(InputStateParams):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.call_add_capture : str = CALL_CAPTURE_DAYS
        self.state_main_mess : str = MESS_CAPTURE_DAYS
        self.but_change_text : str  = BTEXT_CHANGE_DAYS
        self.items_kb_cols : int = NUM_CAPTURE_DAYS_COLS
        self.items_kb_rows : int = NUM_CAPTURE_DAYS_ROWS
        self.items_kb_check : str = CHECK_CAPTURE_DAYS

class CapturePartsStateParams(InputStateParams):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.call_add_capture : str = CALL_CAPTURE_PARTS
        self.state_main_mess : str = MESS_CAPTURE_PARTS
        self.but_change_text : str  = BTEXT_CHANGE_PARTS
        self.items_kb_cols : int = NUM_CAPTURE_PARTS_COLS
        self.items_kb_rows : int = NUM_CAPTURE_PARTS_ROWS
        self.items_kb_check : str = CHECK_CAPTURE_PARTS

class CaptureLevelsStateParams(InputStateParams):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.call_add_capture : str = CALL_CAPTURE_LEVELS
        self.state_main_mess : str = MESS_CAPTURE_LEVELS
        self.but_change_text : str  = BTEXT_CHANGE_LEVELS
        self.items_kb_cols : int = NUM_CAPTURE_LEVELS_COLS
        self.items_kb_rows : int = NUM_CAPTURE_LEVELS_ROWS
        self.items_kb_check : str = CHECK_CAPTURE_LEVELS

    def update_state_kb_with_level_list(self, call_base):
        levels_kb = []
        for level in LEVELS_LIST:
            levels_kb.append(InlineKeyboardButton(text=level, callback_data=call_base+level))
        self.buttons_kb_list = levels_kb
        self.call_base = call_base

class ConfirmationStateParams(InputStateParams):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.call_add_capture : str = CALL_ADD_ENDING
        self.state_main_mess : str = MESS_ADD_ENDING

    def update_state_with_call_base(self, call_base):
        self.call_base = call_base

class CaptureSourcesStateParams(InputStateParams):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.call_add_capture : str = CALL_CAPTURE_SOURCES
        self.state_main_mess : str = MESS_CAPTURE_SOURCES
        self.but_change_text : str  = BTEXT_CHANGE_SOURCES
        self.items_kb_cols : int = NUM_CAPTURE_SOURCES_COLS
        self.items_kb_rows : int = NUM_CAPTURE_SOURCES_ROWS
        self.items_kb_check : str = CHECK_CAPTURE_SOURCES
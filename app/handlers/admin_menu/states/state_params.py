from typing import Optional
from aiogram.types import InlineKeyboardButton
from aiogram.fsm.state import State
from app.handlers.common_settings import *
from app.database.requests import get_users_by_filters, get_words_by_filters
from config import logger
from app.database.models import UserStatus


class InputStateParams:
    def __init__(self,
                 self_state: State,
                 menu_pack : list[list[InlineKeyboardButton]],
                 call_base: str,
                 main_mess: str,
                 # необязательные параменты клавиатуры
                 buttons_pack: Optional[list[InlineKeyboardButton]] = None,
                 buttons_cols: Optional[int] = None,
                 buttons_rows: Optional[int] = None,
                 buttons_check: Optional[str] = None,
                 # необязательные параметры для перехода в следующий State
                 next_state: Optional[State] = None,
                 # необязательные логические флаги
                 is_can_be_empty: bool = False,
                 is_only_one : bool = False,
                 is_last_state_with_changing_mode: bool = False,
                 is_input: bool = False
                 ) -> None:

        # Вводимые значения
        self.input_text : Optional[str] = None
        self.set_of_items: Optional[set] = set()
        self.media_id : Optional[str] = None
        self.media_type : Optional[str] = None

        # Параметры, передаваемые в функцию
        self.self_state = self_state #
        self.menu_pack = menu_pack  #
        self.call_base = call_base #
        self.main_mess = main_mess  #

        # Параменты набора кнопок клавиатуры
        self.buttons_pack = buttons_pack
        self.buttons_cols = buttons_cols
        self.buttons_rows = buttons_rows
        self.buttons_check = buttons_check

        # необязательный параметр для перехода в следующий State
        self.next_state = next_state

        # логические флаги
        self.is_can_be_empty = is_can_be_empty
        self.is_only_one = is_only_one  # выбор только одного элемента
        self.is_last_state_with_changing_mode = is_last_state_with_changing_mode  #
        self.is_input = is_input

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(state={self.self_state}, "
            f"menu_pack=<matrix of size {len(self.menu_pack)}x{max(len(row) for row in self.menu_pack) if self.menu_pack else 0}>, "
            f"call_base='{self.call_base}', "
            f"main_mess='{self.main_mess}', "
            f"buttons_pack={'present' if self.buttons_pack else 'absent'}, "
            f"buttons_cols={self.buttons_cols}, "
            f"buttons_rows={self.buttons_rows}, "
            f"buttons_check='{self.buttons_check or ''}', "
            f"next_state={'present' if self.next_state else 'absent'}, "
            f"input_text='{self.input_text or ''}', "
            f"media_id='{self.media_id or ''}', "
            f"media_type='{self.media_type or ''}', "
            f"is_can_be_empty={self.is_can_be_empty}, "
            f"is_only_one={self.is_only_one}, "
            f"is_last_state_with_changing_mode={self.is_last_state_with_changing_mode}, "
            f"is_input={self.is_input})"
        )


class CaptureUsersStateParams(InputStateParams):
    # Расширение родительского класса настройками для выбора слов

    def __init__(self, call_base: str, **kwargs):
        kwargs['call_base'] = call_base
        kwargs['main_mess'] = MESS_CAPTURE_USERS
        kwargs['buttons_cols'] = NUM_CAPTURE_USERS_COLS
        kwargs['buttons_rows'] = NUM_CAPTURE_USERS_ROWS
        kwargs['buttons_check'] = CHECK_CAPTURE_USERS
        super().__init__(**kwargs)

    async def update_state_kb(self, user_filter: str = 'all') -> None:
        """
        Обновляет пакет кнопок и базовый callback для выбора пользователей.
        Args:
            user_filter (str): Определяет фильтр для выбора пользователей.
        """
        # добавляет пакет кнопок и базовый колл для выбора пользователей
        try:
            if user_filter == 'active':
                users_list = await get_users_by_filters(status=UserStatus.ACTIVE)
            elif user_filter == 'all':
                users_list = await get_users_by_filters()
            elif user_filter == 'test':
                users_list = await get_users_by_filters(user_tg_id=1)
            else:
                logger.warning('Некорректный фильтр пользователей.')
                return

            if not users_list:
                self.main_mess = MESS_NO_USERS
                logger.warning('Список пользователей пуст. Кнопки не обновлены.')
                return

            # Формируем клавиатуру
            users_kb = [InlineKeyboardButton(text=f'{user.ident_name}', callback_data=f'{self.call_base}{user.id}')
                        for user in users_list]

            # Устанавливаем значение
            self.buttons_pack = users_kb
        except Exception as e:
            logger.error(f'Произошла ошибка при получении пользователей при обновлении класса CaptureUsersStateParams: {e}')


class ShowWordsStateParams(InputStateParams):
    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.main_mess : str = MESS_SHOW_WORDS
        self.buttons_cols : int = NUM_SHOW_WORDS_COLS
        self.buttons_rows : int = NUM_SHOW_WORDS_ROWS
        self.buttons_check : str = CHECK_CAPTURE_WORDS


class CaptureWordsStateParams(InputStateParams):
    # Расширение родительского класса настройками для выбора слов
    state_main_mess = MESS_CAPTURE_WORDS
    buttons_cols = NUM_CAPTURE_WORDS_COLS
    buttons_rows = NUM_CAPTURE_WORDS_ROWS
    buttons_check = CHECK_CAPTURE_WORDS

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def update_state_with_all_words(self, call_base: str) -> None:
        # добавляет пакет кнопок и базовый колл для выбора слов
        self.call_base = call_base
        try:
            words_list = await get_words_by_filters()
            if not words_list:
                return
            words_kb = [InlineKeyboardButton(text=f'{word.word}', callback_data=f'{call_base}{word.id}')
                        for word in words_list]
            # Переворачиваем список кнопок
            reversed_words_kb = words_kb[::-1]
            # Устанавливаем обновленные значения
            self.buttons_pack = reversed_words_kb
        except Exception as e:
            logger.info(f'Произошла ошибка при получении слов при обновлении класса CaptureWordsStateParams: {e}')
    

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
    # Расширение родительского класса настройками для выбора уровня
    def __init__(self, call_base: str, **kwargs):
        kwargs['call_base'] = call_base
        kwargs['main_mess'] = MESS_CAPTURE_LEVELS
        kwargs['buttons_cols'] = NUM_CAPTURE_LEVELS_COLS
        kwargs['buttons_rows'] = NUM_CAPTURE_LEVELS_ROWS
        kwargs['buttons_check'] = CHECK_CAPTURE_LEVELS
        levels_kb = [InlineKeyboardButton(text=f'{level}', callback_data=f'{call_base}{level}')
                     for level in LEVELS_LIST]
        kwargs['buttons_pack'] = levels_kb
        super().__init__(**kwargs)



class ConfirmationStateParams(InputStateParams):
    def __init__(self, call_base: str, **kwargs):
        kwargs['call_base'] = call_base
        kwargs['main_mess'] = MESS_ADD_ENDING
        super().__init__(**kwargs)


class CaptureSourcesStateParams(InputStateParams):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.call_add_capture : str = CALL_CAPTURE_SOURCES
        self.state_main_mess : str = MESS_CAPTURE_SOURCES
        self.but_change_text : str  = BTEXT_CHANGE_SOURCES
        self.items_kb_cols : int = NUM_CAPTURE_SOURCES_COLS
        self.items_kb_rows : int = NUM_CAPTURE_SOURCES_ROWS
        self.items_kb_check : str = CHECK_CAPTURE_SOURCES
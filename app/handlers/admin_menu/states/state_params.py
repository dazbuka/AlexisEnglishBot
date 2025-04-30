from typing import Optional
from aiogram.types import InlineKeyboardButton
from aiogram.fsm.state import State
from app.handlers.common_settings import *
from app.database.requests import get_users_by_filters, get_words_by_filters, get_sources_by_filters, \
    get_groups_by_filters, get_medias_by_filters
from config import logger
from app.database.models import UserStatus
from datetime import datetime, date, timedelta


class InputStateParams:
    def __init__(self,
                 self_state: State,
                 menu_pack : list[list[InlineKeyboardButton]],
                 call_base: str,
                 main_mess: str,
                 # необязательные параметры клавиатуры
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

    async def update_state_kb(self, users_filter: str = 'all') -> None:
        """
        Обновляет пакет кнопок и базовый callback для выбора пользователей.
        Args:
            users_filter (str): Определяет фильтр для выбора пользователей.
        """
        # добавляет пакет кнопок и базовый колл для выбора пользователей
        try:
            if users_filter == 'active':
                users_list = await get_users_by_filters(status=UserStatus.ACTIVE)
            elif users_filter == 'all':
                users_list = await get_users_by_filters()
            elif users_filter == 'test':
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
    def __init__(self, call_base: str, **kwargs):
        kwargs['call_base'] = call_base
        kwargs['main_mess'] = MESS_CAPTURE_WORDS
        kwargs['buttons_cols'] = NUM_CAPTURE_WORDS_COLS
        kwargs['buttons_rows'] = NUM_CAPTURE_WORDS_ROWS
        kwargs['buttons_check'] = CHECK_CAPTURE_WORDS
        super().__init__(**kwargs)

    async def update_state_kb(self, words_filter: str = 'all') -> None:
        """
        Обновляет пакет кнопок и базовый callback для выбора слов.
        Args:
            words_filter (str): Определяет фильтр для выбора слов.
        """
        try:
            if words_filter == 'all':
                words_list = await get_words_by_filters()
            else:
                logger.warning('Некорректный фильтр слов.')
                return

            if not words_list:
                self.main_mess = MESS_NO_WORDS
                logger.warning('Список слов пуст. Кнопки не обновлены.')
                return

            # Формируем клавиатуру
            words_kb = [
                InlineKeyboardButton(text=f'{word.word}', callback_data=f'{self.call_base}{word.id}')
                for word in words_list]

            words_kb_reversed = words_kb[::-1]
            # Устанавливаем значение
            self.buttons_pack = words_kb_reversed
        except Exception as e:
            logger.error(
                f'Произошла ошибка при получении слов при обновлении класса CaptureWordsStateParams: {e}')

class CaptureCollsStateParams(InputStateParams):
    # Расширение родительского класса настройками для выбора колокаций
    def __init__(self, call_base: str, **kwargs):
        kwargs['call_base'] = call_base
        kwargs['main_mess'] = MESS_CAPTURE_COLLS
        kwargs['buttons_cols'] = NUM_CAPTURE_COLLS_COLS
        kwargs['buttons_rows'] = NUM_CAPTURE_COLLS_ROWS
        kwargs['buttons_check'] = CHECK_CAPTURE_COLLS
        super().__init__(**kwargs)

    async def update_state_kb(self, colls_filter: str = 'all') -> None:
        """
        Обновляет пакет кнопок и базовый callback для выбора коллокаций.
        Args:
            colls_filter (str): Определяет фильтр для выбора коллокаций.
        """
        try:
            if colls_filter == 'all':
                colls_list = await get_medias_by_filters()
            elif colls_filter == 'media':
                colls_list = await get_medias_by_filters(media_only=True)
            else:
                logger.warning('Некорректный фильтр коллокаций.')
                return

            if not colls_list:
                self.main_mess = MESS_NO_COLLS
                logger.warning('Список коллокаций пуст. Кнопки не обновлены.')
                return

            # Формируем клавиатуру
            colls_kb = [
                InlineKeyboardButton(text=f'{coll.collocation}', callback_data=f'{self.call_base}{coll.id}')
                for coll in colls_list]

            colls_kb_reversed = colls_kb[::-1]

            # Устанавливаем значение
            self.buttons_pack = colls_kb_reversed
        except Exception as e:
            logger.error(
                f'Произошла ошибка при получении коллокаций при обновлении класса CaptureCollsStateParams: {e}')

class CaptureGroupsStateParams(InputStateParams):
    # Расширение родительского класса настройками для выбора групп
    def __init__(self, call_base: str, **kwargs):
        kwargs['call_base'] = call_base
        kwargs['main_mess'] = MESS_CAPTURE_GROUPS
        kwargs['buttons_cols'] = NUM_CAPTURE_GROUPS_COLS
        kwargs['buttons_rows'] = NUM_CAPTURE_GROUPS_ROWS
        kwargs['buttons_check'] = CHECK_CAPTURE_GROUPS
        super().__init__(**kwargs)

    async def update_state_kb(self, groups_filter: str = 'all') -> None:
        """
        Обновляет пакет кнопок и базовый callback для выбора групп.
        Args:
            groups_filter (str): Определяет фильтр для выбора групп.
        """
        try:
            if groups_filter == 'all':
                groups_list = await get_groups_by_filters()
            else:
                logger.warning('Некорректный фильтр групп.')
                return

            if not groups_list:
                self.main_mess = MESS_NO_WORDS
                logger.warning('Список групп пуст. Кнопки не обновлены.')
                return

            # Формируем клавиатуру
            groups_kb = [
                InlineKeyboardButton(text=f'{group.name}', callback_data=f'{self.call_base}{group.id}')
                for group in groups_list]

            # Устанавливаем значение
            self.buttons_pack = groups_kb
        except Exception as e:
            logger.error(
                f'Произошла ошибка при получении групп при обновлении класса CaptureGroupsStateParams: {e}')

class CaptureHomeworksStateParams(InputStateParams):
    # Расширение родительского класса настройками для выбора домашнего задания
    def __init__(self, call_base: str, **kwargs):
        kwargs['call_base'] = call_base
        kwargs['main_mess'] = MESS_CAPTURE_HOMEWORKS
        kwargs['buttons_cols'] = NUM_CAPTURE_HOMEWORKS_COLS
        kwargs['buttons_rows'] = NUM_CAPTURE_HOMEWORKS_ROWS
        kwargs['buttons_check'] = CHECK_CAPTURE_HOMEWORKS
        super().__init__(**kwargs)

    async def update_state_kb(self, homeworks_filter: str = 'all') -> None:
        """
        Обновляет пакет кнопок и базовый callback для выбора домашних заданий.
        Args:
            homeworks_filter (str): Определяет фильтр для выбора домашних заданий.
        """
        try:
            if homeworks_filter == 'all':
                homeworks_list = await get_groups_by_filters()
            elif homeworks_filter == 'actual':
                homeworks_list = await get_groups_by_filters()
            else:
                logger.warning('Некорректный фильтр домашних заданий.')
                return

            if not homeworks_list:
                self.main_mess = MESS_NO_HOMEWORKS
                logger.warning('Список домашних заданий пуст. Кнопки не обновлены.')
                return

            # Формируем клавиатуру
            homeworks_kb = [
                InlineKeyboardButton(text=f'{homework.hometask}', callback_data=f'{self.call_base}{homework.id}')
                for homework in homeworks_list]

            # Устанавливаем значение
            self.buttons_pack = homeworks_kb
        except Exception as e:
            logger.error(
                f'Произошла ошибка при получении групп при обновлении класса CaptureHomeworksStateParams: {e}')

class CaptureDatesStateParams(InputStateParams):
    # Расширение родительского класса настройками для выбора даты
    def __init__(self, call_base: str, **kwargs):
        kwargs['call_base'] = call_base
        kwargs['main_mess'] = MESS_CAPTURE_DATES
        kwargs['buttons_cols'] = NUM_CAPTURE_DATES_COLS
        kwargs['buttons_rows'] = NUM_CAPTURE_DATES_ROWS
        kwargs['buttons_check'] = CHECK_CAPTURE_DATES
        kwargs['buttons_pack'] = [
            InlineKeyboardButton(
            text=f'{(date.today() + timedelta(days=i)).strftime("%d.%m.%Y")}',
            callback_data=f'{call_base}{(date.today() + timedelta(days=i)).strftime("%d.%m.%Y")}'
                                )
                                  for i in range(1, 150)
                                 ]
        super().__init__(**kwargs)

class CapturePriorityStateParams(InputStateParams):
    # Расширение родительского класса настройками для выбора приоритета
    def __init__(self, call_base: str, **kwargs):
        kwargs['call_base'] = call_base
        kwargs['main_mess'] = MESS_CAPTURE_PRIRITY
        kwargs['buttons_cols'] = NUM_CAPTURE_PRIRITY_COLS
        kwargs['buttons_rows'] = NUM_CAPTURE_PRIRITY_ROWS
        kwargs['buttons_check'] = CHECK_CAPTURE_PRIRITY
        kwargs['buttons_pack'] = [InlineKeyboardButton(text=f'{priority}', callback_data=f'{call_base}{priority}')
                                  for priority in range(1,11)]
        super().__init__(**kwargs)

class CaptureDaysStateParams(InputStateParams):
    # Расширение родительского класса настройками для выбора дня
    def __init__(self, call_base: str, **kwargs):
        kwargs['call_base'] = call_base
        kwargs['main_mess'] = MESS_CAPTURE_DAYS
        kwargs['buttons_cols'] = NUM_CAPTURE_DAYS_COLS
        kwargs['buttons_rows'] = NUM_CAPTURE_DAYS_ROWS
        kwargs['buttons_check'] = CHECK_CAPTURE_DAYS
        kwargs['buttons_pack'] = [InlineKeyboardButton(text=f'{day}', callback_data=f'{call_base}{day}')
                                  for day in range(150)]
        super().__init__(**kwargs)

class CapturePartsStateParams(InputStateParams):
    # Расширение родительского класса настройками для выбора части речи
    def __init__(self, call_base: str, **kwargs):
        kwargs['call_base'] = call_base
        kwargs['main_mess'] = MESS_CAPTURE_PARTS
        kwargs['buttons_cols'] = NUM_CAPTURE_PARTS_COLS
        kwargs['buttons_rows'] = NUM_CAPTURE_PARTS_ROWS
        kwargs['buttons_check'] = CHECK_CAPTURE_PARTS
        parts_kb = [InlineKeyboardButton(text=f'{part}', callback_data=f'{call_base}{part}')
                     for part in PARTS_LIST]
        kwargs['buttons_pack'] = parts_kb
        super().__init__(**kwargs)

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
    # Расширение родительского класса настройками для стейта подтверждения ввода
    def __init__(self, call_base: str, **kwargs):
        kwargs['call_base'] = call_base
        kwargs['main_mess'] = MESS_ADD_ENDING
        super().__init__(**kwargs)

class CaptureSourcesStateParams(InputStateParams):
    # Расширение родительского класса настройками для выбора источников
    def __init__(self, call_base: str, **kwargs):
        kwargs['call_base'] = call_base
        kwargs['main_mess'] = MESS_CAPTURE_SOURCES
        kwargs['buttons_cols'] = NUM_CAPTURE_SOURCES_COLS
        kwargs['buttons_rows'] = NUM_CAPTURE_SOURCES_ROWS
        kwargs['buttons_check'] = CHECK_CAPTURE_SOURCES
        super().__init__(**kwargs)

    async def update_state_kb(self, sources_filter: str = 'all') -> None:
        """
        Обновляет пакет кнопок и базовый callback для выбора источника.
        Args:
            sources_filter (str): Определяет фильтр для выбора источников.
        """
        # добавляет пакет кнопок и базовый колл для выбора пользователей
        try:
            if sources_filter == 'all':
                sources_list = await get_sources_by_filters()
            else:
                logger.warning('Некорректный фильтр источника.')
                return

            if not sources_list:
                self.main_mess = MESS_NO_SOURCES
                logger.warning('Список источников пуст. Кнопки не обновлены.')
                return

            # Формируем клавиатуру
            sources_kb = [InlineKeyboardButton(text=f'{source.source_name}', callback_data=f'{self.call_base}{source.id}')
                        for source in sources_list]

            # Устанавливаем значение
            self.buttons_pack = sources_kb
        except Exception as e:
            logger.error(f'Произошла ошибка при получении источников при обновлении класса CaptureSourcesStateParams: {e}')


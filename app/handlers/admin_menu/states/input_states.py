from typing import Any
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
import app.utils.admin_utils as aut
from app.keyboards.keyboard_builder import keyboard_builder
from app.handlers.common_settings import *
from app.handlers.common_settings import *

class StateParams:
    def __init__(self, self_state: State,
                 call_base : str,
                 menu_add : list,
                 call_add_capture: str = None,
                 state_main_mess: str = None,
                 but_change_text: str = None,
                 is_last_state_with_changing_mode: bool = False,
                 # необязательные
                 is_can_be_empty: bool = False,
                 next_state: State = None,
                 items_kb_list : list = None,
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
                f'выбранный элемент - {self.input_text}\n'
                f'набор элементов - {self.captured_items_set}\n'
                f'$$$$$$$')

        return presentation

class CaptureWordsStateParams(StateParams):
    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.call_add_capture : str = CALL_CAPTURE_WORDS
        self.state_main_mess : str = MESS_CAPTURE_WORDS
        self.but_change_text : str  = BTEXT_CHANGE_WORDS
        self.items_kb_cols : int = NUM_CAPTURE_WORDS_COLS
        self.items_kb_rows : int = NUM_CAPTURE_WORDS_ROWS
        self.items_kb_check : str = CHECK_CAPTURE_WORDS


class CaptureCollsStateParams(StateParams):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.call_add_capture : str = CALL_CAPTURE_COLLS
        self.state_main_mess : str = MESS_CAPTURE_COLLS
        self.but_change_text : str  = BTEXT_CHANGE_COLLS
        self.items_kb_cols : int = NUM_CAPTURE_COLLS_COLS
        self.items_kb_rows : int = NUM_CAPTURE_COLLS_ROWS
        self.items_kb_check : str = CHECK_CAPTURE_COLLS


class CaptureGroupsStateParams(StateParams):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.call_add_capture : str = CALL_CAPTURE_GROUPS
        self.state_main_mess : str = MESS_CAPTURE_GROUPS
        self.but_change_text : str  = BTEXT_CHANGE_GROUPS
        self.items_kb_cols : int = NUM_CAPTURE_GROUPS_COLS
        self.items_kb_rows : int = NUM_CAPTURE_GROUPS_ROWS
        self.items_kb_check : str = CHECK_CAPTURE_GROUPS

class CaptureUsersStateParams(StateParams):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.call_add_capture : str = CALL_CAPTURE_USERS
        self.state_main_mess : str = MESS_CAPTURE_USERS
        self.but_change_text : str  = BTEXT_CHANGE_USERS
        self.items_kb_cols : int = NUM_CAPTURE_USERS_COLS
        self.items_kb_rows : int = NUM_CAPTURE_USERS_ROWS
        self.items_kb_check : str = CHECK_CAPTURE_USERS

class CaptureDatesStateParams(StateParams):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.call_add_capture : str = CALL_CAPTURE_DATES
        self.state_main_mess : str = MESS_CAPTURE_DATES
        self.but_change_text : str  = BTEXT_CHANGE_DATES
        self.items_kb_cols : int = NUM_CAPTURE_DATES_COLS
        self.items_kb_rows : int = NUM_CAPTURE_DATES_ROWS
        self.items_kb_check : str = CHECK_CAPTURE_DATES

class CapturePriorityStateParams(StateParams):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.call_add_capture : str = CALL_CAPTURE_PRIRITY
        self.state_main_mess : str = MESS_CAPTURE_PRIRITY
        self.but_change_text : str  = BTEXT_CHANGE_PRIRITY
        self.items_kb_cols : int = NUM_CAPTURE_PRIRITY_COLS
        self.items_kb_rows : int = NUM_CAPTURE_PRIRITY_ROWS
        self.items_kb_check : str = CHECK_CAPTURE_PRIRITY

class CaptureDaysStateParams(StateParams):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.call_add_capture : str = CALL_CAPTURE_DAYS
        self.state_main_mess : str = MESS_CAPTURE_DAYS
        self.but_change_text : str  = BTEXT_CHANGE_DAYS
        self.items_kb_cols : int = NUM_CAPTURE_DAYS_COLS
        self.items_kb_rows : int = NUM_CAPTURE_DAYS_ROWS
        self.items_kb_check : str = CHECK_CAPTURE_DAYS

class CapturePartsStateParams(StateParams):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.call_add_capture : str = CALL_CAPTURE_PARTS
        self.state_main_mess : str = MESS_CAPTURE_PARTS
        self.but_change_text : str  = BTEXT_CHANGE_PARTS
        self.items_kb_cols : int = NUM_CAPTURE_PARTS_COLS
        self.items_kb_rows : int = NUM_CAPTURE_PARTS_ROWS
        self.items_kb_check : str = CHECK_CAPTURE_PARTS

class CaptureLevelsStateParams(StateParams):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.call_add_capture : str = CALL_CAPTURE_LEVELS
        self.state_main_mess : str = MESS_CAPTURE_LEVELS
        self.but_change_text : str  = BTEXT_CHANGE_LEVELS
        self.items_kb_cols : int = NUM_CAPTURE_LEVELS_COLS
        self.items_kb_rows : int = NUM_CAPTURE_LEVELS_ROWS
        self.items_kb_check : str = CHECK_CAPTURE_LEVELS

class CaptureSourcesStateParams(StateParams):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.call_add_capture : str = CALL_CAPTURE_SOURCES
        self.state_main_mess : str = MESS_CAPTURE_SOURCES
        self.but_change_text : str  = BTEXT_CHANGE_SOURCES
        self.items_kb_cols : int = NUM_CAPTURE_SOURCES_COLS
        self.items_kb_rows : int = NUM_CAPTURE_SOURCES_ROWS
        self.items_kb_check : str = CHECK_CAPTURE_SOURCES

class FSMExecutor:
    def __init__(self):
        self.message_text = None
        self.reply_kb = None
        self.media_type = None
        self.media_id = None

    async def execute(self, fsm_state: FSMContext, fsm_call: CallbackQuery = None, fsm_mess: Message = None):
        fsm_state_str = await fsm_state.get_state()
        current_state = fsm_state_str.split(':', 1)[1]
        current_state_params: StateParams = await fsm_state.get_value(current_state)
        print(fsm_state_str, end=' -> ')
        next_state_str = current_state_params.next_state.state
        next_state = next_state_str.split(':', 1)[1]
        next_state_params: StateParams = await fsm_state.get_value(next_state)
        print(next_state_str)
        # сначала обработчик для колла, заодно проверяем чтобы не было мессаджа
        if fsm_call and not fsm_mess:
            # вытаскиваем колл и убираем из него базовый и добавочный колл (заменяем на пусто)
            item_call = fsm_call.data.replace(current_state_params.call_base, '')
            item_call = item_call.replace(current_state_params.call_add_capture, '')
            # самый первый проверочный иф проверяет если текущий стейт - подтверждение всего ввода и будет
            # переход на изменение элементов, в этом случае следуюзий стейт будет преходом, а не цикличиным
            # как обыно, при этом номер страницы мы находим исходя из первого добавленного элемента
            if current_state_params.is_last_state_with_changing_mode:
                # if next_state_params.call_add_change == next_state_params.call_add_capture:
                print('c1', end='-')
                absolute_next_state = next_state_params
                if next_state_params.is_input:
                    page_num_common = 0
                else:
                    if absolute_next_state.captured_items_set:
                        last_item = list(absolute_next_state.captured_items_set)[-1]
                        page_num_common = await aut.get_current_carousel_page_num(item=last_item,
                                                                                  items_kb=absolute_next_state.items_kb_list,
                                                                                  rows=absolute_next_state.items_kb_rows,
                                                                                  cols=absolute_next_state.items_kb_cols)
                    else:
                        page_num_common = 0
                # если нажата кнопка подтверждения на клавиатуре
            elif CALL_CONFIRM in item_call:
                print('c2', end='-')

                # если список элементов пустой и дальше пропускать нельзя - зацикливаемся в этом же стейте выбора
                # элементов, при этом сообщение меняем на ничего не выбрано туда - обратно
                if not current_state_params.captured_items_set and not current_state_params.is_can_be_empty:
                    print('c3', end='-')
                    # выводим сообщение, чередуем, чтобы не было ошибки "невозможно редактировать"
                    if fsm_call.message.caption:
                        common_mess = fsm_call.message.caption
                    else:
                        common_mess = fsm_call.message.text

                    if current_state_params.state_main_mess in common_mess:
                        current_state_params.state_main_mess = MESS_NULL_CHOOSING
                    absolute_next_state = current_state_params
                # во всех остальных случаях переходим в следущюий стейт
                else:
                    print('c4', end='-')
                    absolute_next_state = next_state_params
                page_num_common = 0
                # проверяем на случай если нажата кнопка карусельки
            # если работает каруселька по перемещению между страницами, абсолютный некст будет текущим, страница
            # определяется в зависимости от нажатой карусельки
            elif (item_call.startswith(CALL_NEXT) or item_call.startswith(CALL_LAST) or
                    item_call.startswith(CALL_PREV) or item_call.startswith(CALL_FIRST)):
                print('c5', end='-')

                #
                absolute_next_state = current_state_params
                page_num_common = await aut.get_new_carousel_page_num(call_item=item_call,
                                                                      items_kb=absolute_next_state.items_kb_list,
                                                                      rows=absolute_next_state.items_kb_rows,
                                                                      cols=absolute_next_state.items_kb_cols)
            # если не было подтверждения, а была нажата кнопка элемента на клавиатуре не конфирм и не каруселька
            else:
                print('c6', end='-')
                # убираем чеки из колла, если они вообще заданы
                if current_state_params.items_kb_check:
                    item_call = item_call.replace(current_state_params.items_kb_check, '')
                # из получившегося остатка колла"111-слово" оставляем только цифры
                added_item = item_call.split('-', 1)[0]
                # добавляем его в множество выбранных слов и записываем в стейт
                # проверяем может ли быть один - тогда просто симметрично добавляем (это для групп, например)
                # елси не может быть один - тогда обновляем просто
                if added_item:
                    if not current_state_params.is_only_one:
                        print('с7', end='-')
                        # добавляем элементы
                        current_state_params.captured_items_set = await aut.add_item_in_aim_set_plus_minus(
                                                                aim_set=current_state_params.captured_items_set,
                                                                added_item=added_item)
                    else:
                        print('с8', end='-')

                        current_state_params.captured_items_set = await aut.add_item_in_only_one_aim_set(
                                                                aim_set=current_state_params.captured_items_set,
                                                                added_item=added_item)
                else:
                    print('какая-то проблема с раскодировкой added_item в лупе')
                # обновляем стейт после добавления элементов
                await fsm_state.update_data({current_state: current_state_params})
                # меняем сообщение на добавь еще
                current_state_params.state_main_mess = MESS_MORE_CHOOSING
                # остаемся в том же стейте
                absolute_next_state = current_state_params
                # вычисляем номер текущей страницы, на которой находится слово, чтобы остаться на ней
                page_num_common = await aut.get_current_carousel_page_num(item=added_item,
                                                                          items_kb=absolute_next_state.items_kb_list,
                                                                          rows=absolute_next_state.items_kb_rows,
                                                                          cols=absolute_next_state.items_kb_cols)
            if not absolute_next_state.is_input:
                absolute_next_kb_items_list = await aut.set_check_in_button_list(
                    button_list=absolute_next_state.items_kb_list,
                    aim_set=absolute_next_state.captured_items_set,
                    check=absolute_next_state.items_kb_check)
            else:
                absolute_next_kb_items_list = []


        elif fsm_mess and not fsm_call:
            fsm_state_str = await fsm_state.get_state()
            print('m1', end='-')

            if current_state_params.is_input:
                print('m2', end='-')

                # при нажатии на старт - пока не обнуляется стейт и принимает пустое слово
                if fsm_mess.text != '/start':

                    absolute_next_state = next_state_params

                    current_state_params = aut.update_state_params_with_input_message(message=fsm_mess,
                                                                                      state_params=current_state_params)

                    await fsm_state.update_data({current_state: current_state_params})

                else:
                    print('не переходит дальше, ждет ввода')
                    absolute_next_state = current_state_params
                # print(absolute_next_state)
                new_absolute_next_kb_items_list = absolute_next_state.items_kb_list
                # print(new_absolute_next_kb_items_list)

            # это если мы используем мессаж для поиска среди клавиатуры и остаемся в том же стейте
            elif not current_state_params.is_input and current_state_params.items_kb_list:
                print('m3', end='-')
                absolute_next_state = current_state_params
                new_absolute_next_kb_items_list = []
                for item in absolute_next_state.items_kb_list:
                    if fsm_mess.text.lower() in item.lower():
                        new_absolute_next_kb_items_list.append(item)

            else:
                print('ЕРРОР m4')
                absolute_next_state = next_state_params
                new_absolute_next_kb_items_list = absolute_next_state.items_kb_list

                added_item = fsm_mess.text.lower()
                current_state_params.input_text = added_item
                await fsm_state.update_data({current_state: current_state_params})

            absolute_next_kb_items_list = await aut.set_check_in_button_list(
                button_list=new_absolute_next_kb_items_list,
                aim_set=absolute_next_state.captured_items_set,
                check=absolute_next_state.items_kb_check)
            page_num_common = 0


        else:
            print('ERROR!!! стейтпарамс обработчик')
            absolute_next_state = None
            absolute_next_kb_items_list = None
            page_num_common = 0



        print('cm end')

        self.media_type = absolute_next_state.media_type
        self.media_id = absolute_next_state.media_id

        self.message_text = absolute_next_state.state_main_mess
        self.reply_kb = await keyboard_builder(menu_pack=absolute_next_state.menu_add,
                                               buttons_add_list=absolute_next_kb_items_list,
                                               buttons_base_call=absolute_next_state.call_base + absolute_next_state.call_add_capture,
                                               buttons_add_cols=absolute_next_state.items_kb_cols,
                                               buttons_add_rows=absolute_next_state.items_kb_rows,
                                               is_adding_confirm_button=not absolute_next_state.is_input,
                                               buttons_add_table_number=page_num_common)
        # возвращаемся в тот же стейт добавления слов
        await fsm_state.set_state(absolute_next_state.self_state)




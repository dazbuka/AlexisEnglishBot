from typing import Any
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
import app.utils.admin_utils as aut
from app.keyboards.keyboard_builder import keyboard_builder
from app.handlers.common_settings import (CALL_CHANGE_WORD, CALL_CHANGE_USER, CALL_CHANGE_DATE,
                                          CALL_CONFIRM, MESS_MORE_CHOOSING, MESS_NULL_CHOOSING, CALL_CHANGE_LEVEL)

from data.admin_messages import  (CALL_NEXT, CALL_LAST, CALL_PREV, CALL_FIRST)
# from app.handlers.common_settings import *
from app.handlers.common_settings import *

class StateParams:
    def __init__(self, self_state: State,
                 call_base : str,
                 menu_add : list,
                 call_add_capture: str = None,
                 state_main_mess: str = None,
                 but_change_text: str = None,
                 call_add_change: str = None,
                 # необязательные
                 is_can_be_empty: bool = False,
                 next_state: State = None,
                 items_kb_list : list = None,
                 items_kb_cols : int = None,
                 items_kb_rows : int = None,
                 items_kb_check : str = None,
                 is_only_one : bool = False
                 ):

        # это вводимые значения - либо элемент либо множество для кнопок выбора, изначально - пусто
        self.input_item : Any = None
        self.captured_items_set = set()
        self.self_state : State = self_state #
        self.call_base : str = call_base #
        self.call_add_capture : str = call_add_capture #
        self.call_add_change: str = call_add_change  #
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
        print('!---------------------------------------------------------------------------сделай нормальный репрезент')

    def change_call_to_changing(self):
        self.call_add_capture = self.call_add_change
        # return self

    def __repr__(self):
        repr = f'$$$$$$$ набор элементов - {self.captured_items_set} - $$$$$$$ - {self.call_add_capture}- $$$$$$$ - {self.self_state.state}'

        return repr


class CaptureWordsStateParams(StateParams):
    def __init__(self, **kwargs):
        print('-----------------------------------------------------------------------сделай проверку наличия кваргсов')
        super().__init__(**kwargs)
        self.call_add_capture : str = CALL_CAPTURE_WORD
        self.call_add_change : str = CALL_CHANGE_WORD
        self.state_main_mess : str = MESS_CAPTURE_WORD
        self.but_change_text : str  = TEXT_CHANGE_WORD
        self.items_kb_cols : str = NUM_CAPTURE_WORD_COLS
        self.items_kb_rows : str = NUM_CAPTURE_WORD_ROWS
        self.items_kb_check : str = CHECK_CAPTURE_WORD


class FSMCallSet:
    def __init__(self):
        self.message_text = None
        self.reply_kb = None

    async def execute(self, fsm_state: FSMContext, fsm_call: CallbackQuery, fsm_mess: Message = None):
        fsm_state_str = await fsm_state.get_state()
        current_state = fsm_state_str.split(':', 1)[1]
        current_state_params: StateParams = await fsm_state.get_value(current_state)

        next_state_str = current_state_params.next_state.state
        next_state = next_state_str.split(':', 1)[1]
        next_state_params: StateParams = await fsm_state.get_value(next_state)
        # сначала обработчик для колла, заодно проверяем чтобы не было мессаджа
        if fsm_call and not fsm_mess:
            print('1')
            # вытаксиваем колл и убераем из него базовый и добавочный колл (заменяем на пусто)
            item_call = fsm_call.data.replace(current_state_params.call_base, '')
            item_call = item_call.replace(current_state_params.call_add_capture, '')
            # если нажата кнопка подтверждения на клавиатуре
            print(CALL_CONFIRM)
            print(item_call)
            if CALL_CONFIRM in item_call:
                print('2')
                # проверяемя чтобы были выбраны значения и не стоял флаг что их множество может быть нулевым
                # в этом случае абсолютным следующим стейтом будет переход в следующий стейт по умолчанию
                if current_state_params.captured_items_set or current_state_params.is_can_be_empty:
                    # проставляем чеки для случая если
                    print('3')
                    absolute_next_state = next_state_params
                # если список элементов пустой и дальше пропускать нельзя - зацикливаемся в этом же стейте выбора
                # элементов, при этом сообщение меняем на ничего не выбрано туда - обратно
                else:
                    print('4')
                    # выводим сообщение, чередуем, чтобы не было ошибки "невозможно редактировать"
                    if current_state_params.state_main_mess in fsm_call.message.text:
                        current_state_params.state_main_mess = MESS_NULL_CHOOSING
                    absolute_next_state = current_state_params
                page_num_common = 0
                # проверяем на случай если нажата кнопка карусельки
            elif (item_call.startswith(CALL_NEXT) or item_call.startswith(CALL_LAST) or
                    item_call.startswith(CALL_PREV) or item_call.startswith(CALL_FIRST)):
                print('5')
                print('здесь во первый сделать нужно или енум или множестов, может даже класс, в который еще можно'
                      'и функцию засунуть по листанию')
                print('и вообще его нужно вынести из этого цикла выше на уровень')
                # абсолютный некст будет текущим
                absolute_next_state = current_state_params
                page_num_common = await aut.get_new_carousel_page_num(call=item_call,
                                                                      items_kb=absolute_next_state.items_kb_list,
                                                                      rows=absolute_next_state.items_kb_rows,
                                                                      cols=absolute_next_state.items_kb_cols)
            # если не было подтверждения, а была нажата кнопка элемента на клавиатуре не конфирм и не каруселька
            else:
                print('6')
                # убираем чеки из колла, если они вообще заданы
                if current_state_params.items_kb_check:
                    item_call = item_call.replace(current_state_params.items_kb_check, '')
                print('здесь можно сделать функцию в зависимости от способа кодировки клавиатуры')
                # из получившегося остатка колла"111-слово" оставляем только цифры
                added_item = item_call.split('-', 1)[0]
                # добавляем его в множество выбранных слов и записываем в стейт
                # проверяем может ли быть один - тогда просто симметрично добавляем (это для групп, например)
                # елси не может быть один - тогда обновляем просто
                if not current_state_params.is_only_one:
                    print('7')
                    # добавляем элементы
                    current_state_params.captured_items_set = await aut.add_item_in_aim_set_plus_minus(
                                                            aim_set=current_state_params.captured_items_set,
                                                            added_item=added_item)
                else:
                    print('8')
                    print('поработай с неу, эту функцию по идее нужно объединить, точнее все три объединить нужно')
                    current_state_params.captured_items_set = await aut.add_item_in_only_one_aim_set(
                                                            aim_set=current_state_params.captured_items_set,
                                                            added_item=added_item)
                # обновляем стейт после добавления элементов
                await fsm_state.update_data({current_state: current_state_params})
                # меняем сообщение на добавь еще
                print('предлагаю это сообщение на добавь еще внести в стейт')
                current_state_params.state_main_mess = MESS_MORE_CHOOSING
                # остаемся в том же стейте
                absolute_next_state = current_state_params
                # если замена после внеснеия - то меняем добавочный колл - это для случая, если мы находимся в
                # последнем стейте, и тогда нам нужно не остаться в нем, а перейти в замену элементов
                if next_state_params.call_add_change == next_state_params.call_add_capture:
                    print('11')
                    absolute_next_state = next_state_params
                # если следующий стейт имеет клавиатуру вычисляем номер текущей страницы,
                # на которой находится слово, чтобы остаться на ней

                page_num_common = await aut.get_current_carousel_page_num(item=added_item,
                                                                          items_kb=absolute_next_state.items_kb_list,
                                                                          rows=absolute_next_state.items_kb_rows,
                                                                          cols=absolute_next_state.items_kb_cols)
                # проставляем чеки в следующую клавиатуру

        absolute_next_kb_items_list = await aut.set_check_in_button_list(button_list=absolute_next_state.items_kb_list,
                                                                         aim_set=absolute_next_state.captured_items_set,
                                                                         check=absolute_next_state.items_kb_check)
        print('16')
        state_text = await aut.state_text_builder(fsm_state)
        self.message_text = state_text + '\n' + absolute_next_state.state_main_mess
        self.reply_kb = await keyboard_builder(menu_pack=absolute_next_state.menu_add,
                                               buttons_add_list=absolute_next_kb_items_list,
                                               buttons_base_call=absolute_next_state.call_base + absolute_next_state.call_add_capture,
                                               buttons_add_cols=absolute_next_state.items_kb_cols,
                                               buttons_add_rows=absolute_next_state.items_kb_rows,
                                               is_adding_confirm_button=True,
                                               buttons_add_table_number=page_num_common)
        # возвращаемся в тот же стейт добавления слов
        await fsm_state.set_state(absolute_next_state.self_state)


# класс для обработки текстового сообщения
class FSMMessageSet:
    def __init__(self):
        self.message_text = None
        self.reply_kb = None

    async def set(self, fsm_mess: Message, fsm_state: FSMContext):
        fsm_state_str = await fsm_state.get_state()
        # is_next_loop = True
        print(f'- - - - - - - {fsm_state_str} - - - - - - -')
        current_state_params : StateParams = await fsm_state.get_value('words_state')
        next_state_params: StateParams = await fsm_state.get_value('words_state')

        if current_state_params.items_kb_list and next_state_params.items_kb_list:
            items_kb_new = []
            for item in next_state_params.items_kb_list:
                if fsm_mess.text.lower() in item.lower():
                    items_kb_new.append(item)
        else:
            items_kb_new = next_state_params.items_kb_list
            added_item = fsm_mess.text.lower()
            current_state_params.input_item = added_item
            # это заработает, убери коммент
            # это заработает, убери коммент
            # это заработает, убери коммент
            # это заработает, убери коммент
            # это заработает, убери коммент
            # await fsm_state.update_data({current_state: current_state_params})
            # это заработает, убери коммент



            # await fsm_state.update_data({current_state_params.state_name: current_state_params}) - работало
            # await fsm_state.update_data({current_state_params.self_state.state: current_state_params})

        # проставляем чеки в список кнопок
        items_kb_new = await aut.set_check_in_button_list(button_list=items_kb_new,
                                                          aim_set=next_state_params.captured_items_set,
                                                          check=next_state_params.items_kb_check)
        # выводим заменой сообщения
        state_text = await aut.state_text_builder(fsm_state)
        self.message_text = state_text + '\n' + next_state_params.state_main_mess
        self.reply_kb = await keyboard_builder(menu_pack=next_state_params.menu_add,
                                               buttons_add_list=items_kb_new,
                                               buttons_base_call=next_state_params.call_base + next_state_params.call_add_capture,
                                               buttons_add_cols=next_state_params.items_kb_cols,
                                               buttons_add_rows= next_state_params.items_kb_rows,
                                               is_adding_confirm_button=True,
                                               buttons_add_table_number=0)
        await fsm_state.set_state(next_state_params.self_state)





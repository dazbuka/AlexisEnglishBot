from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.database.requests import get_users_by_filters, get_groups_by_filters
from app.utils.admin_utils import (message_answer,
                                   add_item_in_aim_set_plus_plus,
                                   get_word_list_for_kb_with_ids,
                                   get_group_list_for_kb_with_ids,
                                   get_user_list_for_kb_with_ids,
                                   get_date_list_for_kb,
                                   update_button_with_call_base,
                                   state_text_builder)
from aiogram.fsm.state import State, StatesGroup
# from app.handlers.admin_menu.input_states import AddWord, FSMInputMessageSet, InputStateParams

from app.handlers.admin_menu.loop_states import FSMMessageSet, StateParams, FSMCallSet

from app.keyboards.keyboard_builder import keyboard_builder
from app.keyboards.menu_buttons import (button_menu_setting_back, button_main_admin_menu, button_main_menu,
                                        button_change_word, button_change_user, button_change_date,
                                        button_menu_adding_back)
from app.handlers.common_settings import *


adding_word_router = Router()

class AddWord(StatesGroup):
    author_id = State() # автор который назначает задание - ид
    input_word_state = State()
    capture_level_state = State()
    input_definition = State()
    author = State()
    part = State()
    translation = State()
    confirmation_state = State()


# переход в меню добавления задания по схеме
@adding_word_router.callback_query(F.data == C_ADM_ADD_WORD)
async def adding_word_first_state(call: CallbackQuery, state: FSMContext):
    # очистка стейта
    print('here in adding word')
    await state.clear()

    menu_add_word = [
        [button_menu_adding_back, button_main_admin_menu, button_main_menu]
    ]

    menu_add_word_with_changing = [
        [update_button_with_call_base(button_change_word, CALL_ADD_WORD + CALL_ADD_ENDING),
         update_button_with_call_base(button_change_user, CALL_ADD_WORD + CALL_ADD_ENDING),
         update_button_with_call_base(button_change_date, CALL_ADD_WORD + CALL_ADD_ENDING)],
        [button_menu_setting_back, button_main_admin_menu, button_main_menu]
    ]



    # задаем в стейт ид автора
    author = await get_users_by_filters(user_tg_id=call.from_user.id)
    await state.update_data(author_id=author.id)

    # word_state = InputStateParams(self_state = AddWord.input_word_state,
    #                                base_call = CALL_ADD_WORD,
    #                                call_add = CALL_INPUT_WORD,
    #                                menu_add = menu_add_word,
    #                                state_kb_dict = word_state_dict)
    # print(word_state)
    # await state.update_data(word_state=word_state)

    word_state = StateParams(self_state = AddWord.input_word_state,
                             call_base= CALL_ADD_WORD,
                             call_add_capture= CALL_INPUT_WORD,
                             menu_add = menu_add_word,
                             state_kb_dict=word_state_dict)
    await state.update_data(input_word_state=word_state)

    levels_state = StateParams(self_state = AddWord.capture_level_state,
                               call_base= CALL_ADD_WORD,
                               call_add_capture= CALL_CAPTURE_LEVEL,
                               menu_add = menu_add_word,
                               items_kb_list=LEVEL_LIST,
                               state_kb_dict = levels_state_dict,
                               is_only_one=True)
    await state.update_data(capture_level_state=levels_state)

    first_state = word_state

    # переход в первый стейт
    await state.set_state(first_state.self_state)

    # формируем сообщение, меню, клавиатуру и выводим их

    await call.message.edit_text('vvedite')
    await call.answer()

@adding_word_router.message(F.text, AddWord.input_word_state)
async def admin_adding_word_capture_word(message: Message, state: FSMContext):
    # проверяем слово в базе данных
    # создаем экземпляр класса для обработки текущего состояния фсм
    current_fsm = FSMMessageSet()
    # обрабатываем экземпляра класса, который анализирует наш колл и выдает сообщение и клавиатуру
    await current_fsm.set(message, state)
    print('сделай проверку на наличие слова в базе')
    print('убери пустое слово в том числе при нажатии старт')
    await message_answer(source=message, message_text=current_fsm.message_text, reply_markup=current_fsm.reply_kb)

    # если оно там есть - пусть пробует снова
    # if await rq.get_words_by_filters(word=message.text.lower().strip()):
    #     message_text = amsg.ADM_ADD_WORD_WORD_FIND
    #     reply_kb = await akb.admin_adding_word_kb()
    #     await message_answer(source=message, message_text=message_text, reply_markup=reply_kb)
    #     await state.set_state(AddWord.word)
    # # если нет - запоминаем в стейт слово и ид юзера из бд
    # else:
    #     await state.update_data(word=message.text.lower().strip())
    #     user = await rq.get_users_by_filters(user_tg_id=message.from_user.id)
    #     await state.update_data(author=user.id)
    #     # приглашаем выбрать уровень слова
    #     state_text = await get_text_from_word_adding_state(state)
    #     message_text = f'{state_text}\n{amsg.ADM_ADD_WORD_LEVEL}'
    #     reply_kb = await akb.admin_adding_word_kb(adding_level=True)
    #     await message_answer(source=message, message_text=message_text, reply_markup=reply_kb)
    #     await state.set_state(AddWord.level)


@adding_word_router.callback_query(F.data.startswith(CALL_ADD_WORD + CALL_CAPTURE_LEVEL), AddWord.capture_level_state)
async def set_scheme_capture_words_from_call(call: CallbackQuery, state: FSMContext):
    # создаем экземпляр класса для обработки текущего состояния фсм
    current_fsm = FSMCallSet()
    # обрабатываем экземпляра класса, который анализирует наш колл и выдает сообщение и клавиатуру
    await current_fsm.execute(call, state)

    # отвечаем заменой сообщения
    await call.message.edit_text(current_fsm.message_text, reply_markup=current_fsm.reply_kb)
    await call.answer()
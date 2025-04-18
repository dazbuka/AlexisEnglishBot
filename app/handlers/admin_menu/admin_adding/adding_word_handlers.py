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
import data.admin_messages as amsg
import app.database.requests as rq
import app.keyboards.admin_keyboards as akb

# from app.handlers.admin_menu.input_states import AddWord, FSMInputMessageSet, InputStateParams

from app.handlers.admin_menu.loop_states import StateParams, FSMExecutor, CaptureLevelsStateParams, \
    CapturePartsStateParams

from app.keyboards.keyboard_builder import keyboard_builder
from app.keyboards.menu_buttons import (button_menu_setting_back, button_main_admin_menu, button_main_menu,
                                        button_change_word, button_change_user, button_change_date,
                                        button_menu_adding_back, button_change_level, button_change_part,
                                        button_change_translation, button_change_definition)
from app.handlers.common_settings import *


adding_word_router = Router()

class AddWord(StatesGroup):
    author_id = State() # автор который назначает задание - ид
    input_word_state = State()
    capture_parts_state = State()
    capture_levels_state = State()
    input_definition_state = State()
    input_translation_state = State()
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
         update_button_with_call_base(button_change_level, CALL_ADD_WORD + CALL_ADD_ENDING),
         update_button_with_call_base(button_change_part, CALL_ADD_WORD + CALL_ADD_ENDING)],
        [update_button_with_call_base(button_change_translation, CALL_ADD_WORD + CALL_ADD_ENDING),
         update_button_with_call_base(button_change_definition, CALL_ADD_WORD + CALL_ADD_ENDING)],
        [button_menu_setting_back, button_main_admin_menu, button_main_menu]
    ]

    # задаем в стейт ид автора
    author = await get_users_by_filters(user_tg_id=call.from_user.id)
    await state.update_data(author_id=author.id)

    word_state = StateParams(self_state = AddWord.input_word_state,
                             next_state = AddWord.capture_parts_state,
                             call_base= CALL_ADD_WORD,
                             call_add_capture= CALL_INPUT_WORD,
                             state_main_mess = MESS_INPUT_WORD,
                             but_change_text = TEXT_CHANGE_WORD,
                             menu_add = menu_add_word,
                             is_input=True)
    await state.update_data(input_word_state=word_state)


    parts_state = CapturePartsStateParams(self_state=AddWord.capture_parts_state,
                                           next_state=AddWord.capture_levels_state,
                                           call_base=CALL_ADD_WORD,
                                           menu_add=menu_add_word,
                                           items_kb_list=PART_LIST,
                                           is_can_be_empty=True,
                                           is_only_one=True)
    await state.update_data(capture_parts_state=parts_state)


    levels_state = CaptureLevelsStateParams(self_state=AddWord.capture_levels_state,
                                            next_state=AddWord.input_definition_state,
                                            call_base=CALL_ADD_WORD,
                                            menu_add=menu_add_word,
                                            items_kb_list=LEVEL_LIST,
                                            is_can_be_empty=True,
                                            is_only_one=True)
    await state.update_data(capture_levels_state=levels_state)

    definition_state = StateParams(self_state = AddWord.input_definition_state,
                                  next_state = AddWord.input_translation_state,
                                  call_base= CALL_ADD_WORD,
                                  call_add_capture= CALL_INPUT_DEFINITION,
                                  state_main_mess = MESS_INPUT_DEFINITION,
                                  but_change_text = TEXT_CHANGE_DEFINITION,
                                  menu_add = menu_add_word,
                                  is_input=True)
    await state.update_data(input_definition_state=definition_state)



    translation_state = StateParams(self_state = AddWord.input_translation_state,
                                  next_state = AddWord.confirmation_state,
                                  call_base= CALL_ADD_WORD,
                                  call_add_capture= CALL_INPUT_TRANSLATION,
                                  state_main_mess = MESS_INPUT_TRANSLATION,
                                  but_change_text = TEXT_CHANGE_TRANSLATION,
                                  menu_add = menu_add_word,
                                  is_input=True)
    await state.update_data(input_translation_state=translation_state)


    confirmation_state = StateParams(self_state = AddWord.confirmation_state,
                                     call_base = CALL_ADD_WORD,
                                     call_add_capture= CALL_ADD_ENDING,
                                     menu_add = menu_add_word_with_changing,
                                     state_main_mess=MESS_ADD_ENDING,
                                     is_last_state_with_changing_mode=True)
    await state.update_data(confirmation_state=confirmation_state)


    first_state = word_state

    # переход в первый стейт
    await state.set_state(first_state.self_state)

    # формируем сообщение, меню, клавиатуру и выводим их

    await call.message.edit_text('vvedite')
    await call.answer()


@adding_word_router.message(F.text, AddWord.input_word_state)
@adding_word_router.message(F.text, AddWord.capture_parts_state)
@adding_word_router.message(F.text, AddWord.capture_levels_state)
@adding_word_router.message(F.text, AddWord.input_definition_state)
@adding_word_router.message(F.text, AddWord.input_translation_state)
async def admin_adding_word_capture_word(message: Message, state: FSMContext):
    # проверяем слово в базе данных
    # создаем экземпляр класса для обработки текущего состояния фсм
    current_fsm = FSMExecutor()
    # обрабатываем экземпляра класса, который анализирует наш колл и выдает сообщение и клавиатуру
    await current_fsm.execute(fsm_state=state, fsm_mess=message)
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


@adding_word_router.callback_query(F.data.startswith(CALL_ADD_WORD + CALL_CAPTURE_PART), AddWord.capture_parts_state)
@adding_word_router.callback_query(F.data.startswith(CALL_ADD_WORD + CALL_CAPTURE_LEVEL), AddWord.capture_levels_state)
async def set_scheme_capture_words_from_call(call: CallbackQuery, state: FSMContext):
    # создаем экземпляр класса для обработки текущего состояния фсм
    current_fsm = FSMExecutor()
    # обрабатываем экземпляра класса, который анализирует наш колл и выдает сообщение и клавиатуру
    await current_fsm.execute(fsm_state=state, fsm_call=call)
    # отвечаем заменой сообщения
    await call.message.edit_text(current_fsm.message_text, reply_markup=current_fsm.reply_kb)
    await call.answer()


# конечный обработчик всего стейта
@adding_word_router.callback_query(F.data.startswith(CALL_ADD_WORD + CALL_ADD_ENDING), AddWord.confirmation_state)
async def admin_adding_task_capture_confirmation_from_call(call: CallbackQuery, state: FSMContext):
    # вытаскиваем из колбека уровень
    confirm = call.data.replace(CALL_ADD_WORD + CALL_ADD_ENDING, '')
    # уходим обратно если нужно что-то изменить

    if (confirm == CALL_CHANGING_WORD or confirm == CALL_CHANGING_PART or confirm == CALL_CHANGING_LEVEL
            or confirm == CALL_CHANGING_DEFINITION or confirm == CALL_CHANGING_TRANSLATION):
        confirmation_state: StateParams = await state.get_value('confirmation_state')
        print(confirm)
        print('111')
        if confirm == CALL_CHANGING_WORD:
            # при нажатии на изменение задаем следующий стейт элементов
            confirmation_state.next_state = AddWord.input_word_state
            # делаем так, чтобы в стейте добавления последний стейт (на изменения который) стал следующим
            input_word_state: StateParams = await state.get_value('input_word_state')
            input_word_state.next_state = AddWord.confirmation_state
            await state.update_data(input_word_state=input_word_state)

        elif confirm == CALL_CHANGING_PART:
            # при нажатии на изменение задаем следующий стейт элементов
            confirmation_state.next_state = AddWord.capture_parts_state
            # делаем так, чтобы в стейте добавления последний стейт (на изменения который) стал следующим
            capture_parts_state: StateParams = await state.get_value('capture_parts_state')
            capture_parts_state.next_state = AddWord.confirmation_state
            await state.update_data(capture_parts_state=capture_parts_state)

        elif confirm == CALL_CHANGING_LEVEL:
            # при нажатии на изменение задаем следующий стейт элементов
            confirmation_state.next_state = AddWord.capture_levels_state
            # делаем так, чтобы в стейте добавления последний стейт (на изменения который) стал следующим
            capture_levels_state: StateParams = await state.get_value('capture_levels_state')
            capture_levels_state.next_state = AddWord.confirmation_state
            await state.update_data(capture_levels_state=capture_levels_state)

        elif confirm == CALL_CHANGING_DEFINITION:
            # при нажатии на изменение задаем следующий стейт элементов
            confirmation_state.next_state = AddWord.input_definition_state
            # делаем так, чтобы в стейте добавления последний стейт (на изменения который) стал следующим
            input_definition_state: StateParams = await state.get_value('input_definition_state')
            input_definition_state.next_state = AddWord.confirmation_state
            await state.update_data(input_definition_state=input_definition_state)

        elif confirm == CALL_CHANGING_TRANSLATION:
            # при нажатии на изменение задаем следующий стейт элементов
            confirmation_state.next_state = AddWord.input_translation_state
            # делаем так, чтобы в стейте добавления последний стейт (на изменения который) стал следующим
            input_translation_state: StateParams = await state.get_value('input_translation_state')
            input_translation_state.next_state = AddWord.confirmation_state
            await state.update_data(input_translation_state=input_translation_state)

        await state.update_data(confirmation_state=confirmation_state)
        current_fsm = FSMExecutor()
        await current_fsm.execute(state, call)
        await call.message.edit_text(current_fsm.message_text, reply_markup=current_fsm.reply_kb)
        await call.answer()

    else:
        author_id_state = await state.get_value('author_id')
        author_id = author_id_state
        print(author_id)
        print('не обработано')
        state_text = await state_text_builder(state)

        author_id = await state.get_value('author_id')

        input_word: StateParams = await state.get_value('input_word_state')
        word_item = input_word.input_item

        capture_parts: StateParams = await state.get_value('capture_parts_state')
        parts_set = capture_parts.captured_items_set

        capture_levels: StateParams = await state.get_value('capture_levels_state')
        levels_set = capture_levels.captured_items_set

        input_definition: StateParams = await state.get_value('input_definition_state')
        definition_item = input_definition.input_item

        input_translation: StateParams = await state.get_value('input_translation_state')
        translation_item = input_translation.input_item

        state_text = await state_text_builder(state)




        res = True
        for part in parts_set:
            for level in levels_set:
                res = res and await rq.add_word_to_db(word=word_item,
                                                      level=level,
                                                      part=part,
                                                      translation=translation_item,
                                                      definition=definition_item,
                                                      author_id=author_id)

        message_text = f'----- ----- -----\n{state_text}----- ----- -----\n'

        if res:
            message_text += amsg.ADM_ADD_TASK_ADDED
        else:
            message_text += amsg.ADM_ADD_TASK_ERROR

        reply_kb = await akb.admin_adding_menu_kb()
        await call.message.edit_text(message_text, reply_markup=reply_kb)
        await call.answer()


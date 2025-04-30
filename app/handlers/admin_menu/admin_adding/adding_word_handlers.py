from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.keyboards.menu_buttons import *
from app.handlers.common_settings import *
from app.keyboards.keyboard_builder import keyboard_builder, update_button_with_call_base
from app.utils.admin_utils import message_answer, state_text_builder
from app.database.requests import get_users_by_filters, add_word_to_db, get_words_by_filters

from app.handlers.admin_menu.states.state_executor import FSMExecutor
from app.handlers.admin_menu.states.state_params import (InputStateParams, CaptureLevelsStateParams,
                                                         CapturePartsStateParams, CaptureSourcesStateParams,
                                                         ConfirmationStateParams)
adding_word_router = Router()

class AddWord(StatesGroup):
    author_id = State() # автор который назначает задание - ид
    input_word_state = State()
    capture_parts_state = State()
    capture_levels_state = State()
    capture_sources_state = State()
    input_definition_state = State()
    input_translation_state = State()
    confirmation_state = State()

menu_add_word = [
    [button_adding_menu_back, button_admin_menu, button_main_menu]
]

menu_add_word_with_changing = [
    [update_button_with_call_base(button_change_words, CALL_ADD_WORD),
     update_button_with_call_base(button_change_levels, CALL_ADD_WORD),
     update_button_with_call_base(button_change_parts, CALL_ADD_WORD)],
    [update_button_with_call_base(button_change_translation, CALL_ADD_WORD),
     update_button_with_call_base(button_change_definition, CALL_ADD_WORD),
     update_button_with_call_base(button_change_sources, CALL_ADD_WORD)],
    [button_adding_menu_back, button_admin_menu, button_main_menu]
]


# переход в меню добавления задания по схеме
@adding_word_router.callback_query(F.data == CALL_ADD_WORD)
async def adding_word_first_state(call: CallbackQuery, state: FSMContext):
    # очистка стейта
    await state.clear()

    # задаем в стейт ид автора
    author = await get_users_by_filters(user_tg_id=call.from_user.id)
    await state.update_data(author_id=author.id)
    # начальные параметры стейта
    word_state = InputStateParams(self_state = AddWord.input_word_state,
                                  next_state = AddWord.capture_parts_state,
                                  call_base= CALL_ADD_WORD,
                                  main_mess= MESS_INPUT_WORD,
                                  menu_pack= menu_add_word,
                                  is_input=True)
    await state.update_data(input_word_state=word_state)

    parts_state = CapturePartsStateParams(self_state=AddWord.capture_parts_state,
                                          next_state=AddWord.capture_levels_state,
                                          call_base=CALL_ADD_WORD,
                                          menu_pack=menu_add_word,
                                          is_only_one=True)
    await state.update_data(capture_parts_state=parts_state)

    levels_state = CaptureLevelsStateParams(self_state=AddWord.capture_levels_state,
                                            next_state=AddWord.capture_sources_state,
                                            call_base=CALL_ADD_WORD,
                                            menu_pack=menu_add_word,
                                            is_only_one=True)
    await state.update_data(capture_levels_state=levels_state)

    source_state = CaptureSourcesStateParams(self_state=AddWord.capture_sources_state,
                                             next_state=AddWord.input_definition_state,
                                             call_base=CALL_ADD_WORD,
                                             menu_pack=menu_add_word,
                                             is_only_one=True,
                                             is_can_be_empty=True)
    await source_state.update_state_kb()
    await state.update_data(capture_sources_state=source_state)

    definition_state = InputStateParams(self_state = AddWord.input_definition_state,
                                        next_state = AddWord.input_translation_state,
                                        call_base= CALL_ADD_WORD,
                                        main_mess= MESS_INPUT_DEFINITION,
                                        menu_pack= menu_add_word,
                                        is_input=True)
    await state.update_data(input_definition_state=definition_state)

    translation_state = InputStateParams(self_state = AddWord.input_translation_state,
                                         next_state = AddWord.confirmation_state,
                                         call_base= CALL_ADD_WORD,
                                         main_mess= MESS_INPUT_TRANSLATION,
                                         menu_pack= menu_add_word,
                                         is_input=True)
    await state.update_data(input_translation_state=translation_state)

    confirmation_state = ConfirmationStateParams(self_state = AddWord.confirmation_state,
                                                 call_base = CALL_ADD_WORD,
                                                 menu_pack= menu_add_word_with_changing,
                                                 is_last_state_with_changing_mode=True)
    await state.update_data(confirmation_state=confirmation_state)

    # переход в первый стейт
    first_state = word_state
    await state.set_state(first_state.self_state)
    # формируем сообщение, меню, клавиатуру и выводим их
    reply_kb = await keyboard_builder(menu_pack=first_state.menu_pack,
                                      buttons_pack=first_state.buttons_pack,
                                      buttons_base_call=first_state.call_base,
                                      buttons_cols=first_state.buttons_cols,
                                      buttons_rows=first_state.buttons_rows,
                                      is_adding_confirm_button=not first_state.is_input)

    state_text = await state_text_builder(state)
    message_text = state_text + '\n' + first_state.main_mess
    await call.message.edit_text(text=message_text, reply_markup=reply_kb)
    await call.answer()


@adding_word_router.message(F.text, AddWord.input_word_state)
@adding_word_router.message(F.text, AddWord.capture_parts_state)
@adding_word_router.message(F.text, AddWord.capture_levels_state)
@adding_word_router.message(F.text, AddWord.capture_sources_state)
@adding_word_router.message(F.text, AddWord.input_definition_state)
@adding_word_router.message(F.text, AddWord.input_translation_state)
async def admin_adding_word_capture_word(message: Message, state: FSMContext):

    fsm_state_str = await state.get_state()
    # проверяем слово в базе данных
    if fsm_state_str == AddWord.input_word_state.state:
        input_word_state: InputStateParams = await state.get_value('input_word_state')
        input_word = message.text.lower()
        words = await get_words_by_filters(word=input_word)
        if words:
            input_word_state.next_state = AddWord.input_word_state
            input_word_state.main_mess = MESS_INPUT_WORD_ALREADY_EXIST
        else:
            input_word_state.next_state = AddWord.capture_parts_state
            input_word_state.main_mess = MESS_INPUT_WORD
        await state.update_data(input_word_state=input_word_state)



    # создаем экземпляр класса для обработки текущего состояния фсм
    current_fsm = FSMExecutor()
    # обрабатываем экземпляра класса, который анализирует наш колл и выдает сообщение и клавиатуру
    await current_fsm.execute(fsm_state=state, fsm_mess=message)

    state_text = await state_text_builder(state)
    message_text = state_text + '\n' + current_fsm.message_text
    await message_answer(source=message, message_text=message_text, reply_markup=current_fsm.reply_kb)


@adding_word_router.callback_query(F.data.startswith(CALL_ADD_WORD), AddWord.capture_sources_state)
@adding_word_router.callback_query(F.data.startswith(CALL_ADD_WORD), AddWord.capture_parts_state)
@adding_word_router.callback_query(F.data.startswith(CALL_ADD_WORD), AddWord.capture_levels_state)
async def set_scheme_capture_words_from_call(call: CallbackQuery, state: FSMContext):
    # создаем экземпляр класса для обработки текущего состояния фсм
    current_fsm = FSMExecutor()
    # обрабатываем экземпляра класса, который анализирует наш колл и выдает сообщение и клавиатуру
    await current_fsm.execute(fsm_state=state, fsm_call=call)
    # отвечаем заменой сообщения

    state_text = await state_text_builder(state)
    message_text = state_text + '\n' + current_fsm.message_text
    await call.message.edit_text(message_text, reply_markup=current_fsm.reply_kb)
    await call.answer()


# конечный обработчик всего стейта
@adding_word_router.callback_query(F.data.startswith(CALL_ADD_WORD), AddWord.confirmation_state)
async def admin_adding_task_capture_confirmation_from_call(call: CallbackQuery, state: FSMContext):
    # вытаскиваем из колбека уровень
    confirm = call.data.replace(CALL_ADD_WORD, '')

    # уходим обратно если нужно что-то изменить
    if (confirm == CALL_CHANGING_WORDS or confirm == CALL_CHANGING_PARTS or confirm == CALL_CHANGING_LEVELS
            or confirm == CALL_CHANGING_DEFINITION or confirm == CALL_CHANGING_TRANSLATION
            or confirm == CALL_CHANGING_SOURCES):

        confirmation_state: InputStateParams = await state.get_value('confirmation_state')

        if confirm == CALL_CHANGING_WORDS:
            # при нажатии на изменение задаем следующий стейт элементов
            confirmation_state.next_state = AddWord.input_word_state
            # делаем так, чтобы в стейте добавления последний стейт (на изменения который) стал следующим
            input_word_state: InputStateParams = await state.get_value('input_word_state')
            input_word_state.next_state = AddWord.confirmation_state
            await state.update_data(input_word_state=input_word_state)

        elif confirm == CALL_CHANGING_PARTS:
            # при нажатии на изменение задаем следующий стейт элементов
            confirmation_state.next_state = AddWord.capture_parts_state
            # делаем так, чтобы в стейте добавления последний стейт (на изменения который) стал следующим
            capture_parts_state: InputStateParams = await state.get_value('capture_parts_state')
            capture_parts_state.next_state = AddWord.confirmation_state
            await state.update_data(capture_parts_state=capture_parts_state)

        elif confirm == CALL_CHANGING_LEVELS:
            # при нажатии на изменение задаем следующий стейт элементов
            confirmation_state.next_state = AddWord.capture_levels_state
            # делаем так, чтобы в стейте добавления последний стейт (на изменения который) стал следующим
            capture_levels_state: InputStateParams = await state.get_value('capture_levels_state')
            capture_levels_state.next_state = AddWord.confirmation_state
            await state.update_data(capture_levels_state=capture_levels_state)

        elif confirm == CALL_CHANGING_SOURCES:
            # при нажатии на изменение задаем следующий стейт элементов
            confirmation_state.next_state = AddWord.capture_sources_state
            # делаем так, чтобы в стейте добавления последний стейт (на изменения который) стал следующим
            capture_sources_state: InputStateParams = await state.get_value('capture_sources_state')
            capture_sources_state.next_state = AddWord.confirmation_state
            await state.update_data(capture_sources_state=capture_sources_state)

        elif confirm == CALL_CHANGING_DEFINITION:
            # при нажатии на изменение задаем следующий стейт элементов
            confirmation_state.next_state = AddWord.input_definition_state
            # делаем так, чтобы в стейте добавления последний стейт (на изменения который) стал следующим
            input_definition_state: InputStateParams = await state.get_value('input_definition_state')
            input_definition_state.next_state = AddWord.confirmation_state
            await state.update_data(input_definition_state=input_definition_state)

        elif confirm == CALL_CHANGING_TRANSLATION:
            # при нажатии на изменение задаем следующий стейт элементов
            confirmation_state.next_state = AddWord.input_translation_state
            # делаем так, чтобы в стейте добавления последний стейт (на изменения который) стал следующим
            input_translation_state: InputStateParams = await state.get_value('input_translation_state')
            input_translation_state.next_state = AddWord.confirmation_state
            await state.update_data(input_translation_state=input_translation_state)

        await state.update_data(confirmation_state=confirmation_state)
        current_fsm = FSMExecutor()
        await current_fsm.execute(state, call)
        state_text = await state_text_builder(state)
        message_text = state_text + '\n' + current_fsm.message_text
        await call.message.edit_text(message_text, reply_markup=current_fsm.reply_kb)
        await call.answer()

    # обрабатываем ввод, если все ок и нажато подтверждение
    elif confirm == CALL_CONFIRM:

        # основной обработчик, запись в бд
        author_id = await state.get_value('author_id')

        input_word: InputStateParams = await state.get_value('input_word_state')
        word_item = input_word.input_text

        capture_parts: InputStateParams = await state.get_value('capture_parts_state')
        parts_set = capture_parts.set_of_items

        capture_levels: InputStateParams = await state.get_value('capture_levels_state')
        levels_set = capture_levels.set_of_items

        capture_sources: InputStateParams = await state.get_value('capture_sources_state')
        sources_set = capture_sources.set_of_items
        source_item = None
        if sources_set:
            for source in sources_set:
                source_item = source

        input_definition: InputStateParams = await state.get_value('input_definition_state')
        definition_item = input_definition.input_text

        input_translation: InputStateParams = await state.get_value('input_translation_state')
        translation_item = input_translation.input_text

        state_text = await state_text_builder(state)

        res = True
        for part in parts_set:
            for level in levels_set:
                res = res and await add_word_to_db(word=word_item,
                                                      level=level,
                                                      part=part,
                                                      translation=translation_item,
                                                      definition=definition_item,
                                                      source_id=source_item,
                                                      author_id=author_id)

        message_text = f'----- ----- -----\n{state_text}----- ----- -----\n'

        if res:
            message_text += MESS_ADDED_TO_DB
        else:
            message_text += MESS_ERROR_ADDED_TO_DB

        reply_kb = await keyboard_builder(menu_pack=menu_add_word, buttons_base_call="")

        await call.message.edit_text(message_text, reply_markup=reply_kb)
        await call.answer()


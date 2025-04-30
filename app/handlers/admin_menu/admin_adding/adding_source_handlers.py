from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.keyboards.menu_buttons import *
from app.handlers.common_settings import *
from app.keyboards.keyboard_builder import keyboard_builder, update_button_with_call_base
from app.utils.admin_utils import message_answer, state_text_builder
from app.database.requests import get_users_by_filters, add_word_to_db, add_source_to_db, get_sources_by_filters

from app.handlers.admin_menu.states.state_executor import FSMExecutor
from app.handlers.admin_menu.states.state_params import (InputStateParams, ConfirmationStateParams)
adding_source_router = Router()

class AddSource(StatesGroup):
    author_id = State() # автор который назначает задание - ид
    input_source_name_state = State()
    confirmation_state = State()

menu_add_source = [
    [button_adding_menu_back, button_admin_menu, button_main_menu]
]

menu_add_source_with_changing = [
    [update_button_with_call_base(button_change_source_name, CALL_ADD_SOURCE)],
    [button_adding_menu_back, button_admin_menu, button_main_menu]
]


# переход в меню добавления задания по схеме
@adding_source_router.callback_query(F.data == CALL_ADD_SOURCE)
async def adding_word_first_state(call: CallbackQuery, state: FSMContext):
    # очистка стейта
    await state.clear()

    # задаем в стейт ид автора
    author = await get_users_by_filters(user_tg_id=call.from_user.id)
    await state.update_data(author_id=author.id)
    # начальные параметры стейта
    source_state = InputStateParams(self_state = AddSource.input_source_name_state,
                                    next_state = AddSource.confirmation_state,
                                    call_base= CALL_ADD_SOURCE,
                                    main_mess= MESS_INPUT_SOURCE_NAME,
                                    menu_pack= menu_add_source,
                                    is_input=True)
    await state.update_data(input_source_name_state=source_state)

    confirmation_state = ConfirmationStateParams(self_state = AddSource.confirmation_state,
                                          call_base = CALL_ADD_SOURCE,
                                          menu_pack= menu_add_source_with_changing,
                                          is_last_state_with_changing_mode=True)
    await state.update_data(confirmation_state=confirmation_state)

    # переход в первый стейт
    first_state = source_state
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


@adding_source_router.message(F.text, AddSource.input_source_name_state)
async def admin_adding_source(message: Message, state: FSMContext):
    # проверяем слово в базе данных
    fsm_state_str = await state.get_state()
    # проверяем наличие в базе данных
    if fsm_state_str == AddSource.input_source_name_state.state:
        input_source_state: InputStateParams = await state.get_value('input_source_name_state')
        input_source = message.text.lower()
        sources = await get_sources_by_filters(source_name=input_source)
        if sources:
            input_source_state.next_state = AddSource.input_source_name_state
            input_source_state.main_mess = MESS_INPUT_SOURCE_NAME_ALREADY_EXIST
        else:
            input_source_state.next_state = AddSource.confirmation_state
            input_source_state.main_mess = MESS_INPUT_SOURCE_NAME
        await state.update_data(input_source_name_state=input_source_state)
    # создаем экземпляр класса для обработки текущего состояния фсм


    current_fsm = FSMExecutor()
    # обрабатываем экземпляра класса, который анализирует наш колл и выдает сообщение и клавиатуру
    await current_fsm.execute(fsm_state=state, fsm_mess=message)

    state_text = await state_text_builder(state)
    message_text = state_text + '\n' + current_fsm.message_text
    await message_answer(source=message, message_text=message_text, reply_markup=current_fsm.reply_kb)




# конечный обработчик всего стейта
@adding_source_router.callback_query(F.data.startswith(CALL_ADD_SOURCE), AddSource.confirmation_state)
async def admin_adding_task_capture_confirmation_from_call(call: CallbackQuery, state: FSMContext):
    # вытаскиваем из колбека уровень
    confirm = call.data.replace(CALL_ADD_SOURCE, '')

    # уходим обратно если нужно что-то изменить
    if confirm == CALL_CHANGING_SOURCE_NAME:

        confirmation_state: InputStateParams = await state.get_value('confirmation_state')

        if confirm == CALL_CHANGING_SOURCE_NAME:
            # при нажатии на изменение задаем следующий стейт элементов
            confirmation_state.next_state = AddSource.input_source_name_state
            # делаем так, чтобы в стейте добавления последний стейт (на изменения который) стал следующим
            input_source_name_state: InputStateParams = await state.get_value('input_source_name_state')
            input_source_name_state.next_state = AddSource.confirmation_state
            await state.update_data(input_source_name_state=input_source_name_state)

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

        input_source: InputStateParams = await state.get_value('input_source_name_state')
        source_item = input_source.input_text

        state_text = await state_text_builder(state)

        res = True
        res = res and await add_source_to_db(source_name=source_item,
                                             author_id=author_id)

        message_text = f'----- ----- -----\n{state_text}----- ----- -----\n'

        if res:
            message_text += MESS_ADDED_TO_DB
        else:
            message_text += MESS_ERROR_ADDED_TO_DB

        reply_kb = await keyboard_builder(menu_pack=menu_add_source, buttons_base_call="")

        await call.message.edit_text(message_text, reply_markup=reply_kb)
        await call.answer()


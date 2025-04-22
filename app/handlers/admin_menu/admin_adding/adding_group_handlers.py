from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.keyboards.menu_buttons import *
from app.handlers.common_settings import *

from app.keyboards.keyboard_builder import keyboard_builder, update_button_with_call_base
from app.utils.admin_utils import message_answer, state_text_builder, get_user_list_for_kb_with_ids
from app.database.requests import set_group
from app.handlers.admin_menu.states.input_states import (StateParams, FSMExecutor,
                                                         CaptureLevelsStateParams,
                                                         CaptureUsersStateParams)

adding_group_router = Router()

class AddGroup(StatesGroup):
    input_group_state = State()
    capture_users_state = State()
    capture_levels_state = State()
    confirmation_state = State()

menu_add_group = [
    [button_adding_menu_back, button_admin_menu, button_main_menu]
]

menu_add_group_with_changing = [
    [update_button_with_call_base(button_change_group, CALL_ADD_GROUP + CALL_ADD_ENDING),
     update_button_with_call_base(button_change_users, CALL_ADD_GROUP + CALL_ADD_ENDING),
     update_button_with_call_base(button_change_levels, CALL_ADD_GROUP + CALL_ADD_ENDING)],
    [button_adding_menu_back, button_admin_menu, button_main_menu]
]


# переход в меню добавления задания по схеме
@adding_group_router.callback_query(F.data == CALL_ADD_GROUP)
async def adding_first_state(call: CallbackQuery, state: FSMContext):
    # очистка стейта
    await state.clear()

    # начальные параметры стейта
    group_state = StateParams(self_state = AddGroup.input_group_state,
                              next_state = AddGroup.capture_users_state,
                              call_base= CALL_ADD_GROUP,
                              call_add_capture= CALL_INPUT_GROUP,
                              state_main_mess = MESS_INPUT_GROUP,
                              but_change_text = BTEXT_CHANGE_GROUP,
                              menu_add = menu_add_group,
                              is_input=True)
    await state.update_data(input_group_state=group_state)

    users_state = CaptureUsersStateParams(self_state=AddGroup.capture_users_state,
                                          next_state=AddGroup.capture_levels_state,
                                          call_base=CALL_ADD_GROUP,
                                          menu_add=menu_add_group,
                                          items_kb_list=await get_user_list_for_kb_with_ids())

    await state.update_data(capture_users_state=users_state)

    levels_state = CaptureLevelsStateParams(self_state=AddGroup.capture_levels_state,
                                            next_state=AddGroup.confirmation_state,
                                            call_base=CALL_ADD_GROUP,
                                            menu_add=menu_add_group,
                                            items_kb_list=LEVELS_LIST,
                                            is_only_one=True)
    await state.update_data(capture_levels_state=levels_state)

    confirmation_state = StateParams(self_state = AddGroup.confirmation_state,
                                     call_base = CALL_ADD_GROUP,
                                     call_add_capture= CALL_ADD_ENDING,
                                     menu_add = menu_add_group_with_changing,
                                     state_main_mess=MESS_ADD_ENDING,
                                     is_last_state_with_changing_mode=True)
    await state.update_data(confirmation_state=confirmation_state)

    # переход в первый стейт
    first_state = group_state
    await state.set_state(first_state.self_state)
    # формируем сообщение, меню, клавиатуру и выводим их
    reply_kb = await keyboard_builder(menu_pack=first_state.menu_add,
                                      buttons_add_list= first_state.items_kb_list,
                                      buttons_base_call=first_state.call_base + first_state.call_add_capture,
                                      buttons_add_cols=first_state.items_kb_cols,
                                      buttons_add_rows=first_state.items_kb_rows,
                                      is_adding_confirm_button=not first_state.is_input)

    state_text = await state_text_builder(state)
    message_text = state_text + '\n' + first_state.state_main_mess
    await call.message.edit_text(text=message_text, reply_markup=reply_kb)
    await call.answer()


@adding_group_router.message(F.text, AddGroup.input_group_state)
@adding_group_router.message(F.text, AddGroup.capture_users_state)
@adding_group_router.message(F.text, AddGroup.capture_levels_state)
async def admin_adding_group_capture(message: Message, state: FSMContext):
    # проверяем слово в базе данных
    # создаем экземпляр класса для обработки текущего состояния фсм
    current_fsm = FSMExecutor()
    # обрабатываем экземпляра класса, который анализирует наш колл и выдает сообщение и клавиатуру
    await current_fsm.execute(fsm_state=state, fsm_mess=message)

    state_text = await state_text_builder(state)
    message_text = state_text + '\n' + current_fsm.message_text
    await message_answer(source=message, message_text=message_text, reply_markup=current_fsm.reply_kb)

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


@adding_group_router.callback_query(F.data.startswith(CALL_ADD_GROUP + CALL_CAPTURE_USERS), AddGroup.capture_users_state)
@adding_group_router.callback_query(F.data.startswith(CALL_ADD_GROUP + CALL_CAPTURE_LEVELS), AddGroup.capture_levels_state)
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
@adding_group_router.callback_query(F.data.startswith(CALL_ADD_GROUP + CALL_ADD_ENDING), AddGroup.confirmation_state)
async def admin_adding_task_capture_confirmation_from_call(call: CallbackQuery, state: FSMContext):
    # вытаскиваем из колбека уровень
    confirm = call.data.replace(CALL_ADD_GROUP + CALL_ADD_ENDING, '')

    # уходим обратно если нужно что-то изменить
    if (confirm == CALL_CHANGING_USERS or confirm == CALL_CHANGING_LEVELS or confirm == CALL_CHANGING_GROUPS):

        confirmation_state: StateParams = await state.get_value('confirmation_state')

        if confirm == CALL_CHANGING_GROUPS:
            # при нажатии на изменение задаем следующий стейт элементов
            confirmation_state.next_state = AddGroup.input_group_state
            # делаем так, чтобы в стейте добавления последний стейт (на изменения который) стал следующим
            input_group_state: StateParams = await state.get_value('input_group_state')
            input_group_state.next_state = AddGroup.confirmation_state
            await state.update_data(input_group_state=input_group_state)

        elif confirm == CALL_CHANGING_USERS:
            # при нажатии на изменение задаем следующий стейт элементов
            confirmation_state.next_state = AddGroup.capture_users_state
            # делаем так, чтобы в стейте добавления последний стейт (на изменения который) стал следующим
            capture_users_state: StateParams = await state.get_value('capture_users_state')
            capture_users_state.next_state = AddGroup.confirmation_state
            await state.update_data(capture_users_state=capture_users_state)

        elif confirm == CALL_CHANGING_LEVELS:
            # при нажатии на изменение задаем следующий стейт элементов
            confirmation_state.next_state = AddGroup.capture_levels_state
            # делаем так, чтобы в стейте добавления последний стейт (на изменения который) стал следующим
            capture_levels_state: StateParams = await state.get_value('capture_levels_state')
            capture_levels_state.next_state = AddGroup.confirmation_state
            await state.update_data(capture_levels_state=capture_levels_state)

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
        input_group: StateParams = await state.get_value('input_group_state')
        group_item = input_group.input_text

        capture_users: StateParams = await state.get_value('capture_users_state')
        users_set = capture_users.captured_items_set

        capture_levels: StateParams = await state.get_value('capture_levels_state')
        levels_set = capture_levels.captured_items_set

        state_text = await state_text_builder(state)

        res = True

        users_for_db = ','.join(map(str, list(users_set)))

        for level in levels_set:
            res = res and await set_group(name=group_item, users=users_for_db, level=level)

        message_text = f'----- ----- -----\n{state_text}----- ----- -----\n'

        if res:
            message_text += MESS_ADDED_TO_DB
        else:
            message_text += MESS_ERROR_ADDED_TO_DB

        reply_kb = await keyboard_builder(menu_pack=menu_add_group, buttons_base_call="")

        await call.message.edit_text(message_text, reply_markup=reply_kb)
        await call.answer()


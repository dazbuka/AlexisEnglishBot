from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from datetime import datetime

from app.keyboards.menu_buttons import *
from app.handlers.common_settings import *

from app.keyboards.keyboard_builder import keyboard_builder, update_button_with_call_base
from app.utils.admin_utils import (message_answer, state_text_builder, get_user_list_for_kb_with_ids,
                                   get_group_list_for_kb_with_ids, get_date_list_for_kb, add_item_in_aim_set_plus_plus)
from app.database.requests import get_users_by_filters, get_groups_by_filters, set_link
from app.handlers.admin_menu.states.input_states import (StateParams, FSMExecutor,
                                                         CaptureUsersStateParams,
                                                         CaptureGroupsStateParams,
                                                         CapturePriorityStateParams)

adding_link_router = Router()

class AddLink(StatesGroup):
    input_link_name_state = State()
    input_link_url_state = State()
    capture_groups_state = State()
    capture_users_state = State()
    capture_priority_state = State()
    confirmation_state = State()

menu_add_link = [
    [button_adding_menu_back, button_admin_menu, button_main_menu]
]

menu_add_link_with_changing = [
    [update_button_with_call_base(button_change_link_name, CALL_ADD_LINK + CALL_ADD_ENDING),
     update_button_with_call_base(button_change_link_url, CALL_ADD_LINK + CALL_ADD_ENDING)],
    [update_button_with_call_base(button_change_users, CALL_ADD_LINK + CALL_ADD_ENDING),
     update_button_with_call_base(button_change_priority, CALL_ADD_LINK + CALL_ADD_ENDING)],
    [button_adding_menu_back, button_admin_menu, button_main_menu]
]

# переход в меню добавления задания по схеме
@adding_link_router.callback_query(F.data == CALL_ADD_LINK)
async def adding_first_state(call: CallbackQuery, state: FSMContext):
    # очистка стейта
    await state.clear()

    # задаем в стейт ид автора
    author = await get_users_by_filters(user_tg_id=call.from_user.id)
    await state.update_data(author_id=author.id)

    # начальные параметры стейта
    link_name_state = StateParams(self_state = AddLink.input_link_name_state,
                                 next_state = AddLink.input_link_url_state,
                                 call_base= CALL_ADD_LINK,
                                 call_add_capture= CALL_INPUT_LINK_NAME,
                                 state_main_mess = MESS_INPUT_LINK_NAME,
                                 but_change_text = BTEXT_CHANGE_LINK_NAME,
                                 menu_add = menu_add_link,
                                 is_input=True)
    await state.update_data(input_link_name_state=link_name_state)

    link_url_state = StateParams(self_state=AddLink.input_link_url_state,
                                  next_state=AddLink.capture_groups_state,
                                  call_base=CALL_ADD_LINK,
                                  call_add_capture=CALL_INPUT_LINK_URL,
                                  state_main_mess=MESS_INPUT_LINK_URL,
                                  but_change_text=BTEXT_CHANGE_LINK_URL,
                                  menu_add=menu_add_link,
                                  is_input=True)
    await state.update_data(input_link_url_state=link_url_state)

    groups_state = CaptureGroupsStateParams(self_state=AddLink.capture_groups_state,
                                            next_state=AddLink.capture_users_state,
                                            call_base=CALL_ADD_LINK,
                                            menu_add=menu_add_link,
                                            items_kb_list=await get_group_list_for_kb_with_ids(),
                                            is_can_be_empty=True)
    await state.update_data(capture_groups_state=groups_state)

    users_state = CaptureUsersStateParams(self_state=AddLink.capture_users_state,
                                          next_state=AddLink.capture_priority_state,
                                          call_base=CALL_ADD_LINK,
                                          menu_add=menu_add_link,
                                          items_kb_list=await get_user_list_for_kb_with_ids())
    await state.update_data(capture_users_state=users_state)

    priority_state = CapturePriorityStateParams(self_state=AddLink.capture_priority_state,
                                                next_state=AddLink.confirmation_state,
                                                call_base=CALL_ADD_LINK,
                                                menu_add=menu_add_link,
                                                items_kb_list=['1','2','3','4','5'],
                                                is_only_one=True)
    await state.update_data(capture_priority_state=priority_state)

    confirmation_state = StateParams(self_state = AddLink.confirmation_state,
                                     call_base = CALL_ADD_LINK,
                                     call_add_capture= CALL_ADD_ENDING,
                                     menu_add = menu_add_link_with_changing,
                                     state_main_mess=MESS_ADD_ENDING,
                                     is_last_state_with_changing_mode=True)
    await state.update_data(confirmation_state=confirmation_state)

    # переход в первый стейт
    first_state = link_name_state
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


@adding_link_router.message(F.text, AddLink.input_link_name_state)
@adding_link_router.message(F.text, AddLink.input_link_url_state)
@adding_link_router.message(F.text, AddLink.capture_groups_state)
@adding_link_router.message(F.text, AddLink.capture_users_state)
@adding_link_router.message(F.text, AddLink.capture_priority_state)
async def admin_adding_link_capture(message: Message, state: FSMContext):
    # проверяем слово в базе данных
    # создаем экземпляр класса для обработки текущего состояния фсм
    current_fsm = FSMExecutor()
    # обрабатываем экземпляра класса, который анализирует наш колл и выдает сообщение и клавиатуру
    await current_fsm.execute(fsm_state=state, fsm_mess=message)

    state_text = await state_text_builder(state)
    message_text = state_text + '\n' + current_fsm.message_text
    await message_answer(source=message, message_text=message_text, reply_markup=current_fsm.reply_kb,
                         disable_web_page_preview=True)


@adding_link_router.callback_query(F.data.startswith(CALL_ADD_LINK + CALL_CAPTURE_GROUPS), AddLink.capture_groups_state)
@adding_link_router.callback_query(F.data.startswith(CALL_ADD_LINK + CALL_CAPTURE_USERS), AddLink.capture_users_state)
@adding_link_router.callback_query(F.data.startswith(CALL_ADD_LINK + CALL_CAPTURE_PRIRITY), AddLink.capture_priority_state)
async def set_scheme_capture_words_from_call(call: CallbackQuery, state: FSMContext):
    # создаем экземпляр класса для обработки текущего состояния фсм
    current_fsm = FSMExecutor()
    # обрабатываем экземпляра класса, который анализирует наш колл и выдает сообщение и клавиатуру
    await current_fsm.execute(fsm_state=state, fsm_call=call)
    # отвечаем заменой сообщения

    # специальный местный обработчик, который при работе с группами, добавляет сразу пользователей в стейт
    if CALL_CAPTURE_GROUPS in call.data:
        groups_state: StateParams = await state.get_value('capture_groups_state')
        added_id = groups_state.captured_items_set
        users_state: StateParams = await state.get_value('capture_users_state')
        new_user_set = set()
        for group_id in added_id:
            added_items = (await get_groups_by_filters(group_id=group_id)).users

            new_user_set = await add_item_in_aim_set_plus_plus(aim_set=new_user_set, added_item=added_items)
        users_state.captured_items_set = new_user_set
        await state.update_data(capture_users_state=users_state)

    state_text = await state_text_builder(state)
    message_text = state_text + '\n' + current_fsm.message_text
    await call.message.edit_text(message_text, reply_markup=current_fsm.reply_kb, disable_web_page_preview=True)
    await call.answer()


# конечный обработчик всего стейта
@adding_link_router.callback_query(F.data.startswith(CALL_ADD_LINK + CALL_ADD_ENDING), AddLink.confirmation_state)
async def admin_adding_task_capture_confirmation_from_call(call: CallbackQuery, state: FSMContext):
    # вытаскиваем из колбека уровень
    confirm = call.data.replace(CALL_ADD_LINK + CALL_ADD_ENDING, '')

    # уходим обратно если нужно что-то изменить
    if (confirm == CALL_CHANGING_LINK_NAME or confirm == CALL_CHANGING_LINK_URL or confirm == CALL_CHANGING_USERS
            or confirm == CALL_CHANGING_PRIRITY):

        confirmation_state: StateParams = await state.get_value('confirmation_state')

        if confirm == CALL_CHANGING_LINK_NAME:
            # при нажатии на изменение задаем следующий стейт элементов
            confirmation_state.next_state = AddLink.input_link_name_state
            # делаем так, чтобы в стейте добавления последний стейт (на изменения который) стал следующим
            input_link_name_state: StateParams = await state.get_value('input_link_name_state')
            input_link_name_state.next_state = AddLink.confirmation_state
            await state.update_data(input_link_name_state=input_link_name_state)

        elif confirm == CALL_CHANGING_LINK_URL:
            # при нажатии на изменение задаем следующий стейт элементов
            confirmation_state.next_state = AddLink.input_link_url_state
            # делаем так, чтобы в стейте добавления последний стейт (на изменения который) стал следующим
            input_link_url_state: StateParams = await state.get_value('input_link_url_state')
            input_link_url_state.next_state = AddLink.confirmation_state
            await state.update_data(input_link_url_state=input_link_url_state)

        elif confirm == CALL_CHANGING_USERS:
            # при нажатии на изменение задаем следующий стейт элементов
            confirmation_state.next_state = AddLink.capture_users_state
            # делаем так, чтобы в стейте добавления последний стейт (на изменения который) стал следующим
            capture_users_state: StateParams = await state.get_value('capture_users_state')
            capture_users_state.next_state = AddLink.confirmation_state
            await state.update_data(capture_users_state=capture_users_state)

        elif confirm == CALL_CHANGING_PRIRITY:
            # при нажатии на изменение задаем следующий стейт элементов
            confirmation_state.next_state = AddLink.capture_priority_state
            # делаем так, чтобы в стейте добавления последний стейт (на изменения который) стал следующим
            capture_priority_state: StateParams = await state.get_value('capture_priority_state')
            capture_priority_state.next_state = AddLink.confirmation_state
            await state.update_data(capture_priority_state=capture_priority_state)

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
        input_name_state: StateParams = await state.get_value('input_link_name_state')
        name_item = input_name_state.input_text
        print(name_item)

        input_url_state: StateParams = await state.get_value('input_link_url_state')
        url_item = input_url_state.input_text
        print(url_item)

        capture_users: StateParams = await state.get_value('capture_users_state')
        users_set = capture_users.captured_items_set
        print(users_set)

        priority_state: StateParams = await state.get_value('capture_priority_state')
        priority_set = priority_state.captured_items_set
        print(priority_set)

        state_text = await state_text_builder(state)

        users_for_db = ','.join(map(str, list(users_set)))

        res = True

        for priority in priority_set:
            res = res and await set_link(link_name=name_item, link_url=url_item, users=users_for_db, priority=priority)

        message_text = f'----- ----- -----\n{state_text}----- ----- -----\n'

        if res:
            message_text += MESS_ADDED_TO_DB
        else:
            message_text += MESS_ERROR_ADDED_TO_DB

        reply_kb = await keyboard_builder(menu_pack=menu_add_link, buttons_base_call="")

        await call.message.edit_text(message_text, reply_markup=reply_kb)
        await call.answer()


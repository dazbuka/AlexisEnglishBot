from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta

from app.keyboards.menu_buttons import *
from app.handlers.common_settings import *

from app.database.requests import get_users_by_filters, get_groups_by_filters
from app.utils.admin_utils import (message_answer,
                                   add_item_in_aim_set_plus_plus,
                                   get_colls_list_for_kb_with_ids,
                                   get_group_list_for_kb_with_ids,
                                   get_user_list_for_kb_with_ids,
                                   get_date_list_for_kb)
from app.utils.admin_utils import state_text_builder
from app.database.requests import set_task
from app.handlers.admin_menu.states.state_executor import FSMExecutor
from app.handlers.admin_menu.states.state_params import (InputStateParams, CaptureCollsStateParams,
                                                         CaptureGroupsStateParams, CaptureUsersStateParams,
                                                         CaptureDatesStateParams)

from app.keyboards.keyboard_builder import keyboard_builder, update_button_with_call_base

setting_colls_router = Router()

class SetColls(StatesGroup):
    author_id = State() # автор который назначает задание - ид
    capture_colls_state = State()
    capture_groups_state = State()
    capture_users_state = State()
    capture_dates_state = State()
    confirmation_state = State() # стейт обрабатывающий конечное подтверждение ввода

menu_set_colls = [
    [button_setting_menu_back, button_admin_menu, button_main_menu]
]

menu_set_colls_with_changing = [
    [update_button_with_call_base(button_change_colls, CALL_SET_COLL + CALL_ADD_ENDING),
     update_button_with_call_base(button_change_users, CALL_SET_COLL + CALL_ADD_ENDING),
     update_button_with_call_base(button_change_dates, CALL_SET_COLL + CALL_ADD_ENDING)],
    [button_setting_menu_back, button_admin_menu, button_main_menu]
]

# переход в меню добавления задания по схеме
@setting_colls_router.callback_query(F.data == CALL_SET_COLL)
async def setting_colls_first_state(call: CallbackQuery, state: FSMContext):
    # очистка стейта
    await state.clear()

    # задаем в стейт ид автора
    author = await get_users_by_filters(user_tg_id=call.from_user.id)
    await state.update_data(author_id=author.id)

    colls_state = CaptureCollsStateParams(self_state = SetColls.capture_colls_state,
                                          next_state = SetColls.capture_groups_state,
                                          call_base= CALL_SET_COLL,
                                          menu_add = menu_set_colls,
                                          items_kb_list=(await get_colls_list_for_kb_with_ids())[::-1])
    await state.update_data(capture_colls_state=colls_state)

    groups_state = CaptureGroupsStateParams(self_state=SetColls.capture_groups_state,
                                            next_state=SetColls.capture_users_state,
                                            call_base=CALL_SET_COLL,
                                            menu_add=menu_set_colls,
                                            items_kb_list=await get_group_list_for_kb_with_ids(),
                                            is_can_be_empty=True)
    await state.update_data(capture_groups_state=groups_state)

    users_state = CaptureUsersStateParams(self_state=SetColls.capture_users_state,
                                          next_state=SetColls.capture_dates_state,
                                          call_base=CALL_SET_COLL,
                                          menu_add=menu_set_colls,
                                          items_kb_list=await get_user_list_for_kb_with_ids())
    await state.update_data(capture_users_state=users_state)

    dates_state = CaptureDatesStateParams(self_state=SetColls.capture_dates_state,
                                          next_state=SetColls.confirmation_state,
                                          call_base=CALL_SET_COLL,
                                          menu_add=menu_set_colls,
                                          items_kb_list=await get_date_list_for_kb(),
                                          is_only_one = True)
    await state.update_data(capture_dates_state=dates_state)

    confirmation_state = InputStateParams(self_state = SetColls.confirmation_state,
                                          call_base = CALL_SET_COLL,
                                          call_add_capture= CALL_ADD_ENDING,
                                          menu_pack= menu_set_colls_with_changing,
                                          main_mess=MESS_ADD_ENDING,
                                          is_last_state_with_changing_mode=True)
    await state.update_data(confirmation_state=confirmation_state)

    first_state = colls_state

    # переход в первый стейт
    await state.set_state(first_state.self_state)
    # формируем сообщение, меню, клавиатуру и выводим их
    reply_kb = await keyboard_builder(menu_pack=first_state.menu_pack,
                                      buttons_add_list= first_state.items_kb_list,
                                      buttons_base_call=first_state.call_base + first_state.call_add_capture,
                                      buttons_cols=first_state.items_kb_cols,
                                      buttons_rows=first_state.items_kb_rows,
                                      is_adding_confirm_button=True)

    state_text = await state_text_builder(state)
    message_text = state_text + '\n' + first_state.state_main_mess
    await call.message.edit_text(text=message_text, reply_markup=reply_kb)

    # await call.message.edit_text(message_text, reply_markup=reply_kb)
    await call.answer()



# цикличные хендлеры захвата слов, пользователей и др.
@setting_colls_router.callback_query(F.data.startswith(CALL_SET_COLL + CALL_CAPTURE_COLLS), SetColls.capture_colls_state)
@setting_colls_router.callback_query(F.data.startswith(CALL_SET_COLL + CALL_CAPTURE_GROUPS), SetColls.capture_groups_state)
@setting_colls_router.callback_query(F.data.startswith(CALL_SET_COLL + CALL_CAPTURE_USERS), SetColls.capture_users_state)
@setting_colls_router.callback_query(F.data.startswith(CALL_SET_COLL + CALL_CAPTURE_DATES), SetColls.capture_dates_state)
async def set_colls_capture_colls_from_call(call: CallbackQuery, state: FSMContext):
    # создаем экземпляр класса для обработки текущего состояния фсм
    current_fsm = FSMExecutor()
    # обрабатываем экземпляра класса, который анализирует наш колл и выдает сообщение и клавиатуру
    await current_fsm.execute(fsm_state=state, fsm_call=call)

    # специальный местный обработчик, который при работе с группами, добавляет сразу пользователей в стейт
    if CALL_CAPTURE_GROUPS in call.data:
        groups_state : InputStateParams  = await state.get_value('capture_groups_state')
        added_id = groups_state.set_of_items
        users_state : InputStateParams = await state.get_value('capture_users_state')
        new_user_set = set()
        for group_id in added_id:
            added_items = (await get_groups_by_filters(group_id=group_id)).users

            new_user_set = await add_item_in_aim_set_plus_plus(aim_set=new_user_set, added_item=added_items)
        users_state.set_of_items = new_user_set
        await state.update_data(capture_users_state=users_state)


    # отвечаем заменой сообщения
    state_text = await state_text_builder(state)
    message_text = state_text + '\n' + current_fsm.message_text
    await call.message.edit_text(message_text, reply_markup=current_fsm.reply_kb)
    await call.answer()


# хендлеры поиска слов, введенных с клавиатуры
@setting_colls_router.message(F.text, SetColls.capture_colls_state)
@setting_colls_router.message(F.text, SetColls.capture_groups_state)
@setting_colls_router.message(F.text, SetColls.capture_users_state)
@setting_colls_router.message(F.text, SetColls.capture_dates_state)
async def set_colls_capture_colls_from_message(message: Message, state: FSMContext):
    current_fsm = FSMExecutor()
    # обрабатываем экземпляра класса, который анализирует наш ввод и выдает сообщение и клавиатуру
    await current_fsm.execute(fsm_state=state, fsm_mess=message)
    state_text = await state_text_builder(state)
    message_text = state_text + '\n' + current_fsm.message_text
    await message_answer(source=message, message_text=message_text, reply_markup=current_fsm.reply_kb)


# конечный обработчик всего стейта
@setting_colls_router.callback_query(F.data.startswith(CALL_SET_COLL + CALL_ADD_ENDING), SetColls.confirmation_state)
async def admin_adding_task_capture_confirmation_from_call(call: CallbackQuery, state: FSMContext):
    # вытаскиваем из колбека уровень
    confirm = call.data.replace(CALL_SET_COLL + CALL_ADD_ENDING, '')
    # уходим обратно если нужно что-то изменить

    if confirm == CALL_CHANGING_COLLS or confirm == CALL_CHANGING_USERS or confirm == CALL_CHANGING_DATES:
        confirmation_state: InputStateParams = await state.get_value('confirmation_state')

        if confirm == CALL_CHANGING_COLLS:
            # при нажатии на изменение задаем следующий стейт элементов
            confirmation_state.next_state = SetColls.capture_colls_state
            # делаем так, чтобы в стейте добавления последний стейт (на изменения который) стал следующим
            capture_colls_state: InputStateParams = await state.get_value('capture_colls_state')
            capture_colls_state.next_state = SetColls.confirmation_state
            await state.update_data(capture_colls_state=capture_colls_state)

        elif confirm == CALL_CHANGING_USERS:
            # при нажатии на изменение задаем следующий стейт элементов
            confirmation_state.next_state = SetColls.capture_users_state
            # делаем так, чтобы в стейте добавления последний стейт (на изменения который) стал следующим
            capture_users: InputStateParams = await state.get_value('capture_users_state')
            capture_users.next_state = SetColls.confirmation_state
            await state.update_data(capture_users_state=capture_users)

        elif confirm == CALL_CHANGING_DATES:
            # при нажатии на изменение задаем следующий стейт элементов
            confirmation_state.next_state = SetColls.capture_dates_state
            # делаем так, чтобы в стейте добавления последний стейт (на изменения который) стал следующим
            capture_dates: InputStateParams = await state.get_value('capture_dates_state')
            capture_dates.next_state = SetColls.confirmation_state
            await state.update_data(capture_dates_state=capture_dates)

        await state.update_data(confirmation_state=confirmation_state)
        current_fsm = FSMExecutor()
        await current_fsm.execute(state, call)
        state_text = await state_text_builder(state)
        message_text = state_text + '\n' + current_fsm.message_text
        await call.message.edit_text(message_text, reply_markup=current_fsm.reply_kb)
        await call.answer()

    elif confirm == CALL_CONFIRM:
        # основной обработчик, запись в бд
        author_id = await state.get_value('author_id')

        capture_colls: InputStateParams = await state.get_value('capture_colls_state')
        colls_set = capture_colls.set_of_items

        capture_users: InputStateParams = await state.get_value('capture_users_state')
        users_set = capture_users.set_of_items

        capture_dates: InputStateParams = await state.get_value('capture_dates_state')
        dates_set = capture_dates.set_of_items

        state_text = await state_text_builder(state)

        res = True

        for user in users_set:
            for coll in colls_set:
                for date in dates_set:
                    study_day = datetime.combine(datetime.strptime(date, "%d.%m.%Y"), datetime.now().time())
                    res = res and await set_task(user_id=user, media_id=coll, task_time=study_day, author_id=author_id)


        message_text = f'----- ----- -----\n{state_text}----- ----- -----\n'

        if res:
            message_text += MESS_ADDED_TO_DB
        else:
            message_text += MESS_ERROR_ADDED_TO_DB

        reply_kb = await keyboard_builder(menu_pack=menu_set_colls, buttons_base_call="")

        await call.message.edit_text(message_text, reply_markup=reply_kb)
        await call.answer()



from aiogram import F, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from datetime import datetime, timedelta
from app.database.requests import get_users_by_filters, get_groups_by_filters
from app.utils.admin_utils import (message_answer,
                                   add_item_in_aim_set_plus_plus,
                                   get_word_list_for_kb_with_ids,
                                   get_group_list_for_kb_with_ids,
                                   get_user_list_for_kb_with_ids,
                                   get_date_list_for_kb,
                                   update_button_with_call_base,
                                   state_text_builder)
from app.utils.admin_utils import state_text_builder
import app.database.requests as rq
import app.keyboards.admin_keyboards as akb
from app.handlers.admin_menu.loop_states import (FSMExecutor, StateParams, CaptureWordsStateParams,
                                                 CaptureGroupsStateParams, CaptureUsersStateParams,
                                                 CaptureDatesStateParams)
from app.keyboards.keyboard_builder import keyboard_builder
from app.keyboards.menu_buttons import (button_menu_setting_back, button_main_admin_menu, button_main_menu,
                                        button_change_word, button_change_user, button_change_date)
from app.handlers.common_settings import *
import data.admin_messages as amsg


setting_scheme_router = Router()

class AddScheme(StatesGroup):
    author_id = State() # автор который назначает задание - ид
    capture_words_state = State()
    capture_groups_state = State()
    capture_users_state = State()
    capture_dates_state = State()
    confirmation_state = State() # стейт обрабатывающий конечное подтверждение ввода


# переход в меню добавления задания по схеме
@setting_scheme_router.callback_query(F.data == C_ADM_SET_SCHEME)
async def setting_scheme_first_state(call: CallbackQuery, state: FSMContext):
    # очистка стейта
    await state.clear()
    menu_set_scheme = [
        [button_menu_setting_back, button_main_admin_menu, button_main_menu]
    ]

    menu_set_scheme_with_changing = [
        [update_button_with_call_base(button_change_word, CALL_SET_SCHEME + CALL_ADD_ENDING),
         update_button_with_call_base(button_change_user, CALL_SET_SCHEME + CALL_ADD_ENDING),
         update_button_with_call_base(button_change_date, CALL_SET_SCHEME + CALL_ADD_ENDING)],
        [button_menu_setting_back, button_main_admin_menu, button_main_menu]
    ]

    # задаем в стейт ид автора
    author = await get_users_by_filters(user_tg_id=call.from_user.id)
    await state.update_data(author_id=author.id)

    words_state = CaptureWordsStateParams(self_state = AddScheme.capture_words_state,
                                          next_state = AddScheme.capture_groups_state,
                                          call_base= CALL_SET_SCHEME,
                                          menu_add = menu_set_scheme,
                                          items_kb_list=(await get_word_list_for_kb_with_ids())[::-1])

    await state.update_data(capture_words_state=words_state)

    # здесь добавлен парамент из кэн би эмпти - можно проходить дальше если пустой

    groups_state = CaptureGroupsStateParams(self_state=AddScheme.capture_groups_state,
                                            next_state=AddScheme.capture_users_state,
                                            call_base=CALL_SET_SCHEME,
                                            menu_add=menu_set_scheme,
                                            items_kb_list=await get_group_list_for_kb_with_ids(),
                                            is_can_be_empty=True)

    await state.update_data(capture_groups_state=groups_state)

    users_state = CaptureUsersStateParams(self_state=AddScheme.capture_users_state,
                                          next_state=AddScheme.capture_dates_state,
                                          call_base=CALL_SET_SCHEME,
                                          menu_add=menu_set_scheme,
                                          items_kb_list=await get_user_list_for_kb_with_ids())

    await state.update_data(capture_users_state=users_state)

    dates_state = CaptureDatesStateParams(self_state=AddScheme.capture_dates_state,
                                          next_state=AddScheme.confirmation_state,
                                          call_base=CALL_SET_SCHEME,
                                          menu_add=menu_set_scheme,
                                          items_kb_list=await get_date_list_for_kb(),
                                          is_only_one = True)

    await state.update_data(capture_dates_state=dates_state)

    confirmation_state = StateParams(self_state = AddScheme.confirmation_state,
                                     call_base = CALL_SET_SCHEME,
                                     call_add_capture= CALL_ADD_ENDING,
                                     menu_add = menu_set_scheme_with_changing,
                                     state_main_mess=MESS_ADD_ENDING,
                                     is_last_state_with_changing_mode=True)
    await state.update_data(confirmation_state=confirmation_state)

    first_state = words_state

    # переход в первый стейт
    await state.set_state(first_state.self_state)
    # формируем сообщение, меню, клавиатуру и выводим их
    message_text = first_state.state_main_mess
    reply_kb = await keyboard_builder(menu_pack=first_state.menu_add,
                                      buttons_add_list= first_state.items_kb_list,
                                      buttons_base_call=first_state.call_base + first_state.call_add_capture,
                                      buttons_add_cols=first_state.items_kb_cols,
                                      buttons_add_rows=first_state.items_kb_rows,
                                      is_adding_confirm_button=True)

    await call.message.edit_text(message_text, reply_markup=reply_kb)
    await call.answer()



# цикличные хендлеры захвата слов, пользователей и др.
@setting_scheme_router.callback_query(F.data.startswith(CALL_SET_SCHEME + CALL_CAPTURE_WORD), AddScheme.capture_words_state)
@setting_scheme_router.callback_query(F.data.startswith(CALL_SET_SCHEME + CALL_CAPTURE_GROUP), AddScheme.capture_groups_state)
@setting_scheme_router.callback_query(F.data.startswith(CALL_SET_SCHEME + CALL_CAPTURE_USER), AddScheme.capture_users_state)
@setting_scheme_router.callback_query(F.data.startswith(CALL_SET_SCHEME + CALL_CAPTURE_DATE), AddScheme.capture_dates_state)
async def set_scheme_capture_words_from_call(call: CallbackQuery, state: FSMContext):
    # создаем экземпляр класса для обработки текущего состояния фсм
    current_fsm = FSMExecutor()
    # обрабатываем экземпляра класса, который анализирует наш колл и выдает сообщение и клавиатуру
    await current_fsm.execute(fsm_state=state, fsm_call=call)

    # специальный местный обработчик, который при работе с группами, добавляет сразу пользователей в стейт
    if CALL_CAPTURE_GROUP in call.data:
        text = current_fsm.message_text
        state_text = await state_text_builder(state)
        message_text = text.replace(state_text, '')
        groups_state : StateParams  = await state.get_value('capture_groups_state')
        added_id = groups_state.captured_items_set
        users_state : StateParams = await state.get_value('capture_users_state')
        new_user_set = set()
        for group_id in added_id:
            added_items = (await get_groups_by_filters(group_id=group_id)).users

            new_user_set = await add_item_in_aim_set_plus_plus(aim_set=new_user_set, added_item=added_items)
        users_state.captured_items_set = new_user_set
        await state.update_data(capture_users_state=users_state)
        state_text = await state_text_builder(state)
        current_fsm.message_text = state_text + '\n' + message_text


    # отвечаем заменой сообщения
    await call.message.edit_text(current_fsm.message_text, reply_markup=current_fsm.reply_kb)
    await call.answer()


# хендлеры поиска слов, введенных с клавиатуры
@setting_scheme_router.message(F.text, AddScheme.capture_words_state)
@setting_scheme_router.message(F.text, AddScheme.capture_groups_state)
@setting_scheme_router.message(F.text, AddScheme.capture_users_state)
@setting_scheme_router.message(F.text, AddScheme.capture_dates_state)
async def set_scheme_capture_words_from_message(message: Message, state: FSMContext):
    current_fsm = FSMExecutor()
    # обрабатываем экземпляра класса, который анализирует наш ввод и выдает сообщение и клавиатуру
    await current_fsm.execute(fsm_state=state, fsm_mess=message)
    await message_answer(source=message, message_text=current_fsm.message_text, reply_markup=current_fsm.reply_kb)


# конечный обработчик всего стейта
@setting_scheme_router.callback_query(F.data.startswith(CALL_SET_SCHEME + CALL_ADD_ENDING), AddScheme.confirmation_state)
async def admin_adding_task_capture_confirmation_from_call(call: CallbackQuery, state: FSMContext):
    # вытаскиваем из колбека уровень
    confirm = call.data.replace(CALL_SET_SCHEME + CALL_ADD_ENDING, '')
    # уходим обратно если нужно что-то изменить

    if confirm == CALL_CHANGING_WORD or confirm == CALL_CHANGING_USER or confirm == CALL_CHANGING_DATE:
        confirmation_state: StateParams = await state.get_value('confirmation_state')

        if confirm == CALL_CHANGING_WORD:
            # при нажатии на изменение задаем следующий стейт элементов
            confirmation_state.next_state = AddScheme.capture_words_state
            # делаем так, чтобы в стейте добавления последний стейт (на изменения который) стал следующим
            capture_words: StateParams = await state.get_value('capture_words_state')
            capture_words.next_state = AddScheme.confirmation_state
            await state.update_data(capture_words_state=capture_words)

        elif confirm == CALL_CHANGING_USER:
            # при нажатии на изменение задаем следующий стейт элементов
            confirmation_state.next_state = AddScheme.capture_users_state
            # делаем так, чтобы в стейте добавления последний стейт (на изменения который) стал следующим
            capture_users: StateParams = await state.get_value('capture_users_state')
            capture_users.next_state = AddScheme.confirmation_state
            await state.update_data(capture_users_state=capture_users)

        elif confirm == CALL_CHANGING_DATE:
            # при нажатии на изменение задаем следующий стейт элементов
            confirmation_state.next_state = AddScheme.capture_dates_state
            # делаем так, чтобы в стейте добавления последний стейт (на изменения который) стал следующим
            capture_dates: StateParams = await state.get_value('capture_dates_state')
            capture_dates.next_state = AddScheme.confirmation_state
            await state.update_data(capture_dates_state=capture_dates)

        await state.update_data(confirmation_state=confirmation_state)
        current_fsm = FSMExecutor()
        await current_fsm.execute(state, call)
        await call.message.edit_text(current_fsm.message_text, reply_markup=current_fsm.reply_kb)
        await call.answer()

    else:
        author_id = await state.get_value('author_id')
        capture_words: StateParams = await state.get_value('capture_words_state')
        capture_users: StateParams = await state.get_value('capture_users_state')
        capture_dates: StateParams = await state.get_value('capture_dates_state')

        author_id = author_id
        words_set = capture_words.captured_items_set
        users_set = capture_users.captured_items_set
        dates_set = capture_dates.captured_items_set
        state_text = await state_text_builder(state)

        res = True
        for word in words_set:
            medias = await rq.get_medias_by_filters(word_id=word)
            for media in medias:
                for date in dates_set:
                    assign_date = datetime.strptime(date, "%d.%m.%Y") + timedelta(media.study_day - 1)
                    task_day = datetime.combine(assign_date, datetime.now().time())
                    for user in users_set:
                        res = res and await rq.set_task(user_id=user,
                                                        media_id=media.id,
                                                        task_time=task_day,
                                                        author_id=author_id)

        message_text = f'----- ----- -----\n{state_text}----- ----- -----\n'

        if res:
            message_text += amsg.ADM_ADD_TASK_ADDED
        else:
            message_text += amsg.ADM_ADD_TASK_ERROR

        reply_kb = await akb.admin_adding_menu_kb()
        await call.message.edit_text(message_text, reply_markup=reply_kb)
        await call.answer()





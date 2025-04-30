# from asyncio import current_task
from aiogram.fsm.context import FSMContext
from typing import List
from aiogram.fsm.state import State, StatesGroup
from app.database.models import Media, Source, Task, Word
from aiogram import F, Router
from aiogram.types import CallbackQuery
from app.keyboards.menu_buttons import *
from app.handlers.common_settings import *
from app.database.requests import get_tasks, get_users_by_filters, get_tasks_by_filters, update_task_status, \
    get_medias_by_filters, get_words_by_filters, set_task, get_sources_by_filters
from app.utils.admin_utils import get_new_carousel_page_num, mess_answer, message_answer
from app.keyboards.keyboard_builder import keyboard_builder, update_button_with_call_item
from aiogram.exceptions import TelegramBadRequest
from config import logger
from datetime import datetime, timedelta
from app.handlers.admin_menu.states.state_params import InputStateParams

from app.handlers.admin_menu.states.state_params import InputStateParams
from app.handlers.admin_menu.states.state_executor import FSMExecutor



revision_router = Router()

menu_revision_source = [[button_revision_menu_back, button_main_menu_back]]

menu_revision = [[button_revision_sources_menu, button_revision_words_menu, button_revision_colls_menu],
                 [button_main_menu_back]]

class RevisionState(StatesGroup):
    tasks = State()
    sources = State()
    words = State()
    show_colls = State()


@revision_router.callback_query(F.data == CALL_REVISION_MENU)
async def revision_main(call: CallbackQuery, state: FSMContext):

    await state.clear()
    user_id = (await get_users_by_filters(user_tg_id=call.from_user.id)).id
    print('--------------------------------------------------')
    tasks : List['Task'] = await get_tasks(user_tg_id=call.from_user.id, sent=True, media_task_only=True)
    studied_colls_set = set()
    studied_words_set = set()
    studied_sources_set = set()
    sources = set()
    if tasks:
        for task in tasks:
            if task.media_id:
                studied_colls_set.add(task.media_id)
            if task.media.word_id:
                studied_words_set.add(task.media.word_id)
            if task.media.word.source_id:
                studied_sources_set.add(task.media.word.source_id)
                sources.add(task.media.word.source.source_name)
        # print(sources)

        await state.update_data(words=studied_words_set)
        await state.update_data(colls=studied_colls_set)
        await state.update_data(tasks=tasks)
        await state.set_state(RevisionState.tasks)
    else:
        print('no tasks')
    reply_kb = await keyboard_builder(menu_pack=menu_revision)

    # call_item = call.data.replace(CALL_REVISION_SOURCES_MENU, '')
    # await call.message.edit_text(text=MESS_REVISION_MENU, reply_markup=reply_kb)
    await message_answer(source=call, message_text=MESS_REVISION_MENU, reply_markup=reply_kb)
    await call.answer()

@revision_router.callback_query(F.data == CALL_REVISION_SOURCES_MENU)
@revision_router.callback_query(F.data == CALL_REVISION_WORDS)
@revision_router.callback_query(F.data == CALL_REVISION_COLLS_MENU)
async def setting_state_main(call: CallbackQuery, state: FSMContext):
    tasks: List['Task'] = await get_tasks(user_tg_id=call.from_user.id, sent=True, media_task_only=True)

    if call.data == CALL_REVISION_SOURCES_MENU:
        pass

    elif call.data == CALL_REVISION_WORDS:
        pass



    else:  #if call.data == CALL_REVISION_COLLS_MENU:
        print(f'rev_source_13 - {await state.get_state()}')
        colls_state = InputStateParams(self_state=RevisionState.show_colls,
                                              next_state=RevisionState.show_colls,
                                              call_base=CALL_REVISION_COLLS_MENU,
                                              menu_pack=menu_revision,
                                              is_only_one=True)
        await colls_state.update_state_for_colls_revision(colls_filter='media')
        await state.update_data(show_colls=colls_state)

        message_text = MESS_REVISION_COLLS_MENU

        await state.set_state(RevisionState.show_colls)

        reply_kb = await keyboard_builder(menu_pack=colls_state.menu_pack,
                                          buttons_pack=colls_state.buttons_pack,
                                          buttons_base_call=colls_state.call_base,
                                          buttons_cols=colls_state.buttons_cols,
                                          buttons_rows=colls_state.buttons_rows)

    await call.message.edit_text(text=message_text, reply_markup=reply_kb)
    await call.answer()

@revision_router.callback_query(F.data.startswith(CALL_REVISION_COLLS_MENU), RevisionState.show_colls)
async def set_scheme_capture_words_from_call(call: CallbackQuery, state: FSMContext):

    # создаем экземпляр класса для обработки текущего состояния фсм
    current_fsm = FSMExecutor()
    # обрабатываем экземпляра класса, который анализирует наш колл и выдает сообщение и клавиатуру
    await current_fsm.execute(fsm_state=state, fsm_call=call)
    # отвечаем заменой сообщения

    fsm_state_str = await state.get_state()
    current_state = fsm_state_str.split(':', 1)[1]
    current_state_params: InputStateParams = await state.get_value(current_state)
    media_id = list(current_state_params.set_of_items)[0]

    # media_id = int(call.data.replace(CALL_REVISION_COLLS_MENU, ''))
    media : Media = await get_medias_by_filters(media_id_new=media_id)
    await mess_answer(source=call,
                      media_type=media.media_type,
                      media_id=media.telegram_id,
                      message_text=f'{media.collocation}\n\n{media.caption}',
                      reply_markup=current_fsm.reply_kb)
    await call.answer()


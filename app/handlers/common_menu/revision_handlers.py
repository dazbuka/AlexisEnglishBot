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
from app.handlers.admin_menu.states.input_states import (InputStateParams, FSMExecutor, CaptureLevelsStateParams,
                                                         CaptureDaysStateParams, CaptureWordsStateParams,
                                                         ShowWordsStateParams)



revision_router = Router()

menu_revision_source = [[button_revision_menu_back, button_main_menu_back]]

menu_revision = [[button_revision_sources_menu],
                 [button_revision_words_menu],
                 [button_revision_colls_menu],
                 [button_main_menu_back]]

class RevisionState(StatesGroup):
    tasks = State()
    sources = State()
    words = State()
    colls = State()

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
        print(f'rev_source_11 - {await state.get_state()}')
        base_call = CALL_REVISION_SOURCES_MENU
        base_cols = NUM_SHOW_SOURCES_COLS
        base_rows = NUM_SHOW_SOURCES_ROWS

        sources_id_set = set()
        for task in tasks:
            if task.media.word.source_id:
                sources_id_set.add(task.media.word.source_id)
        sources_kb_buttons = []

        sources = await get_sources_by_filters(source_id_set=sources_id_set)
        for source in sources:
            curr_button = InlineKeyboardButton(text=f'{source.source_name}',
                                               callback_data=f'{CALL_REVISION_SOURCES_MENU}{source.id}')
            sources_kb_buttons.append(curr_button)

        items_kb_buttons = sources_kb_buttons

        message_text = MESS_REVISION_SOURCES_MENU

        await state.set_state(RevisionState.sources)
        await state.update_data(sources=sources_kb_buttons)

    elif call.data == CALL_REVISION_WORDS:
        print(f'rev_source_12 - {await state.get_state()}')
        base_call = CALL_REVISION_WORDS
        base_cols = NUM_SHOW_WORDS_COLS
        base_rows = NUM_SHOW_WORDS_ROWS

        words_id_set = set()
        for task in tasks:
            if task.media.word_id:
                words_id_set.add(task.media.word_id)
        words_kb_buttons = []
        words = await get_words_by_filters(word_id_set=words_id_set)
        for word in words:
            curr_button = InlineKeyboardButton(text=f'{word.word}',
                                               callback_data=f'{CALL_REVISION_WORDS}{word.id}')
            words_kb_buttons.append(curr_button)

        items_kb_buttons = words_kb_buttons

        message_text = MESS_REVISION_WORDS_MENU

        await state.update_data(words=words_kb_buttons)
        await state.set_state(RevisionState.words)

        show_words_state = ShowWordsStateParams(self_state=RevisionState.words,
                                           next_state=RevisionState.colls,
                                           call_base=CALL_REVISION_WORDS,
                                           menu_add=menu_revision,
                                           buttons_kb_list=words_kb_buttons,
                                           is_only_one=True)
        await state.update_data(words=show_words_state)



    else:  #if call.data == CALL_REVISION_COLLS_MENU:
        print(f'rev_source_13 - {await state.get_state()}')
        base_call = CALL_REVISION_COLLS_MENU
        base_cols = NUM_SHOW_COLLS_COLS
        base_rows = NUM_SHOW_COLLS_ROWS

        colls_id_set = set()
        for task in tasks:
            if task.media_id:
                colls_id_set.add(task.media_id)
        colls_kb_buttons = []
        medias = await get_medias_by_filters(media_id_set=colls_id_set)
        for media in medias:
            curr_button = InlineKeyboardButton(text=f'{media.collocation}',
                                               callback_data=f'{CALL_REVISION_COLLS_MENU}{media.id}')
            colls_kb_buttons.append(curr_button)
        items_kb_buttons = colls_kb_buttons

        message_text = MESS_REVISION_COLLS_MENU

        await state.update_data(colls=colls_kb_buttons)
        await state.set_state(RevisionState.colls)

    reply_kb = await keyboard_builder(menu_pack=menu_revision_source,
                                      buttons_add_buttons=items_kb_buttons,
                                      buttons_base_call=base_call,
                                      buttons_add_cols=base_cols,
                                      buttons_add_rows=base_rows)

    await call.message.edit_text(text=message_text, reply_markup=reply_kb)
    await call.answer()

# переход в меню добавления задания по схеме
@revision_router.callback_query(F.data.startswith(CALL_REVISION_SOURCES_MENU), RevisionState.colls)
@revision_router.callback_query(F.data.startswith(CALL_REVISION_SOURCES_MENU), RevisionState.tasks)
@revision_router.callback_query(F.data.startswith(CALL_REVISION_SOURCES_MENU), RevisionState.sources)
async def tasks_main(call: CallbackQuery, state: FSMContext):
    base_call = CALL_REVISION_SOURCES_MENU
    call_item = call.data
    call_item = call_item.replace(base_call,'')
    fsm_state_str = await state.get_state()




    if call_item and fsm_state_str == RevisionState.sources.state:
        print(f'rev_source_1 - call: {call_item} - {await state.get_state()}')
        source_id = int(call_item)
        studied_colls_id_set = set()
        studied_colls_set = set()
        sources = await state.get_value('tasks')
        for task in sources:
            if task.media.word.source_id == source_id:
                studied_colls_id_set.add(task.media_id)

        sources_kb_buttons = []
        buttons_page = 0
        for coll_id in studied_colls_id_set:
            media: Media = await get_medias_by_filters(media_id_new=coll_id)
            curr_button = InlineKeyboardButton(text=f'{media.collocation}',
                                               callback_data=f'{CALL_REVISION_SOURCES_MENU}{media.id}')
            sources_kb_buttons.append(curr_button)

        await state.update_data(sources=sources_kb_buttons)

        reply_kb = await keyboard_builder(menu_pack=menu_revision_source,
                                          buttons_add_buttons=sources_kb_buttons,
                                          buttons_base_call=CALL_REVISION_SOURCES_MENU,
                                          buttons_add_cols=NUM_SHOW_SOURCES_COLS,
                                          buttons_add_rows=NUM_SHOW_SOURCES_ROWS,
                                          is_adding_confirm_button=False,
                                          buttons_add_table_number=buttons_page)
        message_text = MESS_REVISION_SOURCES_MENU
        await call.message.edit_text(text=message_text, reply_markup=reply_kb)
        await call.answer()
        await state.set_state(RevisionState.colls)


    elif call_item and fsm_state_str == RevisionState.colls.state:
        print(f'rev_source_2 - call: {call_item} - {await state.get_state()}')
        coll_id = int(call_item)
        curr_media : Media = await get_medias_by_filters(media_id_new=coll_id)
        colls_kb_buttons = await state.get_value('sources')

        sources_kb_buttons = colls_kb_buttons
        buttons_page = 0

        add_word_id = str(curr_media.word_id)
        add_media_id = str(curr_media.id)

        menu_revision_source_with_def_and_trans = [[update_button_with_call_item(button_definition, add_word_id),
                                                    update_button_with_call_item(button_translation, add_word_id),
                                                    update_button_with_call_item(button_repeat_today, add_media_id)],
                                                   [button_revision_menu_back, button_main_menu_back]]

        reply_kb = await keyboard_builder(menu_pack=menu_revision_source_with_def_and_trans,
                                          buttons_add_buttons=sources_kb_buttons,
                                          buttons_base_call=CALL_REVISION_SOURCES_MENU,
                                          buttons_add_cols=NUM_SHOW_SOURCES_COLS,
                                          buttons_add_rows=NUM_SHOW_SOURCES_ROWS,
                                          is_adding_confirm_button=False,
                                          buttons_add_table_number=buttons_page)

        message_text = f'Collocation: {curr_media.collocation}'
        if curr_media.caption:
            message_text += f'\n\n{curr_media.caption}'


        await mess_answer(source=call,
                          media_type=curr_media.media_type,
                          media_id=curr_media.telegram_id,
                          message_text=message_text,
                          reply_markup=reply_kb)
        await call.answer()

        # words = await get_words_by_filters(source_id=call_item)
        #             print(words)
        #             words_kb_buttons_new = []
        #             for word in words:
        #                 curr_button = InlineKeyboardButton(text=f'{word.word}',
        #                                                    callback_data=f'{CALL_REVISION_SOURCES_MENU}word{word.id}')
        #                 words_kb_buttons_new.append(curr_button)
        #             buttons_page = 0
        #
        #             reply_kb = await keyboard_builder(menu_pack=menu_revision_source,
        #                                               buttons_add_buttons=words_kb_buttons_new,
        #                                               buttons_base_call=CALL_QUICK_MENU,
        #                                               buttons_add_cols=NUM_SHOW_TASKS_COLS,
        #                                               buttons_add_rows=NUM_SHOW_TASKS_ROWS,
        #                                               is_adding_confirm_button=False,
        #                                               buttons_add_table_number=buttons_page)
        #             message_text = MESS_SHOW_TASKS
        #             await call.message.edit_text(text=message_text, reply_markup=reply_kb)
    else:
        print(f'rev_source_3 - call: {call_item} - {await state.get_state()}')
        studied_sources_id_set = set()
        studied_sources_set = set()
        sources = await state.get_value('tasks')
        for task in sources:
            if task.media.word.source_id:
                studied_sources_id_set.add(task.media.word.source_id)
                studied_sources_set.add(task.media.word.source.source_name)

        print(studied_sources_id_set)
        print(studied_sources_set)
        sources_kb_buttons = []
        buttons_page = 0
        for source_id in studied_sources_id_set:
            source : Source = await get_sources_by_filters(source_id=source_id)
            curr_button = InlineKeyboardButton(text=f'{source.source_name}',
                                               callback_data=f'{CALL_REVISION_SOURCES_MENU}{source.id}')
            sources_kb_buttons.append(curr_button)
        reply_kb = await keyboard_builder(menu_pack=menu_revision_source,
                                          buttons_add_buttons=sources_kb_buttons,
                                          buttons_base_call=CALL_REVISION_SOURCES_MENU,
                                          buttons_add_cols=NUM_SHOW_SOURCES_COLS,
                                          buttons_add_rows=NUM_SHOW_SOURCES_ROWS,
                                          is_adding_confirm_button=False,
                                          buttons_add_table_number=buttons_page)
        message_text = MESS_REVISION_SOURCES_MENU
        await call.message.edit_text(text=message_text, reply_markup=reply_kb)
        await call.answer()

        await state.set_state(RevisionState.sources)



    # user_id = (await get_users_by_filters(user_tg_id=call.from_user.id)).id
    # print('here 111')
    # buttons_page = 0
    # colls_kb_buttons = []
    # sources_kb_buttons = []
    # sources = await get_sources_by_filters()
    # print(sources)
    # call_item = call.data.replace(CALL_REVISION_SOURCES_MENU, '')
    #
    # if sources:
    #     print('-------------r1--------------')
    #     if call_item:
    #         print('r2')
    #         if (call_item.startswith(CALL_NEXT) or call_item.startswith(CALL_LAST) or
    #                 call_item.startswith(CALL_PREV) or call_item.startswith(CALL_FIRST)):
    #             print('r3')
    #             tasks_new = await get_tasks(user_tg_id=call.from_user.id, sent=False, media_task_only=True)
    #             tasks_kb_buttons_new = []
    #             for task in tasks_new:
    #                 curr_button = InlineKeyboardButton(text=f'{task.media.collocation}',
    #                                                    callback_data=f'{CALL_QUICK_MENU}{task.id}')
    #                 tasks_kb_buttons_new.append(curr_button)
    #             buttons_page = await get_new_carousel_page_num(call_item=call_item,
    #                                                        items_kb=tasks_kb_buttons_new,
    #                                                        cols=NUM_SHOW_TASKS_COLS,
    #                                                        rows=NUM_SHOW_TASKS_ROWS)
    #
    #
    #
    #             reply_kb = await keyboard_builder(menu_pack=menu_revision_source,
    #                                               buttons_add_buttons=tasks_kb_buttons_new,
    #                                               buttons_base_call=CALL_QUICK_MENU,
    #                                               buttons_add_cols=NUM_SHOW_TASKS_COLS,
    #                                               buttons_add_rows=NUM_SHOW_TASKS_ROWS,
    #                                               is_adding_confirm_button=False,
    #                                               buttons_add_table_number=buttons_page)
    #             message_text = MESS_QUICK_MENU
    #             await call.message.edit_text(text=message_text, reply_markup=reply_kb)
    #         elif call_item.startswith('source'):
    #
    #             print('rs3 begin')
    #             print(call_item)
    #             call_item = int(call_item.replace('source',''))
    #             print(call_item)
    #             words = await get_words_by_filters(source_id=call_item)
    #             print(words)
    #             words_kb_buttons_new = []
    #             for word in words:
    #                 curr_button = InlineKeyboardButton(text=f'{word.word}',
    #                                                    callback_data=f'{CALL_REVISION_SOURCES_MENU}word{word.id}')
    #                 words_kb_buttons_new.append(curr_button)
    #             buttons_page = 0
    #
    #             reply_kb = await keyboard_builder(menu_pack=menu_revision_source,
    #                                               buttons_add_buttons=words_kb_buttons_new,
    #                                               buttons_base_call=CALL_QUICK_MENU,
    #                                               buttons_add_cols=NUM_SHOW_TASKS_COLS,
    #                                               buttons_add_rows=NUM_SHOW_TASKS_ROWS,
    #                                               is_adding_confirm_button=False,
    #                                               buttons_add_table_number=buttons_page)
    #             message_text = MESS_SHOW_TASKS
    #             await call.message.edit_text(text=message_text, reply_markup=reply_kb)
    #
    #
    #         elif call_item.startswith('word'):
    #
    #             print('rw3 begin')
    #             print(call_item)
    #             call_item = int(call_item.replace('word',''))
    #             print(call_item)
    #             medias = await get_medias_by_filters(word_id=call_item)
    #             medias_kb_buttons_new = []
    #             for media in medias:
    #                 curr_button = InlineKeyboardButton(text=f'{media.collocation}',
    #                                                    callback_data=f'{CALL_REVISION_SOURCES_MENU}media{media.id}')
    #                 medias_kb_buttons_new.append(curr_button)
    #             buttons_page = 0
    #
    #             reply_kb = await keyboard_builder(menu_pack=menu_revision_source,
    #                                               buttons_add_buttons=medias_kb_buttons_new,
    #                                               buttons_base_call=CALL_QUICK_MENU,
    #                                               buttons_add_cols=NUM_SHOW_TASKS_COLS,
    #                                               buttons_add_rows=NUM_SHOW_TASKS_ROWS,
    #                                               is_adding_confirm_button=False,
    #                                               buttons_add_table_number=buttons_page)
    #             message_text = MESS_SHOW_TASKS
    #             await call.message.edit_text(text=message_text, reply_markup=reply_kb)
    #
    #
    #         elif call_item.startswith('media'):
    #             print('rw3 begin')
    #             print(call_item)
    #             call_item = int(call_item.replace('media', ''))
    #             print(call_item)
    #             curr_media = await get_medias_by_filters(media_id_new=call_item)
    #             medias = await get_medias_by_filters(word_id=curr_media.word_id)
    #
    #             medias_kb_buttons_new = []
    #             for media in medias:
    #                 curr_button = InlineKeyboardButton(text=f'{media.collocation}',
    #                                                    callback_data=f'{CALL_REVISION_SOURCES_MENU}media{media.id}')
    #                 medias_kb_buttons_new.append(curr_button)
    #             buttons_page = 0
    #
    #             reply_kb = await keyboard_builder(menu_pack=menu_revision_source,
    #                                               buttons_add_buttons=medias_kb_buttons_new,
    #                                               buttons_base_call=CALL_REVISION_SOURCES_MENU,
    #                                               buttons_add_cols=NUM_SHOW_SOURCES_COLS,
    #                                               buttons_add_rows=NUM_SHOW_SOURCES_ROWS,
    #                                               is_adding_confirm_button=False,
    #                                               buttons_add_table_number=buttons_page)
    #
    #             message_text = f'Collocation: {curr_media.collocation}'
    #             if curr_media.caption:
    #                 message_text += f'\n\n{curr_media.caption}'
    #
    #
    #             await mess_answer(source=call,
    #                               media_type=curr_media.media_type,
    #                               media_id=curr_media.telegram_id,
    #                               message_text=message_text,
    #                               reply_markup=reply_kb)
    #             await call.answer()
    #
    #         else:
    #             print('r4')
    #             # media = await get_medias_by_filters(media_id=int(call_item))
    #             curr_task = await get_tasks_by_filters(task_id_new=int(call_item))
    #             await update_task_status(task_id = curr_task.id)
    #             message_text = f'Collocation: {curr_task.media.collocation}'
    #             if curr_task.media.caption:
    #                 message_text += f'\n\n{curr_task.media.caption}'
    #
    #             tasks_new = await get_tasks(user_tg_id=call.from_user.id, sent=False, media_task_only=True)
    #             tasks_kb_buttons_new=[]
    #             for task in tasks_new:
    #                 curr_button = InlineKeyboardButton(text=f'{task.media.collocation}',
    #                                                    callback_data=f'{CALL_QUICK_MENU}{task.id}')
    #                 tasks_kb_buttons_new.append(curr_button)
    #
    #
    #             add_word_id = str(curr_task.media.word_id)
    #             add_media_id = str(curr_task.media.id)
    #
    #             menu_tasks_with_def_and_trans = [
    #                 [update_button_with_call_item(button_definition, add_word_id),
    #                  update_button_with_call_item(button_translation, add_word_id)],
    #                 [update_button_with_call_item(button_repeat_today, add_media_id),
    #                  update_button_with_call_item(button_repeat_tomorrow, add_media_id)],
    #                 [button_main_menu]
    #             ]
    #
    #             reply_kb = await keyboard_builder(menu_pack=menu_tasks_with_def_and_trans,
    #                                               buttons_add_buttons=tasks_kb_buttons_new,
    #                                               buttons_base_call=CALL_REVISION_SOURCES_MENU,
    #                                               buttons_add_cols=NUM_SHOW_SOURCES_COLS,
    #                                               buttons_add_rows=NUM_SHOW_SOURCES_ROWS,
    #                                               is_adding_confirm_button=False,
    #                                               buttons_add_table_number=buttons_page)
    #             await mess_answer(source=call,
    #                               media_type=curr_task.media.media_type,
    #                               media_id=curr_task.media.telegram_id,
    #                               message_text=message_text,
    #                               reply_markup=reply_kb)
    #             await call.answer()
    #     else:
    #         print('r5')
    #         for source in sources:
    #             curr_button = InlineKeyboardButton(text=f'{source.source_name}',
    #                                                callback_data=f'{CALL_REVISION_SOURCES_MENU}source{source.id}')
    #             sources_kb_buttons.append(curr_button)
    #         reply_kb = await keyboard_builder(menu_pack=[[button_main_menu]],
    #                                           buttons_add_buttons=sources_kb_buttons,
    #                                           buttons_base_call=CALL_REVISION_SOURCES_MENU,
    #                                           buttons_add_cols=NUM_SHOW_SOURCES_COLS,
    #                                           buttons_add_rows=NUM_SHOW_SOURCES_ROWS,
    #                                           is_adding_confirm_button=False,
    #                                           buttons_add_table_number=buttons_page)
    #         message_text = MESS_REVISION_SOURCES_MENU
    #         await call.message.edit_text(text=message_text, reply_markup=reply_kb)
    #
    #
    # else:
    #     print('r6')
    #     message_text = MESS_REVISION_SOURCES_MENU_EMPTY
    #     reply_kb = await keyboard_builder(menu_pack=[[button_main_menu]],
    #                                       buttons_add_buttons=colls_kb_buttons,
    #                                       buttons_base_call=CALL_REVISION_SOURCES_MENU,
    #                                       buttons_add_cols=NUM_SHOW_SOURCES_COLS,
    #                                       buttons_add_rows=NUM_SHOW_SOURCES_ROWS,
    #                                       is_adding_confirm_button=False,
    #                                       buttons_add_table_number=buttons_page)
    #
    #     await call.message.edit_text(text=message_text, reply_markup=reply_kb)
    # await call.answer()


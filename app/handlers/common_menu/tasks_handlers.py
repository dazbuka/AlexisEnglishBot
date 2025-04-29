from asyncio import current_task

from aiogram import F, Router
from aiogram.types import CallbackQuery
from app.keyboards.menu_buttons import *
from app.handlers.common_settings import *
from app.database.requests import get_tasks, get_users_by_filters, get_tasks_by_filters, update_task_status, \
    get_medias_by_filters, get_words_by_filters, set_task
from app.utils.admin_utils import get_new_carousel_page_num, mess_answer
from app.keyboards.keyboard_builder import keyboard_builder, update_button_with_call_item
from aiogram.exceptions import TelegramBadRequest
from config import logger
from datetime import datetime, timedelta

tasks_router = Router()

menu_tasks = [
    [button_main_menu]
]

# переход в меню добавления задания по схеме
@tasks_router.callback_query(F.data.startswith(CALL_QUICK_MENU))
async def tasks_main(call: CallbackQuery):
    user_id = (await get_users_by_filters(user_tg_id=call.from_user.id)).id
    print('here 111')
    buttons_page = 0
    tasks_kb_buttons = []
    tasks = await get_tasks(user_tg_id=call.from_user.id, sent=False, media_task_only=True)
    call_item = call.data.replace(CALL_QUICK_MENU, '')

    if tasks:
        print('-------------t1--------------')
        if call_item:
            print('t2')
            if (call_item.startswith(CALL_NEXT) or call_item.startswith(CALL_LAST) or
                    call_item.startswith(CALL_PREV) or call_item.startswith(CALL_FIRST)):
                print('t3')
                tasks_new = await get_tasks(user_tg_id=call.from_user.id, sent=False, media_task_only=True)
                tasks_kb_buttons_new = []
                for task in tasks_new:
                    curr_button = InlineKeyboardButton(text=f'{task.media.collocation}',
                                                       callback_data=f'{CALL_QUICK_MENU}{task.id}')
                    tasks_kb_buttons_new.append(curr_button)
                buttons_page = await get_new_carousel_page_num(call_item=call_item,
                                                           items_kb=tasks_kb_buttons_new,
                                                           cols=NUM_SHOW_TASKS_COLS,
                                                           rows=NUM_SHOW_TASKS_ROWS)



                reply_kb = await keyboard_builder(menu_pack=menu_tasks,
                                                  buttons_pack=tasks_kb_buttons_new,
                                                  buttons_base_call=CALL_QUICK_MENU,
                                                  buttons_cols=NUM_SHOW_TASKS_COLS,
                                                  buttons_rows=NUM_SHOW_TASKS_ROWS,
                                                  is_adding_confirm_button=False,
                                                  buttons_page_number=buttons_page)
                message_text = MESS_QUICK_MENU
                await call.message.edit_text(text=message_text, reply_markup=reply_kb)
            else:
                print('t4')
                # media = await get_medias_by_filters(media_id=int(call_item))
                curr_task = await get_tasks_by_filters(task_id_new=int(call_item))
                await update_task_status(task_id = curr_task.id)
                message_text = f'Collocation: {curr_task.media.collocation}'
                if curr_task.media.caption:
                    message_text += f'\n\n{curr_task.media.caption}'

                tasks_new = await get_tasks(user_tg_id=call.from_user.id, sent=False, media_task_only=True)
                tasks_kb_buttons_new=[]
                for task in tasks_new:
                    curr_button = InlineKeyboardButton(text=f'{task.media.collocation}',
                                                       callback_data=f'{CALL_QUICK_MENU}{task.id}')
                    tasks_kb_buttons_new.append(curr_button)


                add_word_id = str(curr_task.media.word_id)
                add_media_id = str(curr_task.media.id)

                menu_tasks_with_def_and_trans = [
                    [update_button_with_call_item(button_definition, add_word_id),
                     update_button_with_call_item(button_translation, add_word_id)],
                    [update_button_with_call_item(button_repeat_today, add_media_id),
                     update_button_with_call_item(button_repeat_tomorrow, add_media_id)],
                    [button_main_menu]
                ]

                reply_kb = await keyboard_builder(menu_pack=menu_tasks_with_def_and_trans,
                                                  buttons_pack=tasks_kb_buttons_new,
                                                  buttons_base_call=CALL_QUICK_MENU,
                                                  buttons_cols=NUM_SHOW_TASKS_COLS,
                                                  buttons_rows=NUM_SHOW_TASKS_ROWS,
                                                  is_adding_confirm_button=False,
                                                  buttons_page_number=buttons_page)
                await mess_answer(source=call,
                                  media_type=curr_task.media.media_type,
                                  media_id=curr_task.media.telegram_id,
                                  message_text=message_text,
                                  reply_markup=reply_kb)
                await call.answer()
        else:
            print('t5')
            for task in tasks:
                curr_button = InlineKeyboardButton(text=f'{task.media.collocation}',
                                                   callback_data=f'{CALL_QUICK_MENU}{task.id}')
                tasks_kb_buttons.append(curr_button)
            reply_kb = await keyboard_builder(menu_pack=[[button_main_menu]],
                                              buttons_pack=tasks_kb_buttons,
                                              buttons_base_call=CALL_QUICK_MENU,
                                              buttons_cols=NUM_SHOW_TASKS_COLS,
                                              buttons_rows=NUM_SHOW_TASKS_ROWS,
                                              is_adding_confirm_button=False,
                                              buttons_page_number=buttons_page)
            message_text = MESS_QUICK_MENU
            await call.message.edit_text(text=message_text, reply_markup=reply_kb)


    else:
        print('t6')
        message_text = MESS_QUICK_MENU_EMPTY
        reply_kb = await keyboard_builder(menu_pack=[[button_main_menu]],
                                          buttons_pack=tasks_kb_buttons,
                                          buttons_base_call=CALL_QUICK_MENU,
                                          buttons_cols=NUM_SHOW_TASKS_COLS,
                                          buttons_rows=NUM_SHOW_TASKS_ROWS,
                                          is_adding_confirm_button=False,
                                          buttons_page_number=buttons_page)

        await call.message.edit_text(text=message_text, reply_markup=reply_kb)
    await call.answer()

@tasks_router.callback_query(F.data.startswith(CALL_DEFINITION))
async def tasks_main2(call: CallbackQuery):
    word_id = int(call.data.replace(CALL_DEFINITION, ''))
    word = await get_words_by_filters(word_id_new=word_id)
    try:
        await call.answer(f'{word.word} - {word.definition}', show_alert=True)
    except TelegramBadRequest as e:
        logger.error(f'{call.from_user.username} ({call.from_user.first_name})'
                     f' - ошибка definition для {word.word} *{call.data}*: {e}')
        await call.answer(f"Can't show definition, because it is too long", show_alert=True)


@tasks_router.callback_query(F.data.startswith(CALL_TRANSLATION))
async def tasks_main2(call: CallbackQuery):
    word_id = int(call.data.replace(CALL_TRANSLATION, ''))
    word = await get_words_by_filters(word_id_new=word_id)
    try:
        await call.answer(f'{word.word} - {word.translation}', show_alert=True)
    except TelegramBadRequest as e:
        logger.error(f'{call.from_user.username} ({call.from_user.first_name})'
                     f' - ошибка translation для {word.word} *{call.data}*: {e}')
        await call.answer(f"Can't show definition, because it is too long", show_alert=True)


@tasks_router.callback_query(F.data.startswith(CALL_REPEAT_TODAY))
async def repeat_today(call: CallbackQuery):
    # вытаскиваем из колбека номер коллокации и пользователя
    media_id=int(call.data.replace(CALL_REPEAT_TODAY, ''))
    user = await get_users_by_filters(user_tg_id=call.from_user.id)
    # добавляем задание на сегодня
    await set_task(user_id=user.id, media_id=media_id, task_time=datetime.now(), author_id=user.id)
    await call.answer('Task added')


# инлайн кнопка отправки медиа на повторение завтра
@tasks_router.callback_query(F.data.startswith(CALL_REPEAT_TOMORROW))
async def repeat_tomorrow(call: CallbackQuery):
    # вытаскиваем из колбека номер коллокации и пользователя
    media_id=int(call.data.replace(CALL_REPEAT_TOMORROW, ''))
    user = await get_users_by_filters(user_tg_id=call.from_user.id)
    # добавляем задание на завтра
    await set_task(user_id=user.id, media_id=media_id, task_time=datetime.now()+timedelta(days=1), author_id=user.id)
    await call.answer('Task added')
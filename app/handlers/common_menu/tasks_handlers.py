from asyncio import current_task

from aiogram import F, Router
from aiogram.types import CallbackQuery
from app.keyboards.menu_buttons import *
from app.handlers.common_settings import *
from app.database.requests import get_tasks, get_users_by_filters, get_tasks_by_filters, update_task_status, \
    get_medias_by_filters
from app.utils.admin_utils import get_new_carousel_page_num, mess_answer
from app.keyboards.keyboard_builder import keyboard_builder

tasks_router = Router()

menu_tasks = [
    [button_main_menu]
]

# переход в меню добавления задания по схеме
@tasks_router.callback_query(F.data.startswith(CALL_TASKS_MENU))
async def tasks_main(call: CallbackQuery):
    user_id = (await get_users_by_filters(user_tg_id=call.from_user.id)).id
    print('here 111')
    buttons_page = 0
    tasks_kb_buttons = []
    tasks = await get_tasks(user_tg_id=call.from_user.id, sent=False, media_task_only=True)
    call_item = call.data.replace(CALL_TASKS_MENU, '')

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
                                                       callback_data=f'{CALL_TASKS_MENU}{task.id}')
                    tasks_kb_buttons_new.append(curr_button)
                buttons_page = await get_new_carousel_page_num(call_item=call_item,
                                                           items_kb=tasks_kb_buttons_new,
                                                           cols=NUM_SHOW_TASKS_COLS,
                                                           rows=NUM_SHOW_TASKS_ROWS)

                reply_kb = await keyboard_builder(menu_pack=[[button_main_menu]],
                                                  buttons_add_buttons=tasks_kb_buttons_new,
                                                  buttons_base_call=CALL_TASKS_MENU,
                                                  buttons_add_cols=NUM_SHOW_TASKS_COLS,
                                                  buttons_add_rows=NUM_SHOW_TASKS_ROWS,
                                                  is_adding_confirm_button=False,
                                                  buttons_add_table_number=buttons_page)
                message_text = MESS_TASKS_MENU
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
                                                       callback_data=f'{CALL_TASKS_MENU}{task.id}')
                    tasks_kb_buttons_new.append(curr_button)

                reply_kb = await keyboard_builder(menu_pack=[[button_main_menu]],
                                                  buttons_add_buttons=tasks_kb_buttons_new,
                                                  buttons_base_call=CALL_TASKS_MENU,
                                                  buttons_add_cols=NUM_SHOW_TASKS_COLS,
                                                  buttons_add_rows=NUM_SHOW_TASKS_ROWS,
                                                  is_adding_confirm_button=False,
                                                  buttons_add_table_number=buttons_page)
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
                                                   callback_data=f'{CALL_TASKS_MENU}{task.id}')
                tasks_kb_buttons.append(curr_button)
            reply_kb = await keyboard_builder(menu_pack=[[button_main_menu]],
                                              buttons_add_buttons=tasks_kb_buttons,
                                              buttons_base_call=CALL_TASKS_MENU,
                                              buttons_add_cols=NUM_SHOW_TASKS_COLS,
                                              buttons_add_rows=NUM_SHOW_TASKS_ROWS,
                                              is_adding_confirm_button=False,
                                              buttons_add_table_number=buttons_page)
            message_text = MESS_TASKS_MENU
            await call.message.edit_text(text=message_text, reply_markup=reply_kb)


    else:
        print('t6')
        message_text = MESS_TASKS_MENU_EMPTY
        reply_kb = await keyboard_builder(menu_pack=[[button_main_menu]],
                                          buttons_add_buttons=tasks_kb_buttons,
                                          buttons_base_call=CALL_TASKS_MENU,
                                          buttons_add_cols=NUM_SHOW_TASKS_COLS,
                                          buttons_add_rows=NUM_SHOW_TASKS_ROWS,
                                          is_adding_confirm_button=False,
                                          buttons_add_table_number=buttons_page)

        await call.message.edit_text(text=message_text, reply_markup=reply_kb)
    await call.answer()


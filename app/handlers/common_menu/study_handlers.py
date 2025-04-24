from aiogram import F, Router
from aiogram.types import CallbackQuery
from app.keyboards.menu_buttons import *
from app.handlers.common_settings import *
from app.database.requests import get_tasks_for_study, get_users_by_filters
from app.utils.admin_utils import get_new_carousel_page_num
from app.keyboards.keyboard_builder import keyboard_builder

study_router = Router()

menu_study = [
    [button_main_menu]
]

# переход в меню добавления задания по схеме
@study_router.callback_query(F.data.startswith(CALL_STUDY_MENU))
async def study_main(call: CallbackQuery):
    user_id = (await get_users_by_filters(user_tg_id=call.from_user.id)).id
    print('here 111')
    buttons_page = 0
    tasks_kb_buttons = []
    tasks = await get_tasks_for_study(user_tg_id=call.from_user.id, sent=False, media_task_only=True)

    call_item = call.data.replace(CALL_STUDY_MENU, '')

    if tasks:

        print(call_item)
        for task in tasks:
            # print(task.media.collocation)
            curr_button = InlineKeyboardButton(text=f'{task.media.collocation}',
                                               callback_data=f'{CALL_STUDY_MENU}{task.media.id}')
            tasks_kb_buttons.append(curr_button)
        if call_item:
            print('yesssssssssssssssssss')
            buttons_page = await get_new_carousel_page_num(call_item=call_item,
                                                           items_kb=tasks_kb_buttons,
                                                           cols=NUM_SHOW_TASKS_COLS,
                                                           rows=NUM_SHOW_TASKS_ROWS)
        message_text = MESS_TASKS_MENU
    else:
        message_text = MESS_TASKS_MENU_EMPTY
    reply_kb = await keyboard_builder(menu_pack=[[button_main_menu]],
                                      buttons_add_buttons=tasks_kb_buttons,
                                      buttons_base_call=CALL_STUDY_MENU,
                                      buttons_add_cols=NUM_SHOW_TASKS_COLS,
                                      buttons_add_rows=NUM_SHOW_TASKS_ROWS,
                                      is_adding_confirm_button=False,
                                      buttons_add_table_number=buttons_page)

    await call.message.edit_text(text=message_text, reply_markup=reply_kb)
    await call.answer()


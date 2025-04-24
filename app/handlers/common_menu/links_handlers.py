import os
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from datetime import datetime

from app.keyboards.menu_buttons import *
from app.handlers.common_settings import *

from app.database.requests import get_links_by_filters, add_media_to_db, get_users_by_filters
from app.utils.admin_utils import (get_new_carousel_page_num, state_text_builder, mess_answer,
                                   get_word_list_for_kb_with_ids,
                                   get_day_list_for_kb,
                                   get_shema_text_by_word_id     )

import app.keyboards.admin_keyboards as akb
from config import bot, media_dir
from app.handlers.admin_menu.states.input_states import (StateParams, FSMExecutor, CaptureLevelsStateParams,
                                                         CaptureDaysStateParams, CaptureWordsStateParams)

from app.keyboards.keyboard_builder import keyboard_builder, update_button_with_call_base

links_router = Router()

menu_links = [
    [button_main_menu]
]


# переход в меню добавления задания по схеме
@links_router.callback_query(F.data.startswith(CALL_LINKS_MENU))
async def adding_word_first_state(call: CallbackQuery):

    user = await get_users_by_filters(user_tg_id=call.from_user.id)
    user_id = user.id
    buttons_page = 0
    link_kb_buttons = []
    print(user_id)
    links = await get_links_by_filters(user_id=user_id)
    if links:
        for link in links:
            curr_button = InlineKeyboardButton(text=link.name, url=link.link)
            link_kb_buttons.append(curr_button)

        item = call.data.replace(CALL_LINKS_MENU, '')
        if item:
            buttons_page = await get_new_carousel_page_num(call=item, items_kb=link_kb_buttons, rows=2, cols=1)
        message_text = MESS_LINKS_MENU
    else:
        message_text = MESS_LINKS_MENU_EMPTY
    reply_kb = await keyboard_builder(menu_pack=menu_links,
                                      # buttons_add_list= items,
                                      buttons_add_buttons=link_kb_buttons,
                                      buttons_base_call=CALL_LINKS_MENU,
                                      buttons_add_cols=1,
                                      buttons_add_rows=2,
                                      is_adding_confirm_button=False,
                                      buttons_add_table_number=buttons_page)


    await call.message.edit_text(text=message_text, reply_markup=reply_kb)

    await call.answer()


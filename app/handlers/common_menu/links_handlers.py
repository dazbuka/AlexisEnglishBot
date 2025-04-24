from aiogram import F, Router
from aiogram.types import CallbackQuery
from app.keyboards.menu_buttons import *
from app.handlers.common_settings import *
from app.database.requests import get_links_by_filters, get_users_by_filters
from app.utils.admin_utils import get_new_carousel_page_num
from app.keyboards.keyboard_builder import keyboard_builder
links_router = Router()

# переход в меню добавления задания по схеме
@links_router.callback_query(F.data.startswith(CALL_LINKS_MENU))
async def adding_word_first_state(call: CallbackQuery):
    user_id = (await get_users_by_filters(user_tg_id=call.from_user.id)).id
    buttons_page = 0
    link_kb_buttons = []
    links = await get_links_by_filters(user_id=user_id)
    if links:
        call_item = call.data.replace(CALL_LINKS_MENU, '')
        for link in links:
            curr_button = InlineKeyboardButton(text=link.name, url=link.link)
            link_kb_buttons.append(curr_button)
        if call_item:
            buttons_page = await get_new_carousel_page_num(call_item=call_item,
                                                           items_kb=link_kb_buttons,
                                                           cols=NUM_SHOW_LINKS_COLS,
                                                           rows=NUM_SHOW_LINKS_ROWS)
        message_text = MESS_LINKS_MENU
    else:
        message_text = MESS_LINKS_MENU_EMPTY
    reply_kb = await keyboard_builder(menu_pack=[[button_main_menu]],
                                      buttons_add_buttons=link_kb_buttons,
                                      buttons_base_call=CALL_LINKS_MENU,
                                      buttons_add_cols=NUM_SHOW_LINKS_COLS,
                                      buttons_add_rows=NUM_SHOW_LINKS_ROWS,
                                      is_adding_confirm_button=False,
                                      buttons_add_table_number=buttons_page)

    await call.message.edit_text(text=message_text, reply_markup=reply_kb)
    await call.answer()


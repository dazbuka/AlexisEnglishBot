from aiogram.types import (
    InlineKeyboardButton
)
from data.admin_messages import *
from app.handlers.common_settings import *
import app.handlers.callback_messages as callmsg
import data.common_messages as cmsg
import data.admin_messages as amsg

from app.handlers.common_settings import (CALL_CONFIRM)

from app.handlers.common_settings import (TEXT_CHANGE_WORDS, TEXT_BUTTON_CONFIRM, TEXT_CHANGE_USER,
                                          TEXT_CHANGE_DATE)


button_new_main_menu = InlineKeyboardButton(text=BTEXT_MAIN_MENU, callback_data=CALL_MAIN_MENU)

button_new_admin_menu = InlineKeyboardButton(text=BTEXT_ADMIN_MENU, callback_data=CALL_ADMIN_MENU)





new_menu_button = InlineKeyboardButton(text='new_menu_button', callback_data='new_menu_button')


button_menu_setting_back = InlineKeyboardButton(text=T_ADM_MENU_SETTING_BACK,
                                                callback_data=CALL_SETTING_MENU)


button_adm_menu_adding = InlineKeyboardButton(text=TEXT_MENU_ADDING, callback_data=CALL_ADDING_MENU)
button_menu_adding_back = InlineKeyboardButton(text=TEXT_MENU_ADDING_BACK, callback_data=CALL_ADDING_MENU)


button_adding_menu = InlineKeyboardButton(text=ADMIN_BUTTON_ADDING_MENU, callback_data=ADMIN_BUTTON_ADDING_MENU)













button_main_admin_menu = InlineKeyboardButton(text=ADMIN_BUTTON_MAIN_ADMIN_MENU,
                                                  callback_data=ADMIN_BUTTON_MAIN_ADMIN_MENU)
button_main_menu = InlineKeyboardButton(text=ADMIN_BUTTON_MAIN_MENU,
                                            callback_data=callmsg.CALL_PRESS_MAIN_MENU)

button_change_words = InlineKeyboardButton(text=TEXT_CHANGE_WORDS, callback_data=CALL_CHANGING_WORD)
button_change_word = InlineKeyboardButton(text=TEXT_CHANGE_WORD, callback_data=CALL_CHANGING_WORD)

button_change_coll = InlineKeyboardButton(text=TEXT_CHANGE_WORD, callback_data=CALL_CHANGING_WORD)



button_change_user = InlineKeyboardButton(text=TEXT_CHANGE_USER, callback_data=CALL_CHANGING_USER)
button_change_dates = InlineKeyboardButton(text=TEXT_CHANGE_DATE, callback_data=CALL_CHANGING_DATE)
button_change_parts = InlineKeyboardButton(text=TEXT_CHANGE_PART, callback_data=CALL_CHANGING_PART)
button_change_levels = InlineKeyboardButton(text=TEXT_CHANGE_LEVEL, callback_data=CALL_CHANGING_LEVEL)

button_change_collocation = InlineKeyboardButton(text=TEXT_CHANGE_COLL, callback_data=CALL_CHANGING_COLL)
button_change_translation = InlineKeyboardButton(text=TEXT_CHANGE_TRANSLATION, callback_data=CALL_CHANGING_TRANSLATION)

button_change_media = InlineKeyboardButton(text=TEXT_CHANGE_MEDIA, callback_data=CALL_CHANGING_MEDIA)


button_change_definition = InlineKeyboardButton(text=TEXT_CHANGE_DEFINITION, callback_data=CALL_CHANGING_DEFINITION)

button_set_scheme_confirm = InlineKeyboardButton(text=TEXT_BUTTON_CONFIRM, callback_data=CALL_CONFIRM)




button_adm_menu_setting = InlineKeyboardButton(text=T_ADM_MENU_SETTING, callback_data=CALL_SETTING_MENU)
button_adm_menu_editing = InlineKeyboardButton(text=T_ADM_MENU_EDITING, callback_data=C_ADM_MENU_EDITING)
button_common_main_menu = InlineKeyboardButton(text=cmsg.COMMON_BUTTON_MAIN_MENU, callback_data=callmsg.CALL_PRESS_MAIN_MENU)
button_adm_set_scheme = InlineKeyboardButton(text=T_ADM_SET_SCHEME, callback_data=C_ADM_SET_SCHEME)
button_adm_set_coll = InlineKeyboardButton(text=T_ADM_SET_COLL, callback_data=C_ADM_SET_COLL)

button_adm_add_word = InlineKeyboardButton(text=T_ADM_ADD_WORD, callback_data=C_ADM_ADD_WORD)
button_adm_add_coll = InlineKeyboardButton(text=T_ADM_ADD_COLL, callback_data=C_ADM_ADD_COLL)

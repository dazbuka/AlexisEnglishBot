from aiogram.types import (
    InlineKeyboardButton
)
from data.admin_messages import *
from app.handlers.common_settings import *
from app.handlers.common_settings import *


button_confirm = InlineKeyboardButton(text=BTEXT_CONFIRM, callback_data=CALL_CONFIRM)
# button to go to main menu
button_main_menu = InlineKeyboardButton(text=BTEXT_MAIN_MENU, callback_data=CALL_MAIN_MENU)
button_main_menu_back = InlineKeyboardButton(text=BTEXT_MAIN_MENU_BACK, callback_data=CALL_MAIN_MENU)

# main menu
button_tasks_menu = InlineKeyboardButton(text=BTEXT_TASKS_MENU, callback_data=CALL_TASKS_MENU)
button_tasks_menu_back = InlineKeyboardButton(text=BTEXT_TASKS_MENU_BACK, callback_data=CALL_TASKS_MENU)

button_study_menu_old = InlineKeyboardButton(text=BTEXT_STUDY_MENU_OLD, callback_data=CALL_STUDY_MENU_OLD)
button_study_menu_back_old = InlineKeyboardButton(text=BTEXT_STUDY_MENU_BACK_OLD, callback_data=CALL_STUDY_MENU_OLD)

button_revision_menu = InlineKeyboardButton(text=BTEXT_REVISION_MENU, callback_data=CALL_REVISION_MENU)
button_revision_menu_back = InlineKeyboardButton(text=BTEXT_REVISION_MENU_BACK, callback_data=CALL_REVISION_MENU)

button_links_menu = InlineKeyboardButton(text=BTEXT_LINKS_MENU, callback_data=CALL_LINKS_MENU)
button_links_menu_back = InlineKeyboardButton(text=BTEXT_LINKS_MENU_BACK, callback_data=CALL_LINKS_MENU)

button_homework_menu = InlineKeyboardButton(text=BTEXT_HOMEWORK_MENU, callback_data=CALL_HOMEWORK_MENU)
button_homework_menu_back = InlineKeyboardButton(text=BTEXT_HOMEWORK_MENU_BACK, callback_data=CALL_HOMEWORK_MENU)

button_config_menu = InlineKeyboardButton(text=BTEXT_CONFIG_MENU, callback_data=CALL_CONFIG_MENU)
button_config_menu_back = InlineKeyboardButton(text=BTEXT_CONFIG_MENU_BACK, callback_data=CALL_CONFIG_MENU)

button_admin_menu = InlineKeyboardButton(text=BTEXT_ADMIN_MENU, callback_data=CALL_ADMIN_MENU)
button_admin_menu_back = InlineKeyboardButton(text=BTEXT_ADMIN_MENU, callback_data=CALL_ADMIN_MENU)


button_adding_menu = InlineKeyboardButton(text=BTEXT_ADDING_MENU, callback_data=CALL_ADDING_MENU)
button_adding_menu_back = InlineKeyboardButton(text=BTEXT_ADDING_MENU_BACK, callback_data=CALL_ADDING_MENU)

button_add_source = InlineKeyboardButton(text=BTEXT_ADD_SOURCE, callback_data=CALL_ADD_SOURCE)
button_add_word = InlineKeyboardButton(text=BTEXT_ADD_WORD, callback_data=CALL_ADD_WORD)
button_add_coll = InlineKeyboardButton(text=BTEXT_ADD_COLL, callback_data=CALL_ADD_COLL)
button_add_test = InlineKeyboardButton(text=BTEXT_ADD_TEST, callback_data=CALL_ADD_TEST)
button_add_group = InlineKeyboardButton(text=BTEXT_ADD_GROUP, callback_data=CALL_ADD_GROUP)
button_add_homework = InlineKeyboardButton(text=BTEXT_ADD_HOMEWORK, callback_data=CALL_ADD_HOMEWORK)
button_add_link = InlineKeyboardButton(text=BTEXT_ADD_LINK, callback_data=CALL_ADD_LINK)


button_setting_menu = InlineKeyboardButton(text=BTEXT_SETTING_MENU, callback_data=CALL_SETTING_MENU)
button_setting_menu_back = InlineKeyboardButton(text=BTEXT_SETTING_MENU_BACK, callback_data=CALL_SETTING_MENU)

button_set_scheme = InlineKeyboardButton(text=BTEXT_SET_SCHEME, callback_data=CALL_SET_SCHEME)
button_set_coll = InlineKeyboardButton(text=BTEXT_SET_COLL, callback_data=CALL_SET_COLL)


# changing buttons
#     inputing
button_change_source_name = InlineKeyboardButton(text=BTEXT_CHANGE_SOURCE_NAME, callback_data=CALL_CHANGING_SOURCE_NAME)
button_change_word = InlineKeyboardButton(text=BTEXT_CHANGE_WORD, callback_data=CALL_CHANGING_WORD)
button_change_group = InlineKeyboardButton(text=BTEXT_CHANGE_GROUP, callback_data=CALL_CHANGING_GROUP)
button_change_collocation = InlineKeyboardButton(text=BTEXT_CHANGE_COLL, callback_data=CALL_CHANGING_COLL)
button_change_link_name = InlineKeyboardButton(text=BTEXT_CHANGE_LINK_NAME, callback_data=CALL_CHANGING_LINK_NAME)
button_change_link_url = InlineKeyboardButton(text=BTEXT_CHANGE_LINK_URL, callback_data=CALL_CHANGING_LINK_URL)
button_change_homework = InlineKeyboardButton(text=BTEXT_CHANGE_HOMEWORK, callback_data=CALL_CHANGING_HOMEWORK)
button_change_definition = InlineKeyboardButton(text=BTEXT_CHANGE_DEFINITION, callback_data=CALL_CHANGING_DEFINITION)
button_change_translation = InlineKeyboardButton(text=BTEXT_CHANGE_TRANSLATION, callback_data=CALL_CHANGING_TRANSLATION)
button_change_media = InlineKeyboardButton(text=BTEXT_CHANGE_MEDIA, callback_data=CALL_CHANGING_MEDIA)
button_change_caption = InlineKeyboardButton(text=BTEXT_CHANGE_CAPTION, callback_data=CALL_CHANGING_CAPTION)
#     capturing

button_change_sources = InlineKeyboardButton(text=BTEXT_CHANGE_SOURCES, callback_data=CALL_CHANGING_SOURCES)
button_change_words = InlineKeyboardButton(text=BTEXT_CHANGE_WORDS, callback_data=CALL_CHANGING_WORDS)
button_change_groups = InlineKeyboardButton(text=BTEXT_CHANGE_GROUPS, callback_data=CALL_CHANGING_GROUPS)
button_change_collocations = InlineKeyboardButton(text=BTEXT_CHANGE_COLLS, callback_data=CALL_CHANGING_COLLS)
button_change_users = InlineKeyboardButton(text=BTEXT_CHANGE_USERS, callback_data=CALL_CHANGING_USERS)
button_change_colls = InlineKeyboardButton(text=BTEXT_CHANGE_COLLS, callback_data=CALL_CHANGING_COLLS)
button_change_dates = InlineKeyboardButton(text=BTEXT_CHANGE_DATES, callback_data=CALL_CHANGING_DATES)
button_change_priority = InlineKeyboardButton(text=BTEXT_CHANGE_PRIRITY, callback_data=CALL_CHANGING_PRIRITY)
button_change_days = InlineKeyboardButton(text=BTEXT_CHANGE_DAYS, callback_data=CALL_CHANGING_DAYS)
button_change_parts = InlineKeyboardButton(text=BTEXT_CHANGE_PARTS, callback_data=CALL_CHANGING_PARTS)
button_change_levels = InlineKeyboardButton(text=BTEXT_CHANGE_LEVELS, callback_data=CALL_CHANGING_LEVELS)














button_adm_menu_editing = InlineKeyboardButton(text=BTEXT_EDITING_MENU, callback_data=CALL_EDITING_MENU)





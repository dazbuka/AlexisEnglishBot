from aiogram.types import (
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
import data.admin_messages as amsg

from app.keyboards.menu_buttons import *

# inline клавиатура main
async def main_admin_menu_kb():
    inline_keyboard = [
        [button_adding_menu],
        [button_main_menu]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

# инлайн меню для заблокированного пользователя
async def admin_block_menu(user_tg_id):
    inline_keyboard = [
        [
            InlineKeyboardButton(text=amsg.ADMIN_BUTTON_UNBLOCK_USER,
                                 callback_data=f'{amsg.ADMIN_BUTTON_UNBLOCK_USER}{user_tg_id}')
        ],
        [
            InlineKeyboardButton(text=amsg.ADMIN_BUTTON_DELETE_USER,
                                 callback_data=f'{amsg.ADMIN_BUTTON_DELETE_USER}{user_tg_id}')
        ]
        ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


# inline клавиатура main adding
async def admin_adding_menu_kb():
    inline_keyboard = [[button_add_word],
                       [button_add_coll],
                       [button_add_homework],
                       [button_add_group],
                       [button_setting_menu],
                       [button_admin_menu, button_main_menu]]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)



# inline keyboard adding test
async def admin_adding_test_kb(adding_word_list : list = None,
                               adding_test_type_list : list = None,
                               adding_study_day : list = None,
                               confirmation : bool = False):
    builder = InlineKeyboardBuilder()

    if adding_word_list:
        for word in adding_word_list:
            builder.button(text=f'-{word}-', callback_data=f'{callmsg.CALL_ADM_ADD_TEST_WORD}{word[:15]}')

    if adding_test_type_list:
        for test_type in adding_test_type_list:
            builder.button(text=f'{test_type}',
                           callback_data=f'{callmsg.CALL_ADM_ADD_TEST_TYPE}{test_type}')

    if adding_study_day:
        for day in adding_study_day:
            builder.button(text=f'{day}', callback_data=f'{callmsg.CALL_ADM_ADD_TEST_DAY}{day}')

    if confirmation:
        builder.button(text=amsg.ADMIN_BUTTON_CONFIRM_DATA,
                       callback_data=callmsg.CALL_ADM_ADD_TEST_CONF + YES)
        builder.button(text=amsg.ADMIN_BUTTON_NO_CONFIRM_DATA,
                       callback_data=callmsg.CALL_ADM_ADD_TEST_CONF + NO)
        builder.button(text='in devops', callback_data='no call dev')

    builder.button(text=amsg.ADMIN_BUTTON_ADDING_MENU, callback_data=amsg.ADMIN_BUTTON_ADDING_MENU)
    builder.button(text=amsg.ADMIN_BUTTON_MAIN_ADMIN_MENU, callback_data=amsg.ADMIN_BUTTON_MAIN_ADMIN_MENU)
    builder.button(text=amsg.ADMIN_BUTTON_MAIN_MENU, callback_data=callmsg.CALL_PRESS_MAIN_MENU)
    builder.adjust(3)
    return builder.as_markup(resize_keyboard=True)




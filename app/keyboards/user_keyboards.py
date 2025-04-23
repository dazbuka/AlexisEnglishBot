from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from app.keyboards.menu_buttons import *
from app.handlers.common_settings import *
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import ADMIN_IDS

import app.database.requests as rq
import data.admin_messages as amsg
import app.handlers.callback_messages as callmsg
from app.utils.admin_utils import count_user_tasks_by_tg_id

from app.handlers.common_settings import *

# общая главная клавиатура
async def common_main_kb(user_tg_id):
    # подсчитываем задания, формируем клавиатуру
    tasks_counter = await count_user_tasks_by_tg_id(user_tg_id=user_tg_id)
    daily_count = tasks_counter['daily']
    missed_count = tasks_counter['missed']
    # создаем список кнопок для клавиатуры, используем количество неисполненных заданий
    if daily_count+missed_count != 0:
        # добавка к тексту кнопки фразу у вас х заданий
        task_message = HAVE_TASKS.format(daily_count + missed_count)
    else:
        # добавка к тексту кнопки фразы, что заданий нет
        task_message = HAVE_NO_TASKS
    # общая часть клавиатуры
    inline_keyboard = [[button_study_menu],
                       [button_revision_menu],
                       [button_homework_menu],
                       [button_config_menu]]
    # админская добавка
    inline_keyboard_admin = [
        [InlineKeyboardButton(text=amsg.ADMIN_BUTTON_MAIN_ADMIN_MENU,
                              callback_data=amsg.ADMIN_BUTTON_MAIN_ADMIN_MENU)]
    ]
    # админская добавка
    admin_menu_keyboard = [[button_admin_menu]]
    # админка, если телеграм ИД находится в списке админов
    if user_tg_id in ADMIN_IDS:
        inline_keyboard.extend(inline_keyboard_admin)
        inline_keyboard.extend(admin_menu_keyboard)
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


# инлайн меню для заблокированного пользователя
async def inline_block_menu():
    inline_keyboard = [[
            InlineKeyboardButton(text=USER_MSG_REQUEST_WHEN_BLOCKED,
                                 callback_data=USER_MSG_REQUEST_WHEN_BLOCKED)
        ]]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


# меню процесс обучения
async def inline_studing_menu(task_id: int = 1,
                              word_id: int = 1,
                              media_id: int = 0,
                              daily_tasks: int = 0,
                              missed_tasks: int = 0):
    # если аргументы слово и медиа непустые - тогда меню дополняется переводом и добавлением в таски
    if word_id != 0 and media_id != 0:
        inline_keyboard = [
            [
                InlineKeyboardButton(text=USER_BUTTON_DEFINITION,
                                     callback_data=USER_BUTTON_DEFINITION + str(word_id)),
                InlineKeyboardButton(text=USER_BUTTON_TRANSLATION,
                                     callback_data=USER_BUTTON_TRANSLATION + str(word_id))
            ],
            [
                InlineKeyboardButton(text=USER_BUTTON_REPEAT_TODAY,
                                     callback_data=USER_BUTTON_REPEAT_TODAY + str(media_id)),
                InlineKeyboardButton(text=USER_BUTTON_REPEAT_TOMORROW,
                                     callback_data=USER_BUTTON_REPEAT_TOMORROW + str(media_id))
            ]
            ]
    else:
        inline_keyboard = []
    # эта часть клавиатуры будет в любом случае
    inline_keyboard_next =    (
        [
            InlineKeyboardButton(text=USER_STUDYING_BUTTON_NEXT_DAILY_TASK + ' (' + str(daily_tasks) + ')',
                                 callback_data=USER_STUDYING_BUTTON_NEXT_DAILY_TASK + str(task_id)),
            InlineKeyboardButton(text=USER_STUDYING_BUTTON_NEXT_MISSED_TASK + ' (' + str(missed_tasks) + ')',
                                 callback_data=USER_STUDYING_BUTTON_NEXT_MISSED_TASK + str(task_id))
        ],
        [
            InlineKeyboardButton(text=BTEXT_MAIN_MENU_BACK, callback_data=callmsg.CALL_PRESS_MAIN_MENU)
        ]
    )
    # объединяем
    inline_keyboard=[*inline_keyboard, *inline_keyboard_next]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


# inline клавиатура при просмотре всех заданий ревижн
async def inline_revision_tasks_menu(previous_task_id: int = 0,
                                    next_task_id: int = 0,
                                    word_id: int = 0,
                                    media_id: int = 0):
    inline_keyboard = [
        [
            InlineKeyboardButton(text=USER_BUTTON_DEFINITION,
                                 callback_data=USER_BUTTON_DEFINITION + str(word_id)),
            InlineKeyboardButton(text=USER_BUTTON_TRANSLATION,
                                 callback_data=USER_BUTTON_TRANSLATION + str(word_id))
        ],
        [
            InlineKeyboardButton(text=USER_BUTTON_REPEAT_TODAY,
                                 callback_data=USER_BUTTON_REPEAT_TODAY + str(media_id)),
            InlineKeyboardButton(text=USER_BUTTON_REPEAT_TOMORROW,
                                 callback_data=USER_BUTTON_REPEAT_TOMORROW + str(media_id))
        ],
        [
            InlineKeyboardButton(text=USER_REVISION_BUTTON_PREVIOUS_TASK,
                                 callback_data=USER_REVISION_BUTTON_SHOW_LAST_TASKS + str(previous_task_id)),
            InlineKeyboardButton(text=USER_REVISION_BUTTON_NEXT_TASK,
                                 callback_data=USER_REVISION_BUTTON_SHOW_LAST_TASKS + str(next_task_id))
        ],
        [button_revision_menu, button_main_menu]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


# инлайн меню при ревижене
async def inline_revision_menu(next_task_id: int = 0):
    inline_keyboard = [
        [
            InlineKeyboardButton(text=USER_REVISION_BUTTON_SHOW_LAST_WORDS,
                                 callback_data=USER_REVISION_BUTTON_SHOW_LAST_WORDS)
        ],
        [
            InlineKeyboardButton(text=USER_REVISION_BUTTON_SHOW_LAST_TASKS,
                                 callback_data=USER_REVISION_BUTTON_SHOW_LAST_TASKS + str(next_task_id))
        ],
        [
            InlineKeyboardButton(text=BTEXT_MAIN_MENU_BACK, callback_data=callmsg.CALL_PRESS_MAIN_MENU)
        ]
        ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


# revision words
async def inline_revision_word_buttons_kb(word_list):
    builder = InlineKeyboardBuilder()
    for word in word_list:
        builder.button(text=f'- {word} -', callback_data=f'{callmsg.CALL_REVISION_WORD}{word}')
    builder.button(text=BTEXT_REVISION_MENU_BACK, callback_data=CALL_REVISION_MENU)
    builder.button(text=BTEXT_MAIN_MENU_BACK, callback_data=callmsg.CALL_PRESS_MAIN_MENU)
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


# revision collocation
async def inline_revision_collocations_buttons_kb(coll_list):
    builder = InlineKeyboardBuilder()
    for colloc in coll_list:
        builder.button(text=f'- {colloc[1]} -', callback_data=f'{callmsg.CALL_REVISION_COLLOCATION}{colloc[0]}')
    builder.button(text=USER_REVISION_BUTTON_WORD_LIST, callback_data=USER_REVISION_BUTTON_SHOW_LAST_WORDS)
    builder.button(text=BTEXT_MAIN_MENU_BACK, callback_data=callmsg.CALL_PRESS_MAIN_MENU)
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


# инлайн меню при ревижене
async def inline_settings_menu():
    inline_keyboard = [
        [InlineKeyboardButton(text=USER_REVISION_BUTTON_REMINDER_TIME,
                              callback_data=USER_REVISION_BUTTON_REMINDER_TIME)],
        [InlineKeyboardButton(text=BTEXT_MAIN_MENU_BACK,
                              callback_data=callmsg.CALL_PRESS_MAIN_MENU)]
        ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


# settings menu
async def inline_settings_intervals_buttons_kb(interval_list):
    builder = InlineKeyboardBuilder()
    for interval in interval_list:
        builder.button(text=f'{interval}', callback_data=f'{callmsg.CALL_SETTINGS_INTERVAL}{interval}')
    builder.button(text=BTEXT_CONFIRM, callback_data=f'{callmsg.CALL_SETTINGS_INTERVAL}{callmsg.CALL_USER_END_CHOOSING}')
    builder.button(text=BTEXT_CONFIG_MENU, callback_data=CALL_CONFIG_MENU)
    builder.button(text=BTEXT_MAIN_MENU_BACK, callback_data=callmsg.CALL_PRESS_MAIN_MENU)
    builder.adjust(3)
    return builder.as_markup(resize_keyboard=True)
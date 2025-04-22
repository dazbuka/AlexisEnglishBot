from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from app.keyboards.menu_buttons import button_confirm
from data.admin_messages import *


def update_button_with_call_base(button : InlineKeyboardButton, call_base : str):
    button_with_call_base = InlineKeyboardButton(text=button.text,
                                                 callback_data=call_base + button.callback_data)
    return button_with_call_base

# inline keyboard adding task by schema
async def keyboard_builder(menu_pack : list,
                           buttons_base_call : str | None = '',
                           buttons_add_list : list | None = None,
                           buttons_add_cols: int | None = None,
                           buttons_add_rows: int | None = None,
                           is_adding_confirm_button : bool = False,
                           buttons_add_table_number: int | None = 0):

    # билдер и массив аджастинга для начала пустой
    builder = InlineKeyboardBuilder()
    adjusting = []
    # если есть параметр добавления в меню списка слов - добавление соответствующих кнопок
    if buttons_add_list:
        tables = []
        tables_of_items = []
        while buttons_add_list:
            table = []
            table_if_items = []
            row = 0
            while row < buttons_add_rows and buttons_add_list:
                line = 0
                while line < buttons_add_cols and buttons_add_list:
                    line += 1
                    table_if_items.append(buttons_add_list[0])
                    buttons_add_list = buttons_add_list[1:]
                table.append(line)
                row += 1
            tables.append(table)
            tables_of_items.append(table_if_items)

        for item in tables_of_items[buttons_add_table_number]:
            # ограничение длины колбека - 64, ,возьмем 15 - точно хватит для цифр и начала букв
            builder.button(text=f'{item}', callback_data=f'{buttons_base_call}{item[:15]}')

        if len(tables)>1:
            tables[buttons_add_table_number].append(4)
            builder.button(text=TEXT_FIRST, callback_data=f'{buttons_base_call}{CALL_FIRST}{buttons_add_table_number}')
            builder.button(text=TEXT_PREV, callback_data=f'{buttons_base_call}{CALL_PREV}{buttons_add_table_number}')
            builder.button(text=TEXT_NEXT, callback_data=f'{buttons_base_call}{CALL_NEXT}{buttons_add_table_number}')
            builder.button(text=TEXT_LAST, callback_data=f'{buttons_base_call}{CALL_LAST}{buttons_add_table_number}')
        adjusting.extend(tables[buttons_add_table_number])

    # если нужно добавить кнопку подтверждения ввода
    if is_adding_confirm_button:
        but = update_button_with_call_base(button_confirm, buttons_base_call)
        builder.add(but)
        adjusting.append(1)

    # добавляем меню
    for menu_line in menu_pack:
        for menu_item in menu_line:
            builder.add(menu_item)
        adjusting.append(len(menu_line))
    # распределяем меню
    builder.adjust(*adjusting)
    return builder.as_markup()

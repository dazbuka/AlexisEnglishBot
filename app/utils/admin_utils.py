from aiogram.types import InlineKeyboardButton
from aiogram import Bot
import app.database.requests as rq
from app.database.models import UserStatus
from data.admin_messages import *
from config import logger

from aiogram.types import Message, CallbackQuery
import re
from datetime import datetime, date, timedelta


def logger_decorator(func):
    async def wrapper(*args, **kwargs):
        result = await func(*args, **kwargs)
        # print(f"________________________________________________________________________________________________")
        return result
    return wrapper


@logger_decorator
async def message_answer(source: Message | CallbackQuery, message_text, *args, **kwargs):
    if isinstance(source, CallbackQuery):
        bot_mess_num = (await source.message.answer(message_text, *args, **kwargs)).message_id
    elif isinstance(source, Message):
        bot_mess_num = (await source.answer(message_text, *args, **kwargs)).message_id
    else:
        logger.info(f'function *message_answer* have no source{source}')
        bot_mess_num = 1

    await rq.update_user_last_message_id(user_tg_id=source.from_user.id, message_id=bot_mess_num)
    return bot_mess_num


# функция отправки медиа пользователю, ответ на колл
@logger_decorator
async def send_any_media_to_user_with_kb(bot : Bot, user_tg_id, media_type, caption = None, file_id = None, reply_kb = None):
    match media_type:
        case 'text':
            mess_id = await bot.send_message(chat_id=user_tg_id,
                                             text=caption,
                                             reply_markup=reply_kb)
        case 'photo':
            mess_id = await bot.send_photo(chat_id=user_tg_id,
                                           photo=file_id,
                                           caption=caption,
                                           reply_markup=reply_kb)
        case 'video':
            mess_id = await bot.send_video(chat_id=user_tg_id,
                                           video=file_id,
                                           caption=caption,
                                           reply_markup=reply_kb)
        case _:
            mess_id = await bot.send_message(chat_id=user_tg_id,
                                             text='Возникли проблемы с отправкой сообщения',
                                             reply_markup=reply_kb)

    # last = await rq.get_user_last_message_id(user_tg_id)
    # logger.info(f'admin utils last {last} - {caption}')
    # try:
    #     await bot.delete_message(chat_id=user_tg_id, message_id=last)
    #     logger.info(f'admin utils удалил {last} - {caption}')
    # except TelegramBadRequest as e:
    #     logger.error(f'ошибка удаления {e}')

    logger.info(f'now  {mess_id.message_id}')
    await rq.update_user_last_message_id(user_tg_id=user_tg_id, message_id=mess_id.message_id)
    return mess_id


async def count_user_tasks_by_tg_id(user_tg_id):
    all_tasks = await rq.get_tasks_by_filters(user_tg_id=user_tg_id, sent=True, media_task_only=True)
    # последнее отправленное номер ид
    last_send_task_num = all_tasks[-1].id if all_tasks else None
    # все задачи вне зависимости от выполнения
    all_tasks = await rq.get_tasks_by_filters(user_tg_id=user_tg_id)
    last_task_num = all_tasks[-1].id if all_tasks else None
    # все задачи
    all_tasks_count = len(all_tasks) if all_tasks else 0
    # сегодняшние задачи
    today_tasks = await rq.get_tasks_by_filters(user_tg_id=user_tg_id, sent=False, daily_tasks_only=True)
    today_tasks_count = len(today_tasks) if today_tasks else 0
    # пропущенные задачи
    missed_tasks = await rq.get_tasks_by_filters(user_tg_id=user_tg_id, sent=False, missed_tasks_only=True)
    missed_tasks_count = len(missed_tasks) if missed_tasks else 0
    # будущие задачи
    future_tasks = await rq.get_tasks_by_filters(user_tg_id=user_tg_id, sent=False, future_tasks_only=True)
    future_tasks_count = len(future_tasks) if future_tasks else 0

    # создаем дикт
    count_tasks = {
        'all' : all_tasks_count,
        'daily': today_tasks_count,
        'missed': missed_tasks_count,
        'future': future_tasks_count,
        'last' : last_task_num,
        'last_sent': last_send_task_num
    }
    # возвращаем дикт
    return count_tasks


async def get_text_from_word_adding_state(state):
    st_data = await state.get_data()

    word = st_data.get("word")
    word_text = f'Введено слово: {word}\n' if word else ''

    author = st_data.get("author")
    author_text = f'ID aвторa: {author}\n' if author else ''

    level = st_data.get("level")
    level_text = f'Уровень: {level}\n' if level else ''

    part = st_data.get("part")
    part_text = f'Часть речи: {part}\n' if part else ''

    definition = st_data.get("definition")
    definition_text  = f'Определение: {definition}\n' if definition else ''

    translation = st_data.get("translation")
    translation_text = f'Перевод: {translation}\n' if translation else ''

    message_text = (word_text + author_text + level_text +
                    part_text + definition_text + translation_text)

    return message_text


async def get_text_from_media_adding_state(state):
    st_data = await state.get_data()

    word = st_data.get("word")
    word_text = f'Выбрано слово: {word}\n' if word else ''

    word_id = st_data.get("word_id")
    word_id_text = f'ID выбранного слова: {word_id}\n' if word_id else ''

    author = st_data.get("author")
    author_text = f'ID aвторa: {author}\n' if author else ''

    collocation = st_data.get("collocation")
    collocation_text = f'Коллокация: {collocation}\n' if collocation else ''

    level = st_data.get("level")
    level_text = f'Уровень: {level}\n' if level else ''

    media_type = st_data.get("media_type")
    media_type_text = f'Тип медиа: {media_type}\n' if media_type else ''

    caption = st_data.get("caption")
    caption_text = f'Текст или подпись в видео(фото): {caption}\n' if caption else ''

    tg_id = st_data.get("telegram_id")
    tg_id_text = f'Номер в телеграм: {tg_id}\n' if tg_id else ''

    study_day = st_data.get("study_day")
    study_day_text = f'День изучения: {study_day}\n' if study_day else ''

    message_text = (word_text + word_id_text + author_text +
                    collocation_text + level_text + media_type_text +
                    caption_text + tg_id_text + study_day_text)
    return message_text


async def get_text_from_test_adding_state(state):

    st_data = await state.get_data()

    word = st_data.get("word")
    word_text = f'Выбрано слово: {word}\n' if word else ''

    word_id = st_data.get("word_id")
    word_id_text = f'ID выбранного слова: {word_id}\n' if word_id else ''

    author = st_data.get("author")
    author_text = f'ID aвторa: {author}\n' if author else ''

    media_type = st_data.get("media_type")
    media_type_text = f'Тип теста: {media_type}\n' if media_type else ''

    collocation = st_data.get("collocation")
    collocation_text = f'Задание теста: {collocation}\n' if collocation else ''

    caption = st_data.get("caption")
    caption_text = f'Текст или подпись в видео(фото): {caption}\n' if caption else ''

    tg_id = st_data.get("telegram_id")
    tg_id_text = f'Номер в телеграм: {tg_id}\n' if tg_id else ''

    study_day = st_data.get("study_day")
    study_day_text = f'День изучения: {study_day}\n' if study_day else ''

    message_text = (word_text + word_id_text + author_text + media_type_text +
                    collocation_text + caption_text + tg_id_text + study_day_text)

    return message_text

# стейт текст билдер
async def state_text_builder(state):
    # получаем данные, хранящиеся в стейте
    st_data = await state.get_data()
    # конечное сообщение - пустое
    message_text = ''
    if 'author_id' in st_data:
        author_id = st_data.get('author_id')
        author = await rq.get_users_by_filters(user_id=author_id)
        text = author.ident_name
        if text:
            message_text += f'Автор:\n<b>{text}</b>\n'
    if 'input_word_state' in st_data:
        word = (st_data.get("input_word_state")).input_item
        # word_list = []
        # for word_id in words:
        #     word = (await rq.get_words_by_filters(id=word_id)).word
        #     word_list.append(word)
        # text = ', '.join(word_list)
        text = word
        if text:
            message_text += f'Выбраны слова:\n<b>{text}</b>\n'
    if 'capture_words_state' in st_data:
        words=(st_data.get("capture_words_state")).captured_items_set
        word_list = []
        for word_id in words:
            word = (await rq.get_words_by_filters(id=word_id)).word
            word_list.append(word)
        text = ', '.join(word_list)
        if text:
            message_text += f'Выбраны слова:\n<b>{text}</b>\n'
    if 'capture_groups_state' in st_data:
        groups = (st_data.get("capture_groups_state")).captured_items_set
        group_list = []
        for group_id in groups:
            group = (await rq.get_groups_by_filters(group_id=group_id)).name
            group_list.append(group)
        text = ', '.join(group_list)
        if text:
            message_text += f'Выбраны группы:\n<b>{text}</b>\n'
    if 'capture_users_state' in st_data:
        users=(st_data.get("capture_users_state")).captured_items_set
        user_list = []
        for user_id in users:
            user = (await rq.get_users_by_filters(user_id=user_id)).ident_name
            user_list.append(user)
        text = ', '.join(user_list)
        if text:
            message_text += f'Выбраны пользователи:\n<b>{text}</b>\n'
    if 'capture_dates_state' in st_data:
        dates=(st_data.get("capture_dates_state")).captured_items_set
        date_list = []
        for date_values in dates:
            date_list.append(date_values)
        text = ', '.join(date_list)
        if text:
            message_text += f'Выбраны даты:\n<b>{text}</b>\n'
    return message_text

# получает номер страницы пагинации при управлении в карусельке вперед назад
async def get_new_carousel_page_num(call: str, items_kb: list, rows: int, cols: int):
    # считаем количество таблиц исходя из длины массива кнопок и количества строк и столбцов
    count_of_tables = ((len(items_kb) - 1) // (cols * rows)) + 1
    # меняем пагинацию в зависимости от нажатой кнопки
    # если нажата НЕКСТ - вытаскиваем из колла номер текущей страницы, добавляем 1, если последний - идем на первую
    if call.startswith(CALL_NEXT):
        page_num = int(call.replace(CALL_NEXT, ''))
        page_num = 0 if page_num == count_of_tables - 1 else page_num + 1
    # если нажата ПРЕД - вытаскиваем из колла номер текущей страницы, вычитаем 1, если первая - идем на последнюю
    elif call.startswith(CALL_PREV):
        page_num = int(call.replace(CALL_PREV, ''))
        page_num = count_of_tables - 1 if page_num == 0 else page_num - 1
    # если нажата последняя - идет туда
    elif call.startswith(CALL_LAST):
        page_num = count_of_tables - 1
    # если нажата первая - идем туда
    else:
        page_num = 0
    return page_num


# получает номер страницы пагинации при выбере слова, чтобы остаться на той же странице
async def get_current_carousel_page_num(item: str, items_kb: list, rows: int, cols: int):
    # вычисляем страницу выбранного слова, чтобы остаться на ней
    page_num = 0
    if items_kb:
        for i in range(len(items_kb)):
            if item in items_kb[i]:
                page_num = i // (rows * cols)
    return page_num


async def get_text_from_task_adding_state(state):

    st_data = await state.get_data()

    author = st_data.get("author")
    author_text = f'ID aвторa: {author}\n' if author else ''

    words = '\n'.join(map(str, st_data.get("words_set"))) if st_data.get("words_set") else None
    words_text = f'Выбраны слова:\n {words} \n' if words else ''

    medias = '\n'.join(map(str, st_data.get("medias_kb"))) if st_data.get("medias_kb") else None
    medias_text = f'Выбраны коллокации:\n {medias} \n' if medias else ''

    users = '\n'.join(map(str, st_data.get("users_kb"))) if st_data.get("users_kb") else None
    users_text = f'Выбраны пользователи:\n {users}\n' if users else ''

    beginning_date = st_data.get("beginning_date")
    beginning_date_text = f'Дата начала: {beginning_date}\n' if beginning_date else ''

    message_text = (author_text + words_text + medias_text + users_text + beginning_date_text)

    return message_text

async def get_text_from_homework_adding_state(state):

    st_data = await state.get_data()

    author = st_data.get("author")
    author_text = f'ID aвторa: {author}\n' if author else ''

    hometask = st_data.get("hometask")
    hometask_text = f'Домашнее задание: {hometask}\n' if hometask else ''

    users = '\n'.join(map(str, st_data.get("users_kb"))) if st_data.get("users_kb") else None
    users_text = f'Выбраны пользователи:\n {users}\n' if users else ''

    date = st_data.get("date")
    date_text = f'Дата выполнения: {date}\n' if date else ''

    message_text = (author_text + hometask_text + users_text + date_text)

    return message_text


async def get_text_from_group_adding_state(state):

    st_data = await state.get_data()

    name = st_data.get("name")
    name_text = f'Группа: {name}\n' if name else ''

    level = st_data.get("level")
    level_text = f'Уровень: {level}\n' if level else ''

    users = '\n'.join(map(str, st_data.get("users_kb"))) if st_data.get("users_kb") else None
    users_text = f'Пользователи в группе:\n {users}\n' if users else ''

    message_text = (name_text + users_text + level_text)
    return message_text


async def get_words_list_for_kb_with_limit(words = None, limit: int = 21):
    if not words:
        words = await rq.get_words_by_filters(limit=limit)
    word_list = []
    for word in words:
        word_list.append(word)
    return word_list

async def get_word_list_for_kb_with_ids_limited(words = None, limit: int = 21):
    if not words:
        words = await rq.get_words_by_filters(limit=limit)
    word_list = []
    for word in words:
        word_list.append(f'{word.id}-{word.word}')
    return word_list

# new
async def get_word_list_for_kb_with_ids() -> list:
    words = await rq.get_words_by_filters()
    word_list = []
    for word in words:
        word_list.append(f'{word.id}-{word.word}')
    return word_list

# new
async def get_group_list_for_kb_with_ids():
    groups = await rq.get_groups_by_filters()
    group_list = []
    for group in groups:
        group_list.append(f'{group.id}-{group.name}({group.users})')
    return group_list

# new
async def get_user_list_for_kb_with_ids():
    users = await rq.get_users_by_filters()
    user_list = []
    for user in users:
        user_list.append(f'{user.id}-{user.ident_name}')
    return user_list

# new
async def get_date_list_for_kb():
    date_list = []
    # 150 дней выводим в список
    for i in range(150):
        date_item = (date.today() + timedelta(days=i)).strftime("%d.%m.%Y")
        date_list.append(date_item)
    return date_list

async def get_medias_list_for_kb_with_limit(medias = None, limit: int = 20, offset: int = 0, media_only: bool = True):
    if not medias:
        medias = await rq.get_medias_by_filters(limit=limit, offset=offset, media_only=media_only)
    media_list = []
    for media in medias:
        media_list.append(f'{media.id}-{media.collocation}')
    return media_list


def update_button_with_call_base(button : InlineKeyboardButton, call_base : str):
    button_with_call_base = InlineKeyboardButton(text=button.text, callback_data=call_base + button.callback_data)
    return button_with_call_base


async def get_users_list_for_kb_with_limit(users = None, limit: int = 21):
    if not users:
        users = await rq.get_users_by_filters(limit=limit, status=UserStatus.ACTIVE)
    user_list = []
    for user in users:
        user_list.append(f'{user.id}-{user.username}({user.first_name})')
    return user_list


async def get_data_list_for_kb_with_limit(users = None, limit: int = 21):
    if not users:
        users = await rq.get_users_by_filters(limit=limit, status=UserStatus.ACTIVE)
    user_list = []
    for user in users:
        user_list.append(f'{user.id}-{user.username}({user.first_name})')
    return user_list


async def get_groups_list_for_kb_with_limit(groups = None, limit: int = 21):
    if not groups:
        groups = await rq.get_groups_by_filters(limit=limit)
    group_list = []
    for group in groups:
        group_list.append(f'Group:{group.id}-{group.name}({group.users})')
    return group_list


async def get_shema_text_by_word_id(word_id):
    media_list = await rq.get_medias_by_filters(word_id=word_id)
    medias_in_schema = []
    if media_list:
        for media in media_list:
            medias_in_schema.append(f'{media.study_day} - {media.collocation}')
    medias_in_schema.sort()
    shema = '\n'.join(map(str, medias_in_schema))
    return shema




async def get_reminder_all_day_intervals() -> list:
    reminder_24_intervals = []
    for i in range(0,24):
        start = i
        end = i+1 if i!=23 else 0
        reminder_24_intervals.append(f'{str(start).zfill(2)}:00-{str(end).zfill(2)}:00')
    return reminder_24_intervals


async def get_interval_list_for_kb(reminder_intervals: str, check: str = '🟣') -> list:
    all_intervals = await get_reminder_all_day_intervals()
    if reminder_intervals:
        interval_list = reminder_intervals.replace(' ', '').split(',')
        for i in range(len(all_intervals)):
            if all_intervals[i] in interval_list:
                all_intervals[i] = check + all_intervals[i] + check
    return all_intervals


# 030425 функция добавления в множество нажатых с кнопок значений
async def add_item_in_aim_set_plus_minus(aim_set: set, added_item: int | str) -> set:
    # если число (как правило номер ид слова юзера и др)
    if isinstance(added_item, int):
        aim_set.symmetric_difference_update({added_item})
        # aim_set.add(added_item)
    if isinstance(added_item, str):
        number_list = added_item.split(',')
        if number_list[0].isdigit():
            number_set = {int(num.strip()) for num in number_list if num.isdigit()}
        else:
            number_set = {num.strip() for num in number_list}
        aim_set.symmetric_difference_update(number_set)
        # aim_set = aim_set | number_set
    return aim_set

async def add_item_in_only_one_aim_set(aim_set: set, added_item: int | str) -> set:
    # если число (как правило номер ид слова юзера и др)
    if isinstance(added_item, int):
        aim_set = {added_item}
        print('внимание, ниже работает копи, участок памяти не меняется, здесь нет')
        # aim_set.add(added_item)
    if isinstance(added_item, str):
        number_list = added_item.split(',')
        if number_list[0].isdigit():
            number_set = {int(num.strip()) for num in number_list if num.isdigit()}
        else:
            number_set = {num.strip() for num in number_list}
        aim_set = number_set.copy()
        # aim_set = aim_set | number_set
    return aim_set


# 030425 функция добавления в множество нажатых с кнопок значений
async def add_item_in_aim_set_plus_plus(aim_set: set, added_item: int | str) -> set:
    # если число (как правило номер ид слова юзера и др)
    if isinstance(added_item, int):
        aim_set.add({added_item})
    if isinstance(added_item, str):
        number_list = added_item.split(',')
        number_set = {int(num.strip()) for num in number_list if num.isdigit()}
        aim_set = aim_set | number_set
    return aim_set


# 030425 функция установки чеков в список кнопок
async def set_check_in_button_list(button_list: list | None, aim_set : set | None, check: str = '🟣') -> list:
    # проверяем передан ли нам баттон лист и множество
    if button_list:
        new_button_list = button_list.copy()
        if not aim_set:
            pass
        elif isinstance((list(aim_set))[0],int):
            button_list_clear = [int(x.split('-', 1)[0]) for x in button_list]
            for i in range(len(button_list)):
                if button_list_clear[i] in aim_set:
                    new_button_list[i] = check + new_button_list[i] + check
        elif isinstance((list(aim_set))[0],str):
            for i in range(len(button_list)):
                if button_list[i] in aim_set:
                    new_button_list[i] = check + new_button_list[i] + check
        else:
            pass
    else:
        new_button_list = None
    return new_button_list


async def get_list_from_check_list(check_list: str, check: str = '🟣') -> list:
    new_list = []
    for i in range(len(check_list)):
        if check_list[i][0] == check:
            new_list.append(check_list[i][1:-1])
    return new_list


async def set_check_in_list(checked_list: list, checked_items: list = None, checked_item: str = None, check ='🟣'):
    if checked_items:
        for i in range(len(checked_list)):
            for item in checked_items:
                if item in checked_list[i]:
                    if check not in checked_list[i]:
                        checked_list[i] = check + checked_list[i] + check
                    else:
                        checked_list[i] = checked_list[i][1:-1]

    if checked_item:
        for i in range(len(checked_list)):
            if checked_item in checked_list[i]:
                if check not in checked_list[i]:
                    checked_list[i] = check + checked_list[i] + check
                else:
                    checked_list[i] = checked_list[i][1:-1]

    return checked_list


async def set_check_in_id_list_for_kb(checked_list_starts_with_id: list, checked_items: list = None, check ='🟣'):
    print(checked_list_starts_with_id)
    print(checked_items)
    new_list_item = []
    for i in range(len(checked_list_starts_with_id)):
        for checked_item in checked_items:
            if checked_item == int(checked_list_starts_with_id[i].split('-', 1)[0]):
                new_list_item.append(check + checked_list_starts_with_id[i] + check)
            else:
                new_list_item.append(checked_list_starts_with_id[i])
    print(new_list_item)
    return new_list_item


async def check_now_time_in_reminder_intervals(reminder_intervals: str) -> bool:
    rezult = False
    now_time = datetime.now().time()
    if reminder_intervals:
        interval_list = reminder_intervals.replace(' ', '').split(',')
        for interval in interval_list:
            pattern = r'^([01]?[0-9]|2[0-3]):[0-5][0-9]-([01]?[0-9]|2[0-3]):[0-5][0-9]$'
            if re.match(pattern, interval):
                start = datetime.strptime(interval.split('-')[0], "%H:%M").time()
                end = datetime.strptime(interval.split('-')[1], "%H:%M").time()
                rezult = rezult or (start < now_time < end)
    return bool(rezult)
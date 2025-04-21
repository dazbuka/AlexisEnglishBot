import os
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from datetime import datetime

from app.keyboards.menu_buttons import *
from app.handlers.common_settings import *

from app.database.requests import get_users_by_filters, add_media_to_db, get_medias_by_filters
from app.utils.admin_utils import (state_text_builder, mess_answer,
                                   get_word_list_for_kb_with_ids,
                                   send_any_media_to_user_with_kb,
                                   get_day_list_for_kb,
                                   get_shema_text_by_word_id)

import app.keyboards.admin_keyboards as akb
from config import bot, media_dir

from app.handlers.admin_menu.states.input_states import (StateParams, FSMExecutor, CaptureLevelsStateParams,
                                                         CaptureDaysStateParams, CaptureWordsStateParams)

from app.keyboards.keyboard_builder import keyboard_builder, update_button_with_call_base


adding_coll_router = Router()

class AddColl(StatesGroup):
    author_id = State()
    capture_words_state = State()
    input_coll_state = State()
    input_media_state = State()
    input_caption_state = State()
    capture_levels_state = State()
    capture_days_state = State()
    confirmation_state = State()


menu_add_coll = [
    [button_menu_adding_back, button_new_admin_menu, button_new_main_menu]
]

menu_add_coll_with_changing = [
    [update_button_with_call_base(button_change_words, CALL_ADD_COLL + CALL_ADD_ENDING),
     update_button_with_call_base(button_change_collocation, CALL_ADD_COLL + CALL_ADD_ENDING),
     update_button_with_call_base(button_change_levels, CALL_ADD_COLL + CALL_ADD_ENDING)],
    [update_button_with_call_base(button_change_media, CALL_ADD_COLL + CALL_ADD_ENDING),
     update_button_with_call_base(button_change_caption, CALL_ADD_COLL + CALL_ADD_ENDING),
     update_button_with_call_base(button_change_days, CALL_ADD_COLL + CALL_ADD_ENDING)],
    [button_menu_setting_back, button_new_admin_menu, button_new_main_menu]
]

# переход в меню добавления задания по схеме
@adding_coll_router.callback_query(F.data == C_ADM_ADD_COLL)
async def adding_word_first_state(call: CallbackQuery, state: FSMContext):
    # очистка стейта
    await state.clear()



    # задаем в стейт ид автора
    author = await get_users_by_filters(user_tg_id=call.from_user.id)
    await state.update_data(author_id=author.id)

    words_state = CaptureWordsStateParams(self_state=AddColl.capture_words_state,
                                          next_state=AddColl.input_coll_state,
                                          call_base=CALL_ADD_COLL,
                                          menu_add=menu_add_coll,
                                          items_kb_list=(await get_word_list_for_kb_with_ids())[::-1],
                                          is_only_one=True)
    await state.update_data(capture_words_state=words_state)


    input_coll_text_state = StateParams(self_state = AddColl.input_coll_state,
                                        next_state = AddColl.input_media_state,
                                        call_base= CALL_ADD_COLL,
                                        call_add_capture= CALL_INPUT_COLL,
                                        state_main_mess = MESS_INPUT_COLL,
                                        but_change_text = TEXT_CHANGE_COLL,
                                        menu_add = menu_add_coll,
                                        is_input=True)
    await state.update_data(input_coll_state=input_coll_text_state)


    input_media_state = StateParams(self_state=AddColl.input_media_state,
                                       next_state=AddColl.capture_levels_state,
                                       call_base=CALL_ADD_COLL,
                                       call_add_capture=CALL_INPUT_MEDIA,
                                       state_main_mess=MESS_INPUT_MEDIA,
                                       but_change_text=TEXT_CHANGE_MEDIA,
                                       menu_add=menu_add_coll,
                                       is_input=True)
    await state.update_data(input_media_state=input_media_state)

    input_caption_text_state = StateParams(self_state=AddColl.input_caption_state,
                                           next_state=AddColl.confirmation_state,
                                           call_base=CALL_ADD_COLL,
                                           call_add_capture=CALL_INPUT_CAPTION,
                                           state_main_mess=MESS_INPUT_CAPTION,
                                           but_change_text=TEXT_CHANGE_CAPTION,
                                           menu_add=menu_add_coll,
                                           is_input=True)
    await state.update_data(input_caption_state=input_caption_text_state)


    levels_state = CaptureLevelsStateParams(self_state=AddColl.capture_levels_state,
                                            next_state=AddColl.capture_days_state,
                                            call_base=CALL_ADD_COLL,
                                            menu_add=menu_add_coll,
                                            items_kb_list=LEVEL_LIST,
                                            is_can_be_empty=True,
                                            is_only_one=True)
    await state.update_data(capture_levels_state=levels_state)

    days_state = CaptureDaysStateParams(self_state=AddColl.capture_days_state,
                                          next_state=AddColl.confirmation_state,
                                          call_base=CALL_ADD_COLL,
                                          menu_add=menu_add_coll,
                                          items_kb_list=await get_day_list_for_kb(),
                                          is_only_one=True)

    await state.update_data(capture_days_state=days_state)



    confirmation_state = StateParams(self_state = AddColl.confirmation_state,
                                     call_base = CALL_ADD_COLL,
                                     call_add_capture= CALL_ADD_ENDING,
                                     menu_add = menu_add_coll_with_changing,
                                     state_main_mess=MESS_ADD_ENDING,
                                     is_last_state_with_changing_mode=True)
    await state.update_data(confirmation_state=confirmation_state)


    first_state = words_state

    # переход в первый стейт
    await state.set_state(first_state.self_state)

    # формируем сообщение, меню, клавиатуру и выводим их

    reply_kb = await keyboard_builder(menu_pack=first_state.menu_add,
                                      buttons_add_list= first_state.items_kb_list,
                                      buttons_base_call=first_state.call_base + first_state.call_add_capture,
                                      buttons_add_cols=first_state.items_kb_cols,
                                      buttons_add_rows=first_state.items_kb_rows,
                                      is_adding_confirm_button=False)

    await call.message.edit_text(text=first_state.state_main_mess, reply_markup=reply_kb)

    await call.answer()

@adding_coll_router.message(F.text, AddColl.capture_words_state)
@adding_coll_router.message(F.text, AddColl.input_coll_state)
@adding_coll_router.message(F.photo | F.video | F.text, AddColl.input_media_state)
@adding_coll_router.message(F.text, AddColl.input_caption_state)
@adding_coll_router.message(F.text, AddColl.capture_levels_state)
@adding_coll_router.message(F.text, AddColl.capture_days_state)
async def admin_adding_word_capture_word(message: Message, state: FSMContext):

    # взимообмен кэпшен стейт и медиа стейт, в котором есть переменная кэпшн
    media_state: StateParams = await state.get_value('input_media_state')


    # проверяем слово в базе данных
    # создаем экземпляр класса для обработки текущего состояния фсм
    current_fsm = FSMExecutor()
    # обрабатываем экземпляра класса, который анализирует наш колл и выдает сообщение и клавиатуру
    await current_fsm.execute(fsm_state=state, fsm_mess=message)



    await mess_answer(source=message,
                      media_type=media_state.media_type,
                      media_id=media_state.media_id,
                      message_text=current_fsm.message_text,
                      reply_markup=current_fsm.reply_kb)

    fsm_state_str = await state.get_state()

    if fsm_state_str == AddColl.input_media_state.state:
        caption = media_state.input_text
        input_caption_state: StateParams = await state.get_value('input_caption_state')
        input_caption_state.input_text = caption
        await state.update_data(input_caption_state=input_caption_state)




@adding_coll_router.callback_query(F.data.startswith(CALL_ADD_COLL + CALL_CAPTURE_WORD), AddColl.capture_words_state)
@adding_coll_router.callback_query(F.data.startswith(CALL_ADD_COLL + CALL_CAPTURE_LEVEL), AddColl.capture_levels_state)
@adding_coll_router.callback_query(F.data.startswith(CALL_ADD_COLL + CALL_CAPTURE_DAY), AddColl.capture_days_state)
async def set_scheme_capture_words_from_call(call: CallbackQuery, state: FSMContext):

    # создаем экземпляр класса для обработки текущего состояния фсм
    current_fsm = FSMExecutor()
    # обрабатываем экземпляра класса, который анализирует наш колл и выдает сообщение и клавиатуру
    await current_fsm.execute(fsm_state=state, fsm_call=call)
    # отвечаем заменой сообщения





    fsm_state_str = await state.get_state()

    media_state: StateParams = await state.get_value('input_media_state')

    if fsm_state_str == AddColl.capture_days_state.state:
        word_state: StateParams = await state.get_value('capture_words_state')
        word_id = list(word_state.captured_items_set)[0]
        scheme = await get_shema_text_by_word_id(word_id=word_id)
        await mess_answer(source=call,
                          media_type=media_state.media_type,
                          media_id=media_state.media_id,
                          message_text=current_fsm.message_text + '\n\n' + scheme,
                          reply_markup=current_fsm.reply_kb)
    else:
        await mess_answer(source=call,
                          media_type=media_state.media_type,
                          media_id=media_state.media_id,
                          message_text=current_fsm.message_text,
                          reply_markup=current_fsm.reply_kb)

            # await message_answer(source=call, message_text=current_fsm.message_text, reply_markup=current_fsm.reply_kb)
    await call.answer()

    input_media: StateParams = await state.get_value('input_media_state')
    media_caption = input_media.input_text
    print(f'--------------------before adding media capt - {media_caption}')

    input_caption: StateParams = await state.get_value('input_caption_state')
    caption = input_caption.input_text
    print(f'--------------------before adding capt - {caption}')

# конечный обработчик всего стейта
@adding_coll_router.callback_query(F.data.startswith(CALL_ADD_COLL + CALL_ADD_ENDING), AddColl.confirmation_state)
async def admin_adding_task_capture_confirmation_from_call(call: CallbackQuery, state: FSMContext):
    # вытаскиваем из колбека уровень
    confirm = call.data.replace(CALL_ADD_COLL + CALL_ADD_ENDING, '')
    # уходим обратно если нужно что-то изменить



    if (confirm == CALL_CHANGING_WORD or confirm == CALL_CHANGING_COLL or confirm == CALL_CHANGING_LEVEL
            or confirm == CALL_CHANGING_CAPTION or confirm == CALL_CHANGING_MEDIA or confirm == CALL_CHANGING_DAY):

        confirmation_state: StateParams = await state.get_value('confirmation_state')

        if confirm == CALL_CHANGING_WORD:
            # при нажатии на изменение задаем следующий стейт элементов
            confirmation_state.next_state = AddColl.capture_words_state
            # делаем так, чтобы в стейте добавления последний стейт (на изменения который) стал следующим
            capture_words_state: StateParams = await state.get_value('capture_words_state')
            capture_words_state.next_state = AddColl.confirmation_state
            await state.update_data(capture_words_state=capture_words_state)

        elif confirm == CALL_CHANGING_COLL:
            # при нажатии на изменение задаем следующий стейт элементов
            confirmation_state.next_state = AddColl.input_coll_state
            # делаем так, чтобы в стейте добавления последний стейт (на изменения который) стал следующим
            input_coll_state: StateParams = await state.get_value('input_coll_state')
            input_coll_state.next_state = AddColl.confirmation_state
            await state.update_data(input_coll_state=input_coll_state)

        elif confirm == CALL_CHANGING_LEVEL:
            # при нажатии на изменение задаем следующий стейт элементов
            confirmation_state.next_state = AddColl.capture_levels_state
            # делаем так, чтобы в стейте добавления последний стейт (на изменения который) стал следующим
            capture_levels_state: StateParams = await state.get_value('capture_levels_state')
            capture_levels_state.next_state = AddColl.confirmation_state
            await state.update_data(capture_levels_state=capture_levels_state)

        elif confirm == CALL_CHANGING_MEDIA:
            # при нажатии на изменение задаем следующий стейт элементов
            confirmation_state.next_state = AddColl.input_media_state
            # делаем так, чтобы в стейте добавления последний стейт (на изменения который) стал следующим
            input_media_state: StateParams = await state.get_value('input_media_state')
            input_media_state.next_state = AddColl.confirmation_state
            await state.update_data(input_media_state=input_media_state)

        elif confirm == CALL_CHANGING_CAPTION:
            # при нажатии на изменение задаем следующий стейт элементов
            confirmation_state.next_state = AddColl.input_caption_state
            # делаем так, чтобы в стейте добавления последний стейт (на изменения который) стал следующим
            input_caption_state: StateParams = await state.get_value('input_caption_state')
            input_caption_state.next_state = AddColl.confirmation_state
            await state.update_data(input_caption_state=input_caption_state)

        elif confirm == CALL_CHANGING_DAY:
            # при нажатии на изменение задаем следующий стейт элементов
            confirmation_state.next_state = AddColl.capture_days_state
            # делаем так, чтобы в стейте добавления последний стейт (на изменения который) стал следующим
            capture_days_state: StateParams = await state.get_value('capture_days_state')
            capture_days_state.next_state = AddColl.confirmation_state
            await state.update_data(capture_days_state=capture_days_state)

        await state.update_data(confirmation_state=confirmation_state)
        current_fsm = FSMExecutor()
        await current_fsm.execute(state, call)

        media_state: StateParams = await state.get_value('input_media_state')

        await mess_answer(source=call,
                          media_type=media_state.media_type,
                          media_id=media_state.media_id,
                          message_text=current_fsm.message_text,
                          reply_markup=current_fsm.reply_kb)
        await call.answer()


    elif confirm == CALL_CONFIRM:

        # основной обработчик, запись в бд
        author_id = await state.get_value('author_id')

        capture_words: StateParams = await state.get_value('capture_words_state')
        words_set = capture_words.captured_items_set

        input_coll: StateParams = await state.get_value('input_coll_state')
        collocation = input_coll.input_text

        input_media: StateParams = await state.get_value('input_media_state')
        # media_caption = input_media.input_text
        media_type = input_media.media_type
        media_tg_id = input_media.media_id

        input_caption: StateParams = await state.get_value('input_caption_state')
        caption = input_caption.input_text

        capture_levels: StateParams = await state.get_value('capture_levels_state')
        levels_set = capture_levels.captured_items_set

        capture_days: StateParams = await state.get_value('capture_days_state')
        days_set = capture_days.captured_items_set

        state_text = await state_text_builder(state)

        res = True
        for word_id in words_set:
            for level in levels_set:
                for study_day in days_set:
                    res = res and await add_media_to_db(media_type=media_type,
                                                        word_id=word_id,
                                                        collocation=collocation,
                                                        caption=caption,
                                                        telegram_id=media_tg_id,
                                                        study_day=study_day,
                                                        author_id=author_id,
                                                        level=level)

        message_text = f'----- ----- -----\n{state_text}----- ----- -----\n'
        if res:
            message_text += MESS_ADDED_TO_DB
            if media_tg_id:
            # Получаем media_id
                media_id = (await get_medias_by_filters(telegram_id=media_tg_id))[0].id
                # Выделяем файл, который хотим сохранить
                file = await bot.get_file(media_tg_id)
                # Подпапка для сохранения
                path_name = datetime.now().strftime('%y-%m')
                # Проверяем наличие директории и создаем её, если её ещё нет

                if not os.path.exists(os.path.join(media_dir, path_name)):
                    os.makedirs(os.path.join(media_dir, path_name))
                   # Даем название и путь этому файлу
                    for word in words_set:
                        filename = f"{media_id}-{media_type}-{word}{os.path.splitext(file.file_path)[1]}"
                        dest_path = os.path.join(media_dir, path_name, filename)
                        # Скачиваем файл
                        await bot.download_file(file.file_path, dest_path)
        else:
            message_text += MESS_ERROR_ADDED_TO_DB

        reply_kb = await keyboard_builder(menu_pack=menu_add_coll, buttons_base_call="")


        media_state: StateParams = await state.get_value('input_media_state')

        await mess_answer(source=call,
                          media_type=media_state.media_type,
                          media_id=media_state.media_id,
                          message_text=message_text,
                          reply_markup=reply_kb)
        await call.answer()


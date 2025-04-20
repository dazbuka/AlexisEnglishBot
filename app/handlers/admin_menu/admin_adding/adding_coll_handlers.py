from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ContentType
from app.database.requests import get_users_by_filters
from app.utils.admin_utils import (message_answer,
                                   state_text_builder)
from aiogram.fsm.state import State, StatesGroup
import data.admin_messages as amsg
import app.database.requests as rq
import app.keyboards.admin_keyboards as akb
from config import bot, media_dir

# from app.handlers.admin_menu.input_states import AddWord, FSMInputMessageSet, InputStateParams

from app.handlers.admin_menu.states.input_states import (StateParams, FSMExecutor, CaptureLevelsStateParams,
                                                         CaptureDatesStateParams, CaptureWordsStateParams)

from app.keyboards.keyboard_builder import keyboard_builder, update_button_with_call_base
from app.keyboards.menu_buttons import (button_menu_setting_back, button_new_main_menu, button_change_words,
                                        button_menu_adding_back, button_change_levels, button_change_parts,
                                        button_change_translation, button_change_definition, button_new_admin_menu,
                                        button_change_collocation, button_change_media, button_change_dates)
from app.handlers.common_settings import *

from app.utils.admin_utils import (message_answer, mess_answer,
                                   get_word_list_for_kb_with_ids,
                                   send_any_media_to_user_with_kb,
                                   get_date_list_for_kb)


adding_coll_router = Router()

class AddColl(StatesGroup):
    author_id = State()
    capture_words_state = State()
    input_coll_state = State()
    input_media_state = State()
    media_id = State()
    media_type = State()
    capture_levels_state = State()
    capture_dates_state = State()
    confirmation_state = State()


# переход в меню добавления задания по схеме
@adding_coll_router.callback_query(F.data == C_ADM_ADD_COLL)
async def adding_word_first_state(call: CallbackQuery, state: FSMContext):
    print('here in adding coll')
    # очистка стейта
    await state.clear()

    menu_add_coll = [
        [button_menu_adding_back, button_new_admin_menu, button_new_main_menu]
    ]

    menu_add_coll_with_changing = [
        [update_button_with_call_base(button_change_words, CALL_ADD_COLL + CALL_ADD_ENDING),
         update_button_with_call_base(button_change_collocation, CALL_ADD_COLL + CALL_ADD_ENDING),
         update_button_with_call_base(button_change_levels, CALL_ADD_COLL + CALL_ADD_ENDING)],
        [update_button_with_call_base(button_change_media, CALL_ADD_COLL + CALL_ADD_ENDING),
         update_button_with_call_base(button_change_dates, CALL_ADD_COLL + CALL_ADD_ENDING)],
        [button_menu_setting_back, button_new_admin_menu, button_new_main_menu]
    ]

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


    levels_state = CaptureLevelsStateParams(self_state=AddColl.capture_levels_state,
                                            next_state=AddColl.capture_dates_state,
                                            call_base=CALL_ADD_COLL,
                                            menu_add=menu_add_coll,
                                            items_kb_list=LEVEL_LIST,
                                            is_can_be_empty=True,
                                            is_only_one=True)
    await state.update_data(capture_levels_state=levels_state)

    dates_state = CaptureDatesStateParams(self_state=AddColl.capture_dates_state,
                                          next_state=AddColl.confirmation_state,
                                          call_base=CALL_ADD_COLL,
                                          menu_add=menu_add_coll,
                                          items_kb_list=await get_date_list_for_kb(),
                                          is_only_one=True)

    await state.update_data(capture_dates_state=dates_state)



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
@adding_coll_router.message(F.text, AddColl.capture_levels_state)
@adding_coll_router.message(F.text, AddColl.capture_dates_state)
async def admin_adding_word_capture_word(message: Message, state: FSMContext):
    # проверяем слово в базе данных
    # создаем экземпляр класса для обработки текущего состояния фсм
    current_fsm = FSMExecutor()
    # обрабатываем экземпляра класса, который анализирует наш колл и выдает сообщение и клавиатуру
    await current_fsm.execute(fsm_state=state, fsm_mess=message)

    media_state: StateParams = await state.get_value('input_media_state')

    await mess_answer(source=message,
                      media_type=media_state.media_type,
                      media_id=media_state.media_id,
                      message_text=current_fsm.message_text,
                      reply_markup=current_fsm.reply_kb)


@adding_coll_router.callback_query(F.data.startswith(CALL_ADD_COLL + CALL_CAPTURE_WORD), AddColl.capture_words_state)
@adding_coll_router.callback_query(F.data.startswith(CALL_ADD_COLL + CALL_CAPTURE_LEVEL), AddColl.capture_levels_state)
@adding_coll_router.callback_query(F.data.startswith(CALL_ADD_COLL + CALL_CAPTURE_DATE), AddColl.capture_dates_state)
async def set_scheme_capture_words_from_call(call: CallbackQuery, state: FSMContext):
    # создаем экземпляр класса для обработки текущего состояния фсм
    current_fsm = FSMExecutor()
    # обрабатываем экземпляра класса, который анализирует наш колл и выдает сообщение и клавиатуру
    await current_fsm.execute(fsm_state=state, fsm_call=call)
    # отвечаем заменой сообщения


    media_state: StateParams = await state.get_value('input_media_state')

    if media_state.media_id:
        await send_any_media_to_user_with_kb(bot=bot,
                                             user_tg_id=call.from_user.id,
                                             media_type=media_state.media_type,
                                             caption=current_fsm.message_text,
                                             file_id=media_state.media_id,
                                             reply_kb=current_fsm.reply_kb)
    else:
        await call.message.edit_text(current_fsm.message_text, reply_markup=current_fsm.reply_kb)
        # await message_answer(source=call, message_text=current_fsm.message_text, reply_markup=current_fsm.reply_kb)
    await call.answer()


# конечный обработчик всего стейта
@adding_coll_router.callback_query(F.data.startswith(CALL_ADD_COLL + CALL_ADD_ENDING), AddColl.confirmation_state)
async def admin_adding_task_capture_confirmation_from_call(call: CallbackQuery, state: FSMContext):
    # вытаскиваем из колбека уровень
    confirm = call.data.replace(CALL_ADD_COLL + CALL_ADD_ENDING, '')
    # уходим обратно если нужно что-то изменить

    if (confirm == CALL_CHANGING_WORD or confirm == CALL_CHANGING_COLL or confirm == CALL_CHANGING_LEVEL
            or confirm == CALL_CHANGING_MEDIA or confirm == CALL_CHANGING_DATE):

        confirmation_state: StateParams = await state.get_value('confirmation_state')

        if confirm == CALL_CHANGING_WORD:
            # при нажатии на изменение задаем следующий стейт элементов
            confirmation_state.next_state = AddColl.capture_words_state
            # делаем так, чтобы в стейте добавления последний стейт (на изменения который) стал следующим
            capture_words_state: StateParams = await state.get_value('capture_words_state')
            capture_words_state.next_state = AddColl.confirmation_state
            await state.update_data(capture_words_state=capture_words_state)

        # elif confirm == CALL_CHANGING_PART:
        #     # при нажатии на изменение задаем следующий стейт элементов
        #     confirmation_state.next_state = AddWord.capture_parts_state
        #     # делаем так, чтобы в стейте добавления последний стейт (на изменения который) стал следующим
        #     capture_parts_state: StateParams = await state.get_value('capture_parts_state')
        #     capture_parts_state.next_state = AddWord.confirmation_state
        #     await state.update_data(capture_parts_state=capture_parts_state)
        #
        # elif confirm == CALL_CHANGING_LEVEL:
        #     # при нажатии на изменение задаем следующий стейт элементов
        #     confirmation_state.next_state = AddWord.capture_levels_state
        #     # делаем так, чтобы в стейте добавления последний стейт (на изменения который) стал следующим
        #     capture_levels_state: StateParams = await state.get_value('capture_levels_state')
        #     capture_levels_state.next_state = AddWord.confirmation_state
        #     await state.update_data(capture_levels_state=capture_levels_state)
        #
        # elif confirm == CALL_CHANGING_DEFINITION:
        #     # при нажатии на изменение задаем следующий стейт элементов
        #     confirmation_state.next_state = AddWord.input_definition_state
        #     # делаем так, чтобы в стейте добавления последний стейт (на изменения который) стал следующим
        #     input_definition_state: StateParams = await state.get_value('input_definition_state')
        #     input_definition_state.next_state = AddWord.confirmation_state
        #     await state.update_data(input_definition_state=input_definition_state)
        #
        # elif confirm == CALL_CHANGING_TRANSLATION:
        #     # при нажатии на изменение задаем следующий стейт элементов
        #     confirmation_state.next_state = AddWord.input_translation_state
        #     # делаем так, чтобы в стейте добавления последний стейт (на изменения который) стал следующим
        #     input_translation_state: StateParams = await state.get_value('input_translation_state')
        #     input_translation_state.next_state = AddWord.confirmation_state
        #     await state.update_data(input_translation_state=input_translation_state)

        await state.update_data(confirmation_state=confirmation_state)
        current_fsm = FSMExecutor()
        await current_fsm.execute(state, call)
        await call.message.edit_text(current_fsm.message_text, reply_markup=current_fsm.reply_kb)
        await call.answer()


    elif confirm == CALL_CONFIRM:

        # основной обработчик, запись в бд
        author_id = await state.get_value('author_id')

        capture_words: StateParams = await state.get_value('capture_words_state')
        words_set = capture_words.captured_items_set

        # capture_parts: StateParams = await state.get_value('capture_parts_state')
        # parts_set = capture_parts.captured_items_set

        capture_levels: StateParams = await state.get_value('capture_levels_state')
        levels_set = capture_levels.captured_items_set

        capture_dates: StateParams = await state.get_value('capture_dates_state')
        dates_set = capture_dates.captured_items_set

        input_translation: StateParams = await state.get_value('input_translation_state')
        translation_item = input_translation.input_text

        state_text = await state_text_builder(state)

        res = True
        # for part in parts_set:
        #     for level in levels_set:
        #         res = res and await rq.add_word_to_db(word=word_item,
        #                                               level=level,
        #                                               part=part,
        #                                               translation=translation_item,
        #                                               definition=definition_item,
        #                                               author_id=author_id)

        message_text = f'----- ----- -----\n{state_text}----- ----- -----\n'

        if res:
            message_text += amsg.ADM_ADD_TASK_ADDED
        else:
            message_text += amsg.ADM_ADD_TASK_ERROR

        reply_kb = await akb.admin_adding_menu_kb()
        await call.message.edit_text(message_text, reply_markup=reply_kb)
        await call.answer()


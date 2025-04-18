from curses.ascii import isdigit
from aiogram.fsm.state import State, StatesGroup
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from app.utils.admin_utils import get_text_from_group_adding_state
import app.utils.admin_utils as aut
from app.utils.admin_utils import message_answer
import app.database.requests as rq
import app.keyboards.admin_keyboards as akb
import app.handlers.callback_messages as callmsg
import data.common_messages as cmsg
import data.admin_messages as amsg


admin_adding_group_router = Router()

class AddGroup(StatesGroup):
    name = State()
    users_kb = State()
    level = State()
    confirmation = State()

@admin_adding_group_router.callback_query(F.data == amsg.ADMIN_BUTTON_ADD_GROUP)
async def admin_adding_group_start(call: CallbackQuery, state: FSMContext):
    state_text = await aut.get_text_from_group_adding_state(state)
    message_text = f'{state_text}\n{amsg.ADM_ADD_GROUP_NAME}'
    reply_kb = await akb.admin_adding_group_kb()
    await call.message.edit_text(message_text, reply_markup=reply_kb)
    await state.set_state(AddGroup.name)
    await call.answer()


@admin_adding_group_router.message(F.text, AddGroup.name)
async def admin_adding_group_capture_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    state_text = await get_text_from_group_adding_state(state)
    message_text = f'{state_text}\n{amsg.ADM_ADD_GROUP_USERS}'
    user_list = await aut.get_users_list_for_kb_with_limit()
    await state.update_data(users_kb=user_list)
    reply_kb = await akb.admin_adding_group_kb(adding_user_list=user_list)
    await message_answer(source=message, message_text=message_text, reply_markup=reply_kb)
    await state.set_state(AddGroup.users_kb)


# хендлер захвата слова из клавиатуры
@admin_adding_group_router.callback_query(F.data.startswith(callmsg.CALL_ADM_ADD_GROUP_USER), AddGroup.users_kb)
async def admin_adding_group_capture_users_from_call(call: CallbackQuery, state: FSMContext):
    # вытаскиваем из колбека слово
    user_call=call.data.replace(callmsg.CALL_ADM_ADD_GROUP_USER, '')
    users_list = (await state.get_data()).get('users_kb')
    # костыль, не позволяющий пройти дальше не выбрав ничего
    have_check = False
    for user in users_list:
        if not isdigit(user[0]):
            have_check = True

    if user_call == callmsg.CALL_ADMIN_END_CHOOSING and have_check:
        new_user_list = await aut.get_list_from_check_list(users_list)
        await state.update_data(users_kb=new_user_list)
        # вытаскиваем из стейта текст сообщения
        state_text = await aut.get_text_from_group_adding_state(state)
        message_text = f'{state_text}\n{amsg.ADM_ADD_GROUP_LEVEL}'
        reply_kb = await akb.admin_adding_group_kb(adding_level=True)
        await call.message.edit_text(message_text, reply_markup=reply_kb)
        await state.set_state(AddGroup.level)
        await call.answer()
    else:
        users_list=await aut.set_check_in_list(checked_list=users_list, checked_item=user_call)
        message_text = amsg.ADM_ADD_GROUP_USERS_MORE
        reply_kb = await akb.admin_adding_group_kb(adding_user_list=users_list)
        await call.message.edit_text(message_text, reply_markup=reply_kb)
        await state.update_data(users_kb=users_list)
        await state.set_state(AddGroup.users_kb)
        await call.answer()


@admin_adding_group_router.message(F.text, AddGroup.users_kb)
async def admin_adding_group_returning_from_message(message: Message, state: FSMContext):
    user_list = (await state.get_data()).get('users_kb')
    message_text = amsg.ADM_ADD_GROUP_USERS_MORE
    reply_kb = await akb.admin_adding_group_kb(adding_user_list=user_list)
    await message_answer(source=message, message_text=message_text, reply_markup=reply_kb)
    await state.set_state(AddGroup.users_kb)



# хендлер получения уровня
@admin_adding_group_router.callback_query(F.data.startswith(callmsg.CALL_ADM_ADD_GROUP_LEVEL), AddGroup.level)
async def admin_adding_group_capture_level(call: CallbackQuery, state: FSMContext):
    # вытаскиваем из колбека уровень, запоминаем, приглашаем ввести часть речи
    level=call.data.replace(callmsg.CALL_ADM_ADD_GROUP_LEVEL, '')
    await state.update_data(level=level)
    state_text = await get_text_from_group_adding_state(state)
    message_text = f'{state_text}\n{amsg.ADM_ADD_GROUP_CONFIRMATION}'
    reply_kb = await akb.admin_adding_group_kb(confirmation=True)
    await call.message.edit_text(message_text, reply_markup=reply_kb)
    await call.answer()
    await state.set_state(AddGroup.confirmation)


# хендлер получения уровня, если что-то вписано с клавиатуры - отправляем снова на кнопки
@admin_adding_group_router.message(F.text, AddGroup.level)
async def admin_adding_group_capture_level_from_text(message: Message, state: FSMContext):
    # даже не обрабатываем ввод - сразу приглашаем обратно выбрать с клавиатуры
    state_text = await get_text_from_group_adding_state(state)
    message_text = f'{state_text}\n{amsg.ADM_ADD_GROUP_INV_KB}'
    reply_kb = await akb.admin_adding_group_kb(adding_level=True)
    await message_answer(source=message, message_text=message_text, reply_markup=reply_kb)
    await state.set_state(AddGroup.level)


@admin_adding_group_router.callback_query(F.data.startswith(callmsg.CALL_ADM_ADD_GROUP_CONF), AddGroup.confirmation)
async def admin_adding_group_capture_confirmation_from_call(call: CallbackQuery, state: FSMContext):
    # вытаскиваем из колбека уровень
    confirm = call.data.replace(callmsg.CALL_ADM_ADD_GROUP_CONF, '')
    if confirm == cmsg.YES:
        st_data = await state.get_data()
        name = st_data.get("name")
        users_list = st_data.get("users_kb")
        level = st_data.get("level")
        users = [int(x.split('-', 1)[0]) for x in users_list]
        users_for_db = ','.join(map(str, users))
        users_text = '\n'.join(map(str, st_data.get("users_kb")))
        res = await rq.set_group(name=name, users=users_for_db, level=level)

        if res:
            message_text = amsg.ADM_ADD_GROUP_ADDED.format(name, users_text)
        else:
            message_text = amsg.ADM_ADD_GROUP_ERROR

        reply_kb = await akb.admin_adding_menu_kb()
        await call.message.edit_text(message_text, reply_markup=reply_kb)
        await call.answer()

    elif confirm == cmsg.NO:
        await state.clear()
        reply_kb = await akb.admin_adding_group_kb()
        message_text = amsg.ADM_ADD_GROUP_AGAIN
        await call.message.edit_text(message_text, reply_markup=reply_kb)
        await call.answer()






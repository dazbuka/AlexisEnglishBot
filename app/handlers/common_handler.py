from aiogram import F, Router
from aiogram.filters.command import Command
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
import app.handlers.callback_messages as callmsg
import app.keyboards.user_keyboards as ukb
from config import bot, logger
from app.utils.admin_utils import message_answer
from app.handlers.common_settings import *
import app.database.requests as rq
from app.utils.admin_utils import message_answer
import data.admin_messages as amsg
from app.database.models import UserStatus


common_router = Router()


# разблокировка или удаление пользователя
@common_router.callback_query(F.data.startswith(amsg.ADMIN_BUTTON_UNBLOCK_USER))
async def unblock_user(call: CallbackQuery, state: FSMContext):
    await state.clear()
    # вытаскиваем из колбека номер пользователя
    user_tg_id = int(call.data.replace(amsg.ADMIN_BUTTON_UNBLOCK_USER, ''))
    # меняем статус
    await rq.update_user_status(user_tg_id, UserStatus.ACTIVE)
    # отвечаем админу
    await message_answer(source=call, message_text='Пользователь разблокирован',
                         reply_markup=await ukb.common_main_kb(call.from_user.id))
    # отвечаем разблокированному пользователю
    await bot.send_message(user_tg_id, "--Unblocked--. \nHello!", reply_markup=await ukb.common_main_kb(user_tg_id))
    await call.answer()


# удаление пользователя
@common_router.callback_query(F.data.startswith(amsg.ADMIN_BUTTON_DELETE_USER))
async def delete_user(call: CallbackQuery, state: FSMContext):
    await state.clear()
    # вытаскиваем из колбека номер пользователя
    user_tg_id = int(call.data.replace(amsg.ADMIN_BUTTON_DELETE_USER, ''))
    # меняем статус
    await rq.update_user_status(user_tg_id, UserStatus.DELETED)
    # отвечаем админу
    await message_answer(source=call, message_text='Пользователь удален',
                         reply_markup=await ukb.common_main_kb(call.from_user.id))
    # отвечаем разблокированному пользователю
    await bot.send_message(user_tg_id, "--Deleted--. \nBy!")
    await call.answer()


# команда хелп
@common_router.message(Command('help'))
async def get_help(message: Message):
    logger.info(f'{message.from_user.id}-отправил сообщение: {message.text}')
    message_text = MESS_HELP
    await message_answer(source=message, message_text=message_text)

# действия при нажатии инлайн кнопки главное меню с удалением или редактированием сообщения
@common_router.callback_query(F.data == callmsg.CALL_PRESS_MAIN_MENU)
async def main_menu(call: CallbackQuery, state: FSMContext):
    await state.clear()
    message_text = MESS_PRESS_ANY_BUTTON
    reply_kb = await ukb.common_main_kb(user_tg_id= call.from_user.id)
    await message_answer(source=call, message_text=message_text, reply_markup=reply_kb)
    await call.answer()


# произвольное сообщение
@common_router.message(F.text)
async def to_main_menu(message: Message):
    message_text = MESS_DONT_UNDERSTAND
    reply_kb = await ukb.common_main_kb(user_tg_id= message.from_user.id)
    await message_answer(source=message, message_text=message_text, reply_markup=reply_kb)


# произвольный call
@common_router.callback_query(F.data)
async def any_call(call: CallbackQuery):
    logger.info(f'{call.from_user.username} ({call.from_user.first_name})'
                f' - непонятный call *{call.data}*')
    await call.answer(f'{MESS_DONT_UNDERSTAND}, call: {call.data}', show_alert=True)

# произвольный call
@common_router.message(F.photo)
async def to_main_menu(message: Message):
    await message.answer(message.photo[-1].file_id, reply_markup=await ukb.common_main_kb(user_tg_id= message.from_user.id))
    try:
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id - 1)
    except TelegramBadRequest as e:
        logger.error(f'{message.from_user.username} ({message.from_user.first_name})'
                     f' - ошибка при удалении сообщения id по *{message.text}*: {e}')

@common_router.message(F.video)
async def to_main_menu(message: Message):
    await message.answer(message.video.file_id,
                         reply_markup=await ukb.common_main_kb(user_tg_id=message.from_user.id))
    try:
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id - 1)
    except TelegramBadRequest as e:
        logger.error(f'{message.from_user.username} ({message.from_user.first_name})'
                     f' - ошибка при удалении сообщения id по *{message.text}*: {e}')





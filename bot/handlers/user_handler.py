from ast import Add
from socket import close
from aiogram import types, Dispatcher
from tools.db_dispatcher import DataBaseDispatcher
from aiogram.dispatcher import FSMContext




async def start_bot(message: types.Message):
    await message.answer("Привет")


async def close_state(messsage: types.Message, state: FSMContext):
    await messsage.answer("Досрочно завершено")
    await state.finish()

def register_user_handlers(dp: Dispatcher, admin_id: int):
    dp.register_message_handler(start_bot, commands=["start"])
    dp.register_message_handler(close_state, commands="close_process", state="*")
    
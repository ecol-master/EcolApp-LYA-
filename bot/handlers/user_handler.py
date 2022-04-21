from aiogram import types, Dispatcher
from tools.db_dispatcher import DataBaseDispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class LoginUser(StatesGroup):
    user_email = State()
    user_password = State()

db_dispatcher = DataBaseDispatcher()

async def start_bot(message: types.Message):
    await message.answer("Привет")


async def close_state(messsage: types.Message, state: FSMContext):
    await messsage.answer("Досрочно завершено")
    await state.finish()

async def login_user_start(message: types.Message):
    await message.answer("Отлично! Для начала укажите адрес электронной почты")
    await LoginUser.user_email.set()

async def login_email(message: types.Message, state: FSMContext):
    await state.update_data(user_email=message.text)
    await LoginUser.next()
    await message.answer("Теперь укажите пароль от аккаунта")

async def login_password(message: types.Message, state: FSMContext):
    await state.update_data(user_password=message.text)
    user_data = await state.get_data()
    print(db_dispatcher.login_user(message.from_user.id, **user_data))
    await state.finish()

def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(start_bot, commands=["start"])
    dp.register_message_handler(close_state, commands="close_process", state="*")
    dp.register_message_handler(login_user_start, commands="login", state="*")
    dp.register_message_handler(login_email, state=LoginUser.user_email)
    dp.register_message_handler(login_password, state=LoginUser.user_password)
from aiogram import Dispatcher, types
from tools.db_dispatcher import DataBaseDispatcher
from aiogram.dispatcher.filters import IDFilter
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

db_dispatcher = DataBaseDispatcher()

class AddAdmin(StatesGroup):
    admin_name = State()
    admin_email = State()
    admin_password = State()

async def get_users(message: types.Message):
    users = db_dispatcher.get_users()
    await message.answer(text="\n".join(
        [f"{user['nickname']} {user['email']}" for user in users["users"]]
    ))

async def set_admin_start(message: types.Message):
    await message.answer("Укажите имя нового администратора")
    await AddAdmin.admin_name.set()

async def set_admin_name(message: types.Message, state: FSMContext):
    if message.text.strip() == "":
        await message.answer("Имя должно представлять собой строку символов")
        return 
    await state.update_data(admin_name=message.text)
    await AddAdmin.next()
    await message.answer("Теперь укажите почту пользователя")
    
async def set_admin_email(message: types.Message, state: FSMContext):
    await state.update_data(admin_email=message.text)
    await AddAdmin.next()
    await message.answer("Укажите пароль для аккаунта")

async def set_admin_password(message: types.Message, state: FSMContext):
    if len(message.text) < 8:
        await message.answer("Пароль должен быть длиннее")
        return
    await state.update_data(admin_password=message.text)

    user_data = await state.get_data()
    if db_dispatcher.add_user(**user_data):
        await message.answer("Админ добавлен")
    else:
        await message.answer("Что то пошло не так и новый админ не был добавлен")
    await state.finish()



def register_admin_handlers(dp: Dispatcher, admin_id: int):
    
    dp.register_message_handler(get_users, commands=["users"])
    dp.register_message_handler(set_admin_start, IDFilter(user_id=admin_id), commands="add_admin", state="*")
    dp.register_message_handler(set_admin_name, state=AddAdmin.admin_name)
    dp.register_message_handler(set_admin_email, state=AddAdmin.admin_email)
    dp.register_message_handler(set_admin_password, state=AddAdmin.admin_password)
    
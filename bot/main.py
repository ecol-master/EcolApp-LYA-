from aiogram import Dispatcher, Bot
from handlers.user_handler import register_user_handlers
from tools.commands_worker import set_bot_commands
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from handlers.admin_handler import register_admin_handlers
from config import TOKEN, ADMIN_ID
import asyncio
import logging

async def main():
    bot = Bot(token=TOKEN)

    dp = Dispatcher(bot=bot, storage=MemoryStorage())
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    await set_bot_commands(bot=bot)

    register_user_handlers(dp)
    register_admin_handlers(dp=dp, admin_id=ADMIN_ID)
    
    await dp.skip_updates()
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())


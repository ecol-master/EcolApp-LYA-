from aiogram import Bot
from aiogram.types import BotCommand
from aiogram.types.bot_command_scope import BotCommandScopeDefault, BotCommandScopeChat


async def set_bot_commands(bot: Bot):
    usercommands = [
        BotCommand(command="start", description="Справка по использованию бота"),
        BotCommand(command="users", description="получить пользователей"),
        BotCommand(command="add_admin", description="добавить нового администратора"),
    ]
    await bot.set_my_commands(usercommands, scope=BotCommandScopeDefault())

    # admin_commands = [
    #     BotCommand(command="add_new_admin", description="Получение информации о пользователе")
    # ]
    # await bot.set_my_commands(admin_commands, scope=BotCommandScopeChat(chat_id=admin_chat_id))
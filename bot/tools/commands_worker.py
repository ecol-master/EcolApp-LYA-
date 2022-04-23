from aiogram import Bot
from aiogram.types import BotCommand
from aiogram.types.bot_command_scope import BotCommandScopeDefault, BotCommandScopeChat
from aiogram.dispatcher.filters import IDFilter


async def set_bot_commands(bot: Bot, admin_id: int):
    usercommands = [
        BotCommand(command="start", description="Справка по использованию бота"),
        BotCommand(command="login", description="Войти в аккаунт"),
        BotCommand(command="get_info", description="Получить информацию об Экологии"),
        BotCommand(command="account_actions", description="Действия с аккаунтом"),
        BotCommand(command="close_process", description="Завершить действие в случае ошибки при выборе команды")
    ]
    await bot.set_my_commands(usercommands, scope=BotCommandScopeDefault())

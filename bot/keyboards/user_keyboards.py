from ctypes import resize
from unittest.mock import call
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_information = InlineKeyboardMarkup(row_width=2)
main_information.add(
    InlineKeyboardButton(text="Concepts 🔰", callback_data="concepts"), 
    InlineKeyboardButton(text="Nature 🌄", callback_data="nature")
)
main_information.add(InlineKeyboardButton(text="Scientists' opinions 👀", callback_data="opinions"))

account_actions = InlineKeyboardMarkup(row_width=1)
account_actions.add(
    InlineKeyboardButton(text="Account Statistic", callback_data="statistic"), 
    InlineKeyboardButton(text="Sign out", callback_data="sign_out")
)
from aiogram import types, Dispatcher
from tools.db_dispatcher import DataBaseDispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.user_keyboards import main_information, account_actions
import json

class LoginUser(StatesGroup):
    user_email = State()
    user_password = State()

db_dispatcher = DataBaseDispatcher()

async def start_bot(message: types.Message):
    service = "Some URL"
    await message.answer(text=f"Привет ✌!\nEcolStudyBot - бот сервиса {service}!")


async def close_state(messsage: types.Message, state: FSMContext):
    await messsage.answer("Досрочно завершено")
    await state.finish()

# functions for login user
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
    result = db_dispatcher.login_user(message.from_user.id, **user_data)
    match result:
        case {"success":"user was updated"}:
            await message.answer("Ваши данные успешно обновлены!")
        case {"success":"user was added"}:
            await message.answer("Аккаут добавлен")
        case {"failed": "not found"}:
            await message.answer("Неправильные адрес почты или пароль. Убедитесь в правильности введенных данных")
        case _:
            await message.answer("Ничего не произошло потому что произошло непредвиденное :(")
    
    await state.finish()


# functions for action with account


buttons_texts = {
    "concepts": {
        "text": "*🚗 Автомобили использующие воду в качестве источника топлива ❕*\n\nПервым автомобилем на водородных топливных элементах стал Electrovan от General Motors 1966 года. Он был оборудован резервуарами для хранения водорода и мог проехать до 193 км на одном заряде.\n\nОднако это был единичный демонстрационный экземпляр, который передвигался только по территории завода.В 1979-м появился первый автомобиль BMW с водородным двигателем. Толчком к его созданию послужили нефтяные кризисы 1970-х, и по их окончании об идее альтернативных двигателей забыли вплоть до 2000-х годов.\n\nВ 2007 году та же BMW выпустила ограниченную серию автомобилей Hydrogen 7, которые могли работать как на бензине, так и на водороде. Но машина была недешевой, при этом 8-килограммового баллона с газом хватало всего на 200-250 км.Подробнее на РБК",
        "links": ["https://trends.rbc.ru/trends/industry/6048e0629a794750974c67a7",
            "https://www.popularmechanics.com/cars/a3428/4271579/",
            "https://www.unilad.co.uk/life/inventor-of-water-powered-car-died-screaming-they-poisoned-me"
        ]
    },
    "nature": {"text":"*Состояние природы в мире*🌏\n\nПо экспертным оценкам, современная экологическая ситуация в России на _40–50%_ определяется не только загрязнениями и др. влияниями предшествующих лет, но и загрязнениями, обусловленными в основном милитаризацией экономики, химизацией сельского хозяйства, _экстенсивным использованием природных ресурсов_, чернобыльской и др. авариями и катастрофами в СССР, а также глобальными изменениями среды под влиянием деятельности человека на всей планете.", 
    "links":["https://meteoinfo.ru/novosti/99-pogoda-v-mire", 
    "https://www.nkj.ru/archive/articles/10376/", 
    "https://bigenc.ru/geography/text/5575813"]},
    "opinions":{"text":"Будущее будет в корне отличаться от настоящего\n\n_'Поскольку 84% нашей энергии по-прежнему поступает из нефти, угля и газа, большая часть перехода на возобновляемые источники энергии еще впереди. То, что наступит другое будущее, не означает, что настоящее просто уйдет со сцены. Возобновляемые источники энергии не меняют центральное место энергии в геополитике. Также, учитывая, что энергетический переход будет долгим, он не положит конец геополитике ископаемого топлива.' - Хелен Томпсон_\n\n_Да, альтернативные источники энергии и удаление углерода будут иметь решающее значение для обезуглероживания. Но давайте не будем делать вид, что они прибудут достаточно быстро, чтобы ограничить рост температуры на 1,5 °C выше доиндустриального уровня. Политики и исследователи также должны больше работать с уже зарекомендовавшими себя методами — высокоэффективными, поддерживаемыми общественностью способами сокращения потребления энергии._ - Мари Клэр Брисбуа", 
    "links":["https://www.nature.com/articles/d41586-022-00713-3", 
    "https://www.nature.com/articles/d41586-022-00560-2"]}
}

async def user_information(message: types.Message):
    await message.answer(text="Нажмите на одну из категорий чтобы узнать подробнее...", reply_markup=main_information)


async def user_concepts_kb(callback: types.CallbackQuery):
    bot = callback.bot
    await bot.answer_callback_query(callback.id)
    text = buttons_texts["concepts"]
    links = '\n'.join(text['links'])
    text = f"{text['text']}\n\nУзнать подробнее вы можете здесь:\n\n{links}"
    await bot.send_message(chat_id=callback.message.chat.id, text=text, parse_mode=types.ParseMode.MARKDOWN)

async def user_nature_kb(callback:types.CallbackQuery):
    bot = callback.bot
    await bot.answer_callback_query(callback.id)
    text = buttons_texts["nature"]
    links = "\n".join(text["links"])
    text = f"{text['text']}\n\nУзнать подробнее вы можете здесь:\n\n{links}"
    await bot.send_message(chat_id=callback.message.chat.id, text=text, parse_mode=types.ParseMode.MARKDOWN)

async def user_opinions_kb(callback: types.CallbackQuery):
    bot = callback.bot
    await bot.answer_callback_query(callback.id)
    text = buttons_texts["opinions"]
    links = text["links"]
    text = f"{text['text']}\n\nУзнать подробнее вы можете здесь:\n\n{links}"
    await bot.send_message(chat_id=callback.message.chat.id, text=text, parse_mode=types.ParseMode.MARKDOWN)

# user functions to account actions

async def show_user_account_actions(message: types.Message):
    result = db_dispatcher.check_bot_user(message.from_user.id)
    match result:
        case {
            "Name":name,
            "description": description,
            "data_registration":data_register}:
            pass
        case _:
            await message.answer("Вы не вошли в свой аккаунт")
            return
    await message.answer(text="Выберите одно из следующих действий", reply_markup=account_actions)


async def user_account_statistic(callback: types.CallbackQuery):
    bot = callback.bot
    await bot.answer_callback_query(callback.id)
    info = db_dispatcher.get_user_info(callback.from_user.id)

    text_info = f"Your nickname: {info['Name']}\nDescription profile: {info['description']}\nData registration: {info['data_registration']} "
    await bot.send_message(chat_id=callback.message.chat.id, text=text_info)

async def account_sign_out(callback: types.CallbackQuery):
    bot = callback.bot
    await bot.answer_callback_query(callback.id)
    result = db_dispatcher.delete_bot_user(callback.from_user.id)
    match result:
        case  {'success': 'OK'}:
            await bot.send_message(chat_id=callback.message.chat.id, text="Вы успешно вышли из аккаунта")
        case _:
            await bot.send_message(chat_id=callback.message.chat.id, text="Выйти не удалось")


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(start_bot, commands=["start"])
    dp.register_message_handler(close_state, commands="close_process", state="*")

    # login handlers
    dp.register_message_handler(login_user_start, commands="login", state="*")
    dp.register_message_handler(login_email, state=LoginUser.user_email)
    dp.register_message_handler(login_password, state=LoginUser.user_password)

    # regsiter callback handlers on kb main_informations
    dp.register_message_handler(user_information, commands=["get_info"])
    dp.register_callback_query_handler(user_concepts_kb, text="concepts")
    dp.register_callback_query_handler(user_nature_kb, text="nature")
    dp.register_callback_query_handler(user_opinions_kb, text="opinions")

    # register account actions
    dp.register_message_handler(show_user_account_actions, commands=["account_actions"])
    dp.register_callback_query_handler(user_account_statistic, text="statistic")
    dp.register_callback_query_handler(account_sign_out, text="sign_out")

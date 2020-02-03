from utils import get_param
import settings

# Telegram modules
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram.vendor.ptb_urllib3 import urllib3
from telegram import Update, Message

from emoji import emojize

from glob import glob
from random import choice

import ephem
from datetime import datetime
import logging

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.basicConfig(format="%(name)s - %(levelname)s - %(message)s",
                    level=logging.INFO,
                    filename="bot.log")

def start(update: Update, context):
    """
    Обработчик команды /start
    Args:
        update:  Контекст бота
        context: Внешний контекст

    Returns:
        None
    """
    smile = emojize(choice(settings.USER_EMOJI), use_aliases=True)
    text = f'Привет {smile}'
    print(text)
    update.message.reply_text(text)


def planet(update: Update, context: CallbackContext):
    """
    Обработчик команды /planet

    Args:
        update:  Контекст бота
        context: Внешний контекст

    Returns:
        None
    """
    # Достаём название плнеты/звезды из сообщения
    user_text = update.message.text.split()
    if len(user_text) < 2:
        error_msg = "Некорректные данные.\n"\
                    "Введите команду в виде: /planet Mars."

        print(error_msg)
        update.message.reply_text(error_msg)
        return

    planet_name = user_text[1]

    # Генерируем список.
    plan_moon = []
    for _0, _1, name in ephem._libastro.builtin_planets():
        plan_moon.append(name)

    # Проверяем наличие планеты в словаре.
    if not (planet_name in plan_moon):
        error_msg = "Неизвестная пленета.\n" \
                    "Список доступных планет:\n"\
                    "{}".format("\n".join(plan_moon))

        print(error_msg)
        update.message.reply_text(error_msg)
        return

    # Генерируем, выводим и отправляем ответ
    planet_obj = getattr(ephem, planet_name)
    planet_obj = planet_obj(datetime.now())

    answer_text = """
    Планета {}, сейчас находится в созвездии {}
    """.format(planet_name,
               ephem.constellation(planet_obj)[1])
    print(answer_text)
    update.message.reply_text(answer_text)


def talk_to_me(update: Update, context: CallbackContext):
    """
    Обработчик входящего сообщения
    Args:
        update:  Контекст бота
        context: Внешний контекст

    Returns:
        None
    """
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(user_text)

def send_cat_picture(update: Update, context: CallbackContext):
    """
    Обработчик команды /start
    Args:
        update:  Контекст бота
        context: Внешний контекст

    Returns:
        None
    """
    cat_list = glob("images/*.jp*g")
    cat_pic = choice(cat_list)
    context.bot.send_photo(chat_id=update.message.chat.id, photo=open(cat_pic, 'rb'))

def main():
    # Получаем данные из конфига
    token = get_param("telegram_setting", "learn_atseplyaev_bot_token")
    proxy_url = get_param("telegram_setting", "proxy_url")
    proxy_username = get_param("telegram_setting", "proxy_username")
    proxy_password = get_param("telegram_setting", "proxy_password")

    PROXY = {
        'proxy_url': proxy_url,
        'urllib3_proxy_kwargs': {
            'username': proxy_username,
            'password': proxy_password,
        }
    }
    print(PROXY)

    bot = Updater(token, use_context=True, request_kwargs=PROXY)

    dp = bot.dispatcher

    dp.add_handler(CommandHandler("cat", send_cat_picture))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("planet", planet))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    bot.start_polling()
    bot.idle()


if __name__ == "__main__":
    main()

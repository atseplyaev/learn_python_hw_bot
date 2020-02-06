from utils import *

# Telegram modules
from telegram.ext import Updater, CommandHandler, \
    MessageHandler, Filters, CallbackContext

from telegram.vendor.ptb_urllib3 import urllib3
from telegram import Update, Message, ReplyKeyboardMarkup, KeyboardButton

from glob import glob
from random import choice

import ephem
from datetime import datetime
import logging

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.basicConfig(format="%(name)s - %(levelname)s - %(message)s",
                    level=logging.INFO,
                    filename="bot.log")


def start(update: Update, context: CallbackContext):
    """
    Обработчик команды /start
    Args:
        update:  Контекст бота
        context: Внешний контекст

    Returns:
        None
    """
    emo = get_user_emo(context.user_data)
    context.user_data['emo'] = emo
    text = f'Привет {emo}'
    print(text)
    update.message.reply_text(text, reply_markup=get_keyboard())


def planet(update: Update):
    """
    Обработчик команды /planet

    Args:
        update:  Контекст бота

    Returns:
        None
    """
    # Достаём название плнеты/звезды из сообщения
    user_text = update.message.text.split()
    if len(user_text) < 2:
        error_msg = "Некорректные данные.\n" \
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
                    "Список доступных планет:\n" \
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
    update.message.reply_text(answer_text, reply_markup=get_keyboard())


def talk_to_me(update: Update, context: CallbackContext):
    """
    Обработчик входящего сообщения
    Args:
        update:  Контекст бота
        context: Внешний контекст

    Returns:
        None
    """
    emo = get_user_emo(context.user_data)
    user_text = "Привет {} {}! Ты написал {}".format(update.message.chat.first_name, emo,
                                                     update.message.text)
    logging.info("User: %s, Chat id %s, Message: %s", update.message.chat.username,
                 update.message.chat.id, update.message.text)
    update.message.reply_text(user_text, reply_markup=get_keyboard())


def send_cat_picture(update: Update, context: CallbackContext):
    """
    Обработчик команды /cat и кнопки "Прислать котика"
    Args:
        update:  Контекст бота
        context: Внешний контекст

    Returns:
        None
    """
    cat_list = glob("images/*.jp*g")
    cat_pic = choice(cat_list)
    context.bot.send_photo(chat_id=update.message.chat.id, photo=open(cat_pic, 'rb'))


def change_avatar(update: Update, context: CallbackContext):
    """
    Обработчик команды "Сменить аватарку"
    Args:
        update:  Контекст бота
        context: Внешний контекст

    Returns:
        None
    """
    text = ""
    if 'emo' in context.user_data:
        text = 'Ваш старый аватар: {}.'.format(context.user_data['emo'])
        del context.user_data['emo']

    new_avatar = get_user_emo(context.user_data)
    text = f'{text} Ваш новый аватар: {new_avatar}'
    update.message.reply_text(text, reply_markup=get_keyboard())


def get_location(update: Update, context: CallbackContext):
    """
    Обработчик команды "Геолокация"
    Args:
        update:  Контекст бота
        context: Внешний контекст

    Returns:
        None
    """
    print(update.message.location)
    text = f'Готово: {get_user_emo(context.user_data)}'
    update.message.reply_text(text, reply_markup=get_keyboard())


def get_contact(update: Update, context: CallbackContext):
    """
    Обработчик команды "Контактные данные"
    Args:
        update:  Контекст бота
        context: Внешний контекст

    Returns:
        None
    """
    print(update.message.contact)
    text = f'Готово: {get_user_emo(context.user_data)}'
    update.message.reply_text(text, reply_markup=get_keyboard())


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

    dp.add_handler(MessageHandler(Filters.regex('^(Прислать котика)$'), send_cat_picture, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.regex('^(Сменить аватар)$'), change_avatar, pass_user_data=True))
    dp.add_handler(CommandHandler("cat", send_cat_picture, pass_user_data=True))
    dp.add_handler(CommandHandler("start", start, pass_user_data=True))
    dp.add_handler(CommandHandler("planet", planet, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))

    bot.start_polling()
    bot.idle()


if __name__ == "__main__":
    main()

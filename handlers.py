from glob import glob
from random import choice

import os
import ephem
from datetime import datetime
from utils import get_user_emo, get_keyboard, is_cat

from telegram.ext import CallbackContext
from telegram import Update
import logging


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


def check_user_photo(update: Update, context: CallbackContext):
    update.message.reply_text("Обрабатываю фото")
    os.makedirs("downloads", exist_ok=True)
    photo_file = context.bot.getFile(update.message.photo[-1].file_id)
    filename = os.path.join('downloads', '{}.jpg'.format(photo_file.file_id))
    print(filename)
    photo_file.download(filename)

    if is_cat(filename):
        update.message.reply_text("Обнаружен котик, добавляю в библиотеку.")
        new_filename = os.path.join('images', 'cat_{}.jpg'.format(photo_file.file_id))
        os.rename(filename, new_filename)
    else:
        os.remove(filename)
        update.message.reply_text("Тревога, котик не обнаружен.")


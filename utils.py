import os
import configparser
from random import choice
import settings
from emoji import emojize
from telegram import ReplyKeyboardMarkup, KeyboardButton
from clarifai.rest import ClarifaiApp


def get_param(section, name):
    """
    Возращает значение параметра "name" из секции "section"

    Args:
        section: имя секции
        name: имя параметра

    Returns:
        str: значение параметра.
    """
    path = os.path.expanduser("~/.mpython_conf")
    if not os.path.exists(path):
        print("{} not found".format(path))
        return

    config = configparser.ConfigParser()

    config.read(path)
    value = config.get(section, name)
    return value


def get_user_emo(user_data):
    """
    Возвращает новый или уже существующий аватар
    Args:
        user_data: Пользовательские данные

    Returns:
        None
    """
    if not ('emo' in user_data):
        user_data['emo'] = emojize(choice(settings.USER_EMOJI), use_aliases=True)

    return user_data['emo']


def get_keyboard():
    """
    Возвращает дефолтную клавиатуру.
    Returns:
        ReplyKeyboardMarkup: Дефолтная клавиатура.
    """
    contact_button = KeyboardButton('Контактные данные', request_contact=True)
    location_button = KeyboardButton('Геолокация', request_location=True)

    return ReplyKeyboardMarkup([
        ['Прислать котика', 'Сменить аватар'],
        [contact_button, location_button]
    ], resize_keyboard=True
    )


def is_cat(filename):
    image_has_cat = False
    app = ClarifaiApp(api_key=get_param("telegram_setting", "clarifai_token"))
    model = app.public_models.general_model
    response = model.predict_by_filename(filename, max_concepts=5)
    if response['status']['code'] == 10000:
        for concept in response['outputs'][0]['data']['concepts']:
            if concept['name'] == 'cat':
                image_has_cat = True
                break
    return image_has_cat

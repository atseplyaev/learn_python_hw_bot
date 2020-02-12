from utils import get_param
from handlers import *

# Telegram modules
from telegram.ext import Updater, CommandHandler, \
    MessageHandler, Filters, ConversationHandler

from telegram.vendor.ptb_urllib3 import urllib3

import logging

def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    logging.basicConfig(format="%(name)s - %(levelname)s - %(message)s",
                        level=logging.INFO,
                        filename="bot.log")

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

    form = ConversationHandler(
        entry_points=[
            MessageHandler( Filters.regex("^(Заполнить анкету)$"), form_start, pass_user_data=True)
        ],
        states={
            "name":[MessageHandler(Filters.text, form_get_name, pass_user_data=True)],
            "rating": [MessageHandler(Filters.regex("^([1-5])$"), form_rating, pass_user_data=True)],
            "comment": [MessageHandler(Filters.text, form_comment, pass_user_data=True),
                        CommandHandler("cancel", form_skip, pass_user_data=True)]
        },
        fallbacks=[MessageHandler(Filters.text | Filters.video | Filters.photo \
                                  | Filters.document, dontknow, pass_user_data=True)]
    )
    dp.add_handler(form)

    dp.add_handler(MessageHandler(Filters.regex('^(Прислать котика)$'), send_cat_picture, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.regex('^(Сменить аватар)$'), change_avatar, pass_user_data=True))
    dp.add_handler(CommandHandler("cat", send_cat_picture, pass_user_data=True))
    dp.add_handler(CommandHandler("start", start, pass_user_data=True))
    dp.add_handler(CommandHandler("planet", planet, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.photo, check_user_photo))

    bot.start_polling()
    bot.idle()


if __name__ == "__main__":
    main()

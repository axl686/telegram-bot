import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler

from handlers import *
import settings

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
)

def main():
    #learn1_axl_bot
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user, pass_user_data=True))
    dp.add_handler(CommandHandler("car", get_car_picture, pass_user_data=True))
    dp.add_handler(CommandHandler("planet", get_const_planet, pass_user_data=True))

    dp.add_handler(RegexHandler('^(Прислать тачку)$', get_car_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Сменить аватар)$', change_avatar, pass_user_data=True))

    dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    
    mybot.start_polling()
    mybot.idle()

if __main__ == "__main__":
    main()

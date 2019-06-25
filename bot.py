import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler

from handlers import *
import settings


def main():
    #learn1_axl_bot
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)

    logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO,
                        filename='bot.log'
    )

    dp = mybot.dispatcher

    anketa = ConversationHandler(
        entry_points[RegexHandler('^(Заполнить анкету)$', form_start, pass_user_data=True)],
        states{
            'name': [MessageHandler(Filters.text, form_get_name, pass_user_data=True)],
            'rating': [RegexHandler('^(1|2|3|4|5)$'), form_rating, pass_user_data=True],
            'comment': [MessageHandler(Filters.text, form_comment, pass_user_data=True),
                        CommandHandler('skip', form_skip_comment, pass_user_data=True)]
        },
        fallbacks = [MessageHandler(
            Filters.text | Filters.video | Filters.photo | Filters.document,
            dunno, 
            pass_user_data=True)
        ]
    )

    dp.add_handler(CommandHandler("start", greet_user, pass_user_data=True))
    dp.add_handler(anketa)
    dp.add_handler(CommandHandler("car", get_car_picture, pass_user_data=True))
    dp.add_handler(CommandHandler("planet", get_const_planet, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Send me a cool car)$', get_car_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Change avatar)$', change_avatar, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.photo, check_user_photo, pass_user_data=True))
    
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))
    
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler
from telegram.ext import messagequeue as mq

from handlers import *
import settings

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
)

subscribers = set()


def my_test(bot, job):
    bot.sendMessage(chat_id=840851, text='Lovely Spam! Wonderful Spam!')
    job.interval += 5
    if job.interval > 20:
        bot.sendMessage(chat_id=840851, text='By!')
        job.schedule_removal()


def main():
    #learn1_axl_bot
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)
    mybot.bot._msg_queue = mq.MessageQueue()
    mybot.bot._is_message_queued_default = True

    logging.info('Bot starting')

    dp = mybot.dispatcher

    mybot.job_queue.run_repeating(send_updates, interval=5) #interval in seconds

    anketa = ConversationHandler(
        entry_points = [RegexHandler('^(Fill the form)$', form_start, pass_user_data=True)],
        states = {
            'name': [MessageHandler(Filters.text, form_get_name, pass_user_data=True)],
            'rating': [RegexHandler('^(1|2|3|4|5)$', form_rating, pass_user_data=True)],
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
    dp.add_handler(RegexHandler('^(send me a cool car)$', get_car_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(change avatar)$', change_avatar, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data=True))
    dp.add_handler(CommandHandler('subscribe', subscribe))
    dp.add_handler(CommandHandler('unsubscribe', unsubscribe))
    dp.add_handler(CommandHandler('alarm', set_alarm, pass_args=True, pass_job_queue=True))

    dp.add_handler(MessageHandler(Filters.photo, check_user_photo, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))
    
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
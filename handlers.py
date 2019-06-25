import datetime
import logging
import os

import ephem
from emoji import emojize
from glob import glob
from random import choice

from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, ParseMode
from telegram.ext import ConversationHandler

import settings
from utils import get_user_emo, get_keyboardimport, is_car

def greet_user(bot, update, user_data):
    emo = emojize(choice(settings.USER_EMOJI), use_aliases=True)
    user_data['emo'] = emo
    text = 'Hi there {}'.format(emo)
    update.message.reply_text(text, reply_markup=get_keyboard())

def talk_to_me(bot, update, user_data):
    emo = get_user_emo(user_data)
    user_text = "Hey you, {}! Did you say about my mama: '{}'? {}".format(update.message.chat.first_name, update.message.text, emo)
    logging.info("User: %s, Chat id: %s, Message: %s", update.message.chat.username, 
                        update.message.chat.id, update.message.text)
    update.message.reply_text(user_text, reply_markup=get_keyboard())

def get_const_planet(bot, update, user_data):
    planet = split(text)[1]
    print(text)
    print(planet)
    planets_list = [name for _0, _1, name in ephem._libastro.builtin_planets()]
    
    if planet in planets_list:
      pl = ephem.planet(now.strftime("%Y/%m/%d"))
      const = ephem.constellation(pl)
      print(const)
      update.message.reply_text(const, reply_markup=get_keyboard())

def get_car_picture(bot, update, user_data):
    car_list = glob('images/*.jp*g')
    car_picture = choice(car_list)
    bot.send_photo(chat_id=update.message.chat.id, photo=open(car_picture, 'rb'), reply_markup=get_keyboard())

def change_avatar(bot, update, user_data):
    if 'emo' in user_data:
        del user_data['emo']
    emo = get_user_emo(user_data)
    update.message.reply_text('Done! {}'.format(emo), reply_markup=get_keyboard())

def get_contact(bot, update, user_data):
    print(update.message.contact)
    emo = get_user_emo(user_data)
    update.message.reply_text('Done! {}'.format(emo), reply_markup=get_keyboard())

def get_location(bot, update, user_data):
    print(update.message.location)
    emo = get_user_emo(user_data)
    update.message.reply_text('Done! {}'.format(emo), reply_markup=get_keyboard())

def check_user_photo(bot, update, user_data):
    update.message.reply_text('Checking photo')
    os.makedirs('downloads', exist_ok=True)
    photo_file = bot.getFile(update.message.photo[-1].file_id)
    filename = os.path.join('downloads', '{}.jpg'.format(photo_file.file_id))
    photo_file.download(filename)
    if is_car(filename):
        update.message.reply_text('It is a car! It was added in storage')
        new_filename = os.path.join('images', 'car_{}.jpg'.format(photo_file.file_id))
        os.rename(filename, new_filename)
    else:
        os.remove(filename)
        update.message.reply_text('Phhh... It is not a car!')

def form_start(bot, update, user_data):
    update.message.reply_text('What is your name?', 'Enter your name and surname', reply_markup=ReplyKeyboardRemove)
    return 'name'

def form_get_name(bot, update, user_data):
    user_name = update.message.text
    if len(user_name.split(' ')) != 2:
        update.message.reply_text('Please, enter your name and surname')
        return 'name'
    else:
        user_data['form_name'] = user_name
        reply_keyboard = [['1','2','3','4','5']]

        update.message.reply_text(
            'Please, rate our bot form 1 to 5',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )
        return 'rating'

def form_rating(bot, update, user_data):
    user_data['form_rating'] = update.message.text
    update.message.reply_text('Please, tell us what are you thinking about our bot')
    return 'comment'

def form_comment(bot, update, user_data):
    user_data['form_comment'] = update.message.text
    user_text = """
<b>Name Surname:</b> {form_name}
<b>Rating:</b> {form_rating}
<b>Comment:</b> {form_comment}""".format(**user_data)
    update.message.reply_text(user_text, reply_markup=get_keyboard(), parse_mode=ParseMode.HTML)

    return ConversationHandler.END

def form_skip_comment(bot, update, user_data):
    user_text = """
        <b>Name Surname:</b> {form_name}
        <b>Rating:</b> {form_rating}""".format(**user_data)
    update.message.reply_text(user_text, reply_markup=get_keyboard(), parse_mode=ParseMode.HTML)

    return ConversationHandler.END

def dunno(bot, update, user_data):
    update.message.reply_text("I do not uderstand you")

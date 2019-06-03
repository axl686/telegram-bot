import datetime
import logging

import ephem
from glob import glob
from random import choice
from utils import get_user_emo, get_keyboardimport

import settings

def greet_user(bot, update, user_data):
    emo = emojize(choice(settings.USER_EMOJI), use_aliases=True)
    user_data['emo'] = emo
    text = 'Hi there {}'.format(emo)
    update.message.reply_text(text, reply_markup=get_keyboard())

def talk_to_me(bot, update, user_data):
    emo = get_user_emo(user_data)
    user_text = "Hey, you {}! Did you say about my mama: {}?".format(update.message.chat.first_name, emo, update.message.text)
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
    update.message.reply_text('Done:'.format(emo), reply_markup=get_keyboard())

def get_contact(bot, update, user_data):
    print(update.message.contact)
    emo = get_user_emo(user_data)
    update.message.reply_text('Done:'.format(emo), reply_markup=get_keyboard())

def get_location(bot, message, user_data):
    print(update.message.location)
    emo = get_user_emo(user_data)
    update.message.reply_text('Done:'.format(emo), reply_markup=get_keyboard())

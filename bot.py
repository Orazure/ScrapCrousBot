#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging,asyncio,pytz,dateparser
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import *
from telegram.constants import ParseMode
import smtplib, ssl, email,json
from datetime import date,datetime


today = date.today()
logging.basicConfig(
    filename='/home/alexadmin/dev/botTelegram/CrousBot/users.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    """Clears the callback data cache"""

    context.bot.callback_data_cache.clear_callback_data()

    context.bot.callback_data_cache.clear_callback_queries()

    await update.effective_message.reply_text("All clear!")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
  
    with open('/home/alexadmin/dev/botTelegram/CrousBot/plats.json') as json_file:
        data = json.load(json_file)
    tmp=""
    for i in data:
        if  dateparser.parse(i['date'].removeprefix('Menu du ')).date() == datetime.strptime(today.strftime("%Y-%m-%d"),"%Y-%m-%d").date():
            date=i['date'].removeprefix('Menu du ')+"\U000025B6"+'\n'
            dishes = i['main_dishes'].split(', \n')
            for dish in dishes:
                tmp=tmp+dish+" "

    if tmp == "Menu non communiqué":
        tmp="Pas de menu disponible pour aujourd'hui"
        date=""
    if tmp == "": 
        tmp="Pas de menu disponible pour aujourd'hui"
        date=""
    text_caps = "\U0001F374"+date+tmp
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps,parse_mode=ParseMode.MARKDOWN)


async def weeks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open('/home/alexadmin/dev/botTelegram/CrousBot/plats.json') as json_file:
        data = json.load(json_file)
    tmp=""
    # send all the dishes of the week with the date
    for i in data:
        date=i['date'].removeprefix('Menu du ')+"\U000025B6"+'\n'
        dishes = i['main_dishes'].split(', \n')
        for dish in dishes:
            allDishes= dish+" "
        tmp= tmp+"\n"+"\U0001F374"+date+allDishes+"\n"
    text_caps = tmp
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps,parse_mode=ParseMode.MARKDOWN)


async def spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="You are spamming, please stop")

if __name__ == '__main__':
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # add spam function to dispatcher
    defaults = Defaults(parse_mode=ParseMode.MARKDOWN, tzinfo=pytz.timezone('Europe/Berlin'),block=True,protect_content=True)
    application = ApplicationBuilder().token("TOKEN HERE").defaults(defaults).rate_limiter(AIORateLimiter(1,10,10,60,10)).build()
    
    caps_handler = CommandHandler('menu', caps)
    weeks_handler = CommandHandler('weeks', weeks)
    
    # add handler to avoid spam
    # application.add_handler(MessageHandler(filters.Update,spam))
    application.add_handler(caps_handler)
    application.add_handler(weeks_handler)
    
    application.run_polling()



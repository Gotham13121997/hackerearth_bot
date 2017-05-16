# Copyright (C) 2016 Javier Ayres
#
# This file is part of python-telegram-bot-openshift.
#
# python-telegram-bot-openshift is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# python-telegram-bot-openshift is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with python-telegram-bot-openshift.  If not, see <http://www.gnu.org/licenses/>.

import logging
from queue import Queue
from threading import Thread
from telegram import Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Updater, Filters
import bs4 as bs
import html5lib
import urllib.request
TOKEN = '393061554:AAGBPgtWAO-JU_qALQMct4wTbA4PPZGFAP8'


def start(bot, update):
    update.message.reply_text('welcome enter the hackerearth id of the person')


def help(bot, update):
    update.message.reply_text('enter the hackerearth id and get the details of the person')


def echo(bot, update):
    s=update.message.text
    opener=urllib.request.build_opener()
    opener.addheaders=[('User-agent','Mozilla/5.0')]
    try:sauce=opener.open('https://www.hackerearth.com/@'+s)
    except urllib.error.URLError as e:
        update.message.reply_text('wrong id')
    print('used')
    soup=bs.BeautifulSoup(sauce,'html5lib')
    stri=""
    for i in soup.find_all('h1',{"class":"track-name name ellipsis"}):
        stri=stri+i.text+"\n"
    for i in soup.find_all('a',{"href":"/users/"+s+"/activity/hackerearth/#user-rating-graph"}):
        stri=stri+i.text+"\n"
    for i in soup.find_all('a',{"href":"/@"+s+"/followers/"}):
        stri=stri+i.text+"\n"
    for i in soup.find_all('a',{"href":"/@"+s+"/following/"}):
        stri=stri+i.text+"\n"
    update.message.reply_text(stri)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))

# Write your handlers here


def setup(webhook_url=None):
    """If webhook_url is not passed, run with long-polling."""
    logging.basicConfig(level=logging.WARNING)
    if webhook_url:
        bot = Bot(TOKEN)
        update_queue = Queue()
        dp = Dispatcher(bot, update_queue)
    else:
        updater = Updater(TOKEN)
        bot = updater.bot
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("help", help))

        # on noncommand i.e message - echo the message on Telegram
        dp.add_handler(MessageHandler(Filters.text, echo))

        # log all errors
        dp.add_error_handler(error)
    # Add your handlers here
    if webhook_url:
        bot.set_webhook(webhook_url=webhook_url)
        thread = Thread(target=dp.start, name='dispatcher')
        thread.start()
        return update_queue, bot
    else:
        bot.set_webhook()  # Delete webhook
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    setup()

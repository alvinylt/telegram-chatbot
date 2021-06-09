import telegram
import telegram.ext
import re
from random import randint
import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

API_KEY = ## <Telegram API key here>
updater = telegram.ext.Updater(API_KEY)
dispatcher = updater.dispatcher

WELCOME = 0
QUESTION = 1
CANCEL = 2
CORRECT = 3

def start(update_obj, context):
    update_obj.message.reply_text("Hello there, do you want to answer a question? (Yes/No)",
        reply_markup=telegram.ReplyKeyboardMarkup([['Yes', 'No']], one_time_keyboard=True)
    )
    return WELCOME

def randomize_numbers(update_obj, context):
    context.user_data['rand_x'], context.user_data['rand_y'] = randint(0,1000), randint(0,1000)
    update_obj.message.reply_text(f"Calculate {context.user_data['rand_x']}+{context.user_data['rand_y']}")

def welcome(update_obj, context):
    if update_obj.message.text.lower() in ['yes', 'y']:
        randomize_numbers(update_obj, context)
        return QUESTION
    else:
        return CANCEL

def question(update_obj, context):
    solution = int(context.user_data['rand_x']) + int(context.user_data['rand_y'])
    if solution == int(update_obj.message.text):
        update_obj.message.reply_text("Correct answer!")
        update_obj.message.reply_text("Was this tutorial helpful to you?")
        return CORRECT
    else:
        update_obj.message.reply_text("Wrong answer :'(")
        randomize_numbers(update_obj, context)
        return QUESTION
    
def correct(update_obj, context):
    if update_obj.message.text.lower() in ['yes', 'y']:
        update_obj.message.reply_text("Glad it was useful! ^^")
    else:
        update_obj.message.reply_text("You must be a programming wizard already!")
    first_name = update_obj.message.from_user['first_name']
    update_obj.message.reply_text(f"See you {first_name}!, bye")
    return telegram.ext.ConversationHandler.END

def cancel(update_obj, context):
    first_name = update_obj.message.from_user['first_name']
    update_obj.message.reply_text(
        f"Okay, no queston for you then. Take care, {first_name}!", reply_markup=telegram.ReplyKeyboardRemove()
    )
    return telegram.ext.ConversationHandler.END

yes_no_regex = re.compile(r'^(yes|no|y|n)$', re.IGNORECASE)
handler = telegram.ext.ConversationHandler(
    entry_points=[telegram.ext.CommandHandler('start', start)],
    states = {
        WELCOME: [telegram.ext.MessageHandler(telegram.ext.Filters.regex(yes_no_regex), welcome)],
        QUESTION: [telegram.ext.MessageHandler(telegram.ext.Filters.regex(r'^\d+$'), question)],
        CANCEL: [telegram.ext.MessageHandler(telegram.ext.Filters.regex(yes_no_regex), cancel)],
        CORRECT: [telegram.ext.MessageHandler(telegram.ext.Filters.regex(yes_no_regex), correct)],
    },
    fallbacks=[telegram.ext.CommandHandler('cancel', cancel)],
    )

dispatcher.add_handler(handler)

updater.start_polling()
updater.idle()

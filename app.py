import telebot
from config import TOKEN, keys
from extensions import CurrencyExchanger, ConversionException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['photo'])
def function_name(message):
    bot.reply_to(message, f"Nice photo, is it You?")


@bot.message_handler(content_types=['voice', ])
def repeat(message: telebot.types.Message):
    bot.send_message(message.chat.id, "What a nice voice!")  # sending message
    bot.reply_to(message, "Are You kidding?")  # replaying to the message
    bot.send_message(message.chat.id, 'Would you like to exchange some currency? Enter /help or /start to start')


@bot.message_handler(content_types=['sticker'])
def function_name(message):
    bot.send_message(message.chat.id, "What a funny pic! I like it")
    bot.send_message(message.chat.id, "Would you like to exchange some currency? Enter /help or /start to start")


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'To start the currency exchange, please enter the command for te bot in the following format: \n ' \
           '<currency name>\<requested currency name>\<currency amount>\n' \
           'To see the list of available currency, enter /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Available currencies are:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConversionException('Request–s format is not correct - 3 values should be entered')
        quote, base, amount = values
        total_base = round(CurrencyExchanger.convert(quote, base, amount)*float(amount),2)
    except ConversionException as e:
        bot.reply_to(message, f'User-s mistake\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Not able to complete this request\n{e}')
    else:
        text = f'Price of {amount} {quote} in {base}s - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(non_stop=True)

import telebot
from bot_config import TOKEN, KEYS
from extensions import APIException, Converter

bot = telebot.TeleBot(TOKEN)

# обработка команд start, help
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Вас приветствует бот-конвертер валют!\n\nЧтобы увидеть список всех доступных валют, \
введите команду\n/values\n\nЧтобы выполнить конвертацию, введите команду в следующем формате:\n<имя валюты> \
<в какую валюту перевести> <количество переводимой валюты>\nЕсли количество валюты не целое, в качестве разделителя \
целой и дробной частей используйте точку.\n\nЧтобы получить инструкцию еще раз, введите команду\n/help'
    bot.reply_to(message, text)

# обработка команды values
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in KEYS.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

# обработка сообщения с валютами
@bot.message_handler(content_types=['text'])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Введите команду или 3 параметра')

        base, quote, amount = values
        price = Converter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'Результат конвертации\n {amount} {base} = {price} {quote}'
        bot.send_message(message.chat.id, text)

bot.polling()

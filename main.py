from telebot import TeleBot
from telebot.types import Message
from decouple import config
from settings import CURRRENCIES
from extensions import CurrensyConverter, APIException

bot = TeleBot(token=config("BOT_TOKEN", default="NOT_FOUND"))
converter = CurrensyConverter()


@bot.message_handler(commands=["start"])
def start_message(message: Message):
  """Сообщение с текстом приветствия"""
  bot.send_message(message.chat.id, "Привет! Я бот, предназначенный для перевода валют")
  help_message(message)
  

@bot.message_handler(commands=["help"])
def help_message(message: Message):
  """Сообщение с текстом помощи"""
  msg_text = """Чтобы воспользоваться функционалом бота, нужно ввести одну из комманд:
/help    -  Выводит сообщение с допустимыми командами
/values  -  Выводит список всех доступных для перевода валют
'base' 'quote' 'amount' - Переводит валюту.
base - символ валюты, цену на которую нужно узнать;
quote - сивмол валюты, цену в которой нужно узнать;
amount - количество переводимой валюты
Символы валют можно узнать с помощью команды /values"""
  bot.send_message(message.chat.id, msg_text)


@bot.message_handler(commands=["values"])
def get_values_message(message: Message):
    """Выводит все доступные валюты"""
    all_currencies = "\n".join([" - ".join(i) for i in CURRRENCIES.items()])
    msg_text = "Вот все доступные валюты. Значение через тире - символ, который надо использовать в запросе на перевод валют\n"
    bot.send_message(message.chat.id, msg_text + all_currencies)


@bot.message_handler(content_types=['text'])
def convert_message(message: Message):
    """Осуществляет перевод валюты и выводит результат"""
    try:
        args = message.text.split()
        if len(args) != 3:
            raise APIException("Количество аргументов не равно трем!") 
        base, quote, amount = args
        value = converter.get_price(base, quote, amount)
    except APIException as apiexc:
       bot.reply_to(message, apiexc)
    except Exception as e:
       bot.reply_to(message, f"Произошла непредвиденная ошибка: {e}")
    else:
       bot.reply_to(message, f"Цена {base} в {quote} в количестве {amount} равна {value}")


if __name__ == "__main__":
    bot.polling()

import telebot
import random
import conf
from pymorphy2 import MorphAnalyzer
from nltk import word_tokenize
import kto_ubil_marka

bot = telebot.TeleBot(conf.TOKEN)
morph = MorphAnalyzer()
bot.remove_webhook()

good_morning_messages = {
    'en': [
        "Good morning! Have a bright and fulfilling day!",
        "Good morning! May this day be filled with joy and success!",
        "Morning is the start of new possibilities. Wishing you the best of this day!",
        "I wish you a wonderful day!"
    ],
    'ru': [
        "Доброе утро! Пусть этот день будет самым лучшим!",
        "Утро - время для новых начинаний. Пусть этот день будет ярким и удачным!",
        "С добрым утром! Желаю улыбок и хорошего настроения!",
        "Желаю самого распрекрасного дня!"
    ],
    'de': [
        "Guten Morgen! Möge dieser Tag der Beste sein!",
        "Der Morgen ist die Zeit für neue Anfänge. Lassen Sie den Tag hell und erfolgreich sein!",
        "Guten Morgen! Ich wünsche ein Lächeln und gute Laune!",
        "Ich wünsche dir einen schönen Tag!"
    ],
    'it': [
        "Buongiorno! Possa questo giorno essere il migliore!",
        "La mattina è un momento per nuovi inizi. Possa la giornata essere luminosa e di successo!",
        "Buongiorno! Ti auguro sorrisi e buon umore!",
        "Ti auguro una bella giornata!"
    ]
}

def lemmatize_sentence(sentence):
    token_words = word_tokenize(sentence)
    lemmatized_words = [morph.parse(word)[0].normal_form for word in token_words]
    lemmatized_sentence = ' '.join(lemmatized_words)
    return lemmatized_sentence

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "\t Здравствуйте! Hallo! Ciao! Hello! "
                                      "\n\n\t Это бот, который будет генерировать фразы про все хорошее для успокоения нервов и желать вам прекрасного дня на "
                                      "разных языках! А для русского и английского даже сделает морфологический разбор каждого слова"
                                      " и напишет начальные формы) "
                                      "\n\n\t ✍️✍️Введите команду /language для выбора языка пожеланий (их ограниченное количество)." 
                                      "\n\n\t ✍️✍️ Введите команду /new для того, чтобы сгенерировать предложение про все хорошее и доброе на русском языке.")

@bot.message_handler(commands=['language'])
def good_morning(message):
    language_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    language_keyboard.add('🇬🇧 English', '🇷🇺 Русский', '🇩🇪 Deutsch', '🇮🇹 Italian')
    bot.send_message(message.chat.id, "Выберите язык:", reply_markup=language_keyboard)

@bot.message_handler(func=lambda message: message.text == '🇬🇧 English')
def send_english_message(message):
    morning_message = random.choice(good_morning_messages['en'])
    bot.send_message(message.chat.id, morning_message)
    lemmatized_message = lemmatize_sentence(morning_message)
    bot.send_message(message.chat.id, lemmatized_message)
    words = morning_message.split()
    for word in words:
        parsed_word = morph.parse(word)[0]
        analyzed_result = f'Слово: {word}\n' \
                          f'Начальная форма: {parsed_word.normal_form}\n' \
                          f'Часть речи: {parsed_word.tag.POS}\n' \
                          f'Падеж: {parsed_word.tag.case}\n' \
                          f'Род: {parsed_word.tag.gender}\n' \
                          f'Число: {parsed_word.tag.number}\n'
        bot.send_message(message.chat.id, analyzed_result)

@bot.message_handler(func=lambda message: message.text == '🇷🇺 Русский')
def send_russian_message(message):
    morning_message = random.choice(good_morning_messages['ru'])
    bot.send_message(message.chat.id, morning_message)
    lemmatized_message = lemmatize_sentence(morning_message)
    bot.send_message(message.chat.id, lemmatized_message)
    words = morning_message.split()
    for word in words:
        parsed_word = morph.parse(word)[0]
        analyzed_result = f'Слово: {word}\n' \
                          f'Начальная форма: {parsed_word.normal_form}\n' \
                          f'Часть речи: {parsed_word.tag.POS}\n' \
                          f'Падеж: {parsed_word.tag.case}\n' \
                          f'Род: {parsed_word.tag.gender}\n' \
                          f'Число: {parsed_word.tag.number}\n'
        bot.send_message(message.chat.id, analyzed_result)

@bot.message_handler(func=lambda message: message.text == '🇮🇹 Italian')
def send_russian_message(message):
    morning_message = random.choice(good_morning_messages['it'])
    bot.send_message(message.chat.id, morning_message)


@bot.message_handler(func=lambda message: message.text == '🇩🇪 Deutsch')
def send_russian_message(message):
    morning_message = random.choice(good_morning_messages['de'])
    bot.send_message(message.chat.id, morning_message)

@bot.message_handler(commands=['new'])
def send_len(message):
    bot.send_message(message.chat.id, kto_ubil_marka.m.make_short_sentence(100))

if __name__ == '__main__':
    bot.polling(none_stop=True)
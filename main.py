import telebot
from googletrans import Translator

bot=telebot.TeleBot("6088967906:AAE1NoPKyPN1f8kbMe_u9IYmRGFp13hwpvg")
translator=Translator()

@bot.message_handler(commands=['translate'])
def start_translate(message):
    bot.send_message(message.chat.id,"چه متنی را می خواهید ترجمه کنید؟")
    bot.register_next_step_handler(message,translate_text)

def translate_text(message):
    source_text=message.text
    lang_list={'فارسی':'fa','انگلیسی':'en','اسپانیایی':'es','فرانسوی':'fr'}
    lang_key=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    lang_key.add(*(telebot.types.KeyboardButton(key) for key in lang_list.keys()))

    bot.send_message(message.chat.id,"زبان مبدا را انتخاب کنید؟",reply_markup=lang_key)

    @bot.message_handler(func=lambda message:message.text in lang_list.keys())
    def define_target_lang(message):
        source_lang=lang_list[message.text]
        bot.send_message(message.chat.id,"زبان مقصد را انتخاب کنید",reply_markup=lang_key)

        @bot.message_handler(func=lambda message: message.text in lang_list.keys())
        def get_translated_text(message):
            target_lang=lang_list[message.text]
            translation=translator.translate(source_text,src=source_lang,dest=target_lang)
            bot.send_message(message.chat.id,f"متن ورودی:<b>{source_text}</b>\n متن ترجمه شده: <b>{translation.text}</b>", parse_mode='HTML')
            bot.remove_message_handler(define_target_lang)
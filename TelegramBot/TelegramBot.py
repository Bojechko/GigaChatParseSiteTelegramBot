import os
from time import sleep

import telebot
from dotenv import load_dotenv


class TelegramBot:

    def __init__(self, giga_chat_requester):
        """
        Происходит создание экземпляра гигачатреквестера, а так же создание бота.

        :param giga_chat_requester: экземпляр класса GigaChatRequester
        """
        load_dotenv()

        self.giga = giga_chat_requester

        self.bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))

        print('init done')


        @self.bot.message_handler(content_types=['audio',
                                            'video',
                                            'document',
                                            'photo',
                                            'sticker',
                                            'voice',
                                            'location',
                                            'contact'])

        def not_text(message):
            """
            Проверка, что только текст пришел из бота
            """
            user_id = message.chat.id
            self.bot.send_message(user_id, 'Я работаю только с текстовыми сообщениями!')



        @self.bot.message_handler(content_types=['text'])
        def handle_text_message(message):
            """
            Обработка сообщений
            :param message: сообщение
            """
            user_id = message.chat.id

            response = self.giga.make_request(message.text)

            self.bot.send_message(user_id, response)

            sleep(2)


    def run(self):
        self.bot.polling(none_stop=True)

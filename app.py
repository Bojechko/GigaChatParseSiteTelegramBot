from GigaChat.GigaChatRequester import GigaChatRequester
from PreprocessingService.EmbeddingCreator import EmbeddingCreator
from PreprocessingService.UrlsLoader import UrlsLoader
from TelegramBot.TelegramBot import TelegramBot
from prompt import PROMPT

"""Загрузка данных из ссылок"""
urls_loader = UrlsLoader()
urls_loader.vectorize_data(500, 100)

vector_db_loader = EmbeddingCreator(urls_loader.get_split_data(), model_name="deepvk/USER-bge-m3")
retriever = vector_db_loader.retriever()

giga = GigaChatRequester(retriever, PROMPT)

bot = TelegramBot(giga)
bot.run()
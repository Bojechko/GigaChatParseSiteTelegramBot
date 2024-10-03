from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader

from config import URLS


class UrlsLoader:
    """Загрузчик данных из ссылок"""

    def __init__(self):
        self.split_data = None
        self.loader = WebBaseLoader(URLS)


    def vectorize_data(self, chunk_size, chunk_overlap):
        """
        Бъем данные на чанки из ссылок, предварительно загрузив их. Разбитые данные хранятся в self.split_data

        :param chunk_size:максимальное количество символов в одном чанке
        :param chunk_overlap: количество символов, которые совпадают между двумя соседними чанками.
        """
        data = self.loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,
                                                       chunk_overlap=chunk_overlap)
        self.split_data = text_splitter.split_documents(data)


    def get_split_data(self):
        """Получить разбитые данные"""
        return self.split_data


if __name__ == "__main__":
    urls_loader = UrlsLoader()
    urls_loader.vectorize_data(500, 100)


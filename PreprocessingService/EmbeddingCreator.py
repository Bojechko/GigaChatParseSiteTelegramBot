from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


class EmbeddingCreator:


    def __init__(self, split_data, model_name,
                 model_kwargs={'device': 'cpu'},
                 encode_kwargs={'normalize_embeddings': False}):
        """
        Создаем векторное хранилище и эмбеддинг.

        :param split_data: Разбитые данные из UrlsLoader
        :param model_name: имя модели, которую используем
        :param model_kwargs: https://api.python.langchain.com/en/latest/embeddings/langchain_community.embeddings.huggingface.HuggingFaceEmbeddings.html
        :param encode_kwargs: https://api.python.langchain.com/en/latest/embeddings/langchain_community.embeddings.huggingface.HuggingFaceEmbeddings.html
        """

        self.embedding = HuggingFaceEmbeddings(model_name=model_name,
                                               model_kwargs=model_kwargs,
                                               encode_kwargs=encode_kwargs)

        self.vector_store = FAISS.from_documents(split_data, embedding=self.embedding)

        self.embedding_retriever = None


    def retriever(self, extraction_options=None):
        """
        Создаем ретривер

        :param extraction_options: количество фрагментов наиболее похожих по смыслу
        :return: embedding_retriever
        """
        if extraction_options is None:
            extraction_options = {"k": 5}
            self.embedding_retriever = self.vector_store.as_retriever(search_kwargs=extraction_options)
            return self.embedding_retriever
        else:
            raise ("Write extraction options. EXEMPLE: {'k': 5}")

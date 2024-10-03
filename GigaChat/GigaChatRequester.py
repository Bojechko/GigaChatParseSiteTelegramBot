import os

from dotenv import load_dotenv
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chat_models.gigachat import GigaChat
from langchain_core.prompts import ChatPromptTemplate

from PreprocessingService.EmbeddingCreator import EmbeddingCreator



class GigaChatRequester:

    def __init__(self, retriever, prompt):
        """
        Инициализация гигачата. Задаем модель, токен. А так же промпт

        :param retriever: ретривер
        :param prompt: Промпт, если не устраивает дефолтный. В виде строки.
        """
        load_dotenv()
        self.llm = GigaChat(credentials=os.getenv('SBER_AUTH'),
                      model='GigaChat-Pro:latest',
                       verify_ssl_certs=False,
                       profanity_check=False)


        self.prompt=ChatPromptTemplate.from_template(prompt)

        document_chain = create_stuff_documents_chain(
            llm=self.llm,
            prompt=self.prompt
        )
        self.retrieval_chain = create_retrieval_chain(retriever, document_chain)


    def make_request(self, input_text):
        """
        Обращение к гигачату с запросом
        :param input_text: текст запроса
        :return: ответ от гигачата в виде строки
        """
        data = self.retrieval_chain.invoke(
            {'input': input_text}
        )

        print(data)

        return data.get('answer', 'Ответ не найден')


if __name__ == '__main__':
    from PreprocessingService.UrlsLoader import UrlsLoader
    from prompt import PROMPT

    urls_loader = UrlsLoader()
    urls_loader.vectorize_data(500, 100)
    vector_db_loader = EmbeddingCreator(urls_loader.get_split_data(), model_name="deepvk/USER-bge-m3")
    retr = vector_db_loader.retriever()
    giga = GigaChatRequester(retr, PROMPT)

    giga.make_request('Что вы можете сделать для ритейлеров? Приведи несколько примеров')






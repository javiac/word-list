from dependency_injector import containers, providers
import pymongo
from src.contexts.words.word_service import WordService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    database_client = providers.Singleton(pymongo.MongoClient, "localhost", 27017)

    word_service = providers.Factory(
        WordService,
        db_client=database_client,
        db_name='plytix'
    )

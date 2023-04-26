from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.settings.environment import Environment
from src.patterns.singleton import Singleton


class PostgresDatabase(metaclass=Singleton):
    def __init__(self):
        self.env = Environment()
        self.__engine = self.__create_database_engine()
        self.session = None

    def __create_database_engine(self):
        engine = create_engine(self.env.DATABASE_CONNECTION_STRING)
        return engine

    def get_engine(self):
        return self.__engine

    def get_base(self):
        return self.__base

    def __enter__(self):
        session_maker = sessionmaker(bind=self.__engine)
        self.session = session_maker()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        self.session = None

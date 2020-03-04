from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import Session, exc


class Connection:
    session = None
    engine = None

    @staticmethod
    def get_engine():
        if Connection.engine is None:
            return create_engine('mysql+pymysql://root@localhost:3306/testdb', echo=False)
        return Connection.engine

    @staticmethod
    def get_session():
        if Connection.session is None:
            return Session(bind=Connection.get_engine(), expire_on_commit=True)
        return Connection.session

    def __init__(self):
        Connection.session = Connection.get_session()


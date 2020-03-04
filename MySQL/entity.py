from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Employee(Base):
    def __init__(self, id, name):
        self.id = id
        self.name = name

    __tablename__ = "employees"
    id = Column(Integer, primary_key=True)
    name = Column(String)





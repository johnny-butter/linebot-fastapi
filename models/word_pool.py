from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class WordPool(Base):

    __tablename__ = 'py_word_pool'

    id = Column(Integer, primary_key=True)
    word = Column(String(60), nullable=False)

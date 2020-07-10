from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Keywords(Base):

    __tablename__ = 'py_keywords'

    id = Column(Integer, primary_key=True)
    keyword = Column(String(60), nullable=False)
    response_cls = Column(String(60), nullable=False)

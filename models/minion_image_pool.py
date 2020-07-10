from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class MinionImagePool(Base):

    __tablename__ = 'py_minion_image_pool'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    size = Column(String(30), nullable=False)
    url = Column(Text, nullable=False)

from sqlalchemy import Column, String, Integer
from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class WeatherLocationMap(Base):

    __tablename__ = 'py_weather_location_map'

    id = Column(Integer, primary_key=True)
    location = Column(String(20), nullable=False)
    weather_api_key = Column(String(20), nullable=False)

    __table_args__ = (
        UniqueConstraint('location', 'weather_api_key'),
    )

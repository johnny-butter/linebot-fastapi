from .keywords import Keywords
from .word_pool import WordPool
from .minion_image_pool import MinionImagePool
from .weather_location_map import WeatherLocationMap

from config import settings

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(settings.DB_URL, pool_size=8, max_overflow=0, echo=True)
db_session = sessionmaker(bind=engine, autoflush=False)

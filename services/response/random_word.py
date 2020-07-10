from services.response.base import Base
from linebot.models import TextSendMessage
from models import WordPool
from sqlalchemy.sql.expression import func


class RandomWord(Base):

    def response(self):
        return TextSendMessage(text=self._get_random_word())

    def _get_random_word(self):
        return self.db_session() \
            .query(WordPool) \
            .order_by(func.random()) \
            .first().word

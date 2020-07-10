from random import randint
from services.response.base import Base
from linebot.models import StickerMessage


class RandomLineSticker(Base):

    def response(self):
        return StickerMessage(
            package_id='11537',
            sticker_id=self._get_random_line_sticker()
        )

    def _get_random_line_sticker(self):
        return randint(52002734, 52002773)

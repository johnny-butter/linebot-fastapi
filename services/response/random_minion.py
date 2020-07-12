from sqlalchemy.sql.expression import func
from models import MinionImagePool
from services.response.base import Base
from linebot.models import ImageSendMessage


class RandomMinion(Base):

    def __init__(self, *args, **kwargs):
        super(RandomMinion, self).__init__(**kwargs)
        self.random_image_name = self._get_random_image_name()

    def response(self):
        image_url_dict = self._get_image_url()

        return ImageSendMessage(
            original_content_url=image_url_dict['origin'],
            preview_image_url=image_url_dict['preview']
        )

    def _get_random_image_name(self):
        return self.db_session(). \
            query(MinionImagePool). \
            filter(MinionImagePool.size == 'preview'). \
            order_by(func.random()). \
            first().name

    def _get_image_url(self):
        image_urls = self.db_session(). \
            query(MinionImagePool.size, MinionImagePool.url). \
            filter(MinionImagePool.name == self.random_image_name). \
            all()

        image_url_dict = {}
        for image_size, image_url in image_urls:
            image_url_dict[image_size] = image_url

        return image_url_dict


if __name__ == '__main__':
    RandomMinion().response()

import requests
import pytz
from services.response.base import Base
from linebot.models import TextSendMessage
from datetime import datetime, timedelta
from config import settings
from models import WeatherLocationMap


class WeatherReport(Base):

    def __init__(self, *args, **kwargs):
        super(WeatherReport, self).__init__(**kwargs)
        tw = pytz.timezone('Asia/Taipei')
        self.current_time = datetime.now().astimezone(tw)

    def response(self):
        return TextSendMessage(text=self._get_weather_report())

    def _get_weather_report(self):
        wlm = self._get_weather_location_map()

        if not wlm:
            return 'The location is not supported'

        query_params = {
            'Authorization': settings.WEATHER_OPEN_API_AUTH_CODE,
            'format': 'json',
            'elementName': 'WeatherDescription',
            'locationName': wlm.location,
            'timeFrom': self._get_current_time(),
            'timeTo': self._get_current_time(plus_hours=3),
        }

        resp = requests.get(
            f'https://opendata.cwb.gov.tw/api/v1/rest/datastore/{wlm.weather_api_key}',
            params=query_params
        )

        if not resp.ok:
            return 'Can not get weather report'

        return self._parse_weather_data(resp.json())

    def _get_weather_location_map(self):
        if not self.line_event_message:
            return None

        location = self.line_event_message.split('天氣')[0]

        weather_location_map = self.db_session(). \
            query(WeatherLocationMap). \
            filter(WeatherLocationMap.location == location). \
            first()

        return weather_location_map

    def _get_current_time(self, plus_hours=0):
        current_time = self.current_time

        if plus_hours > 0:
            current_time += timedelta(hours=plus_hours)

        return current_time.strftime('%Y-%m-%dT%H:%M:%S')

    def _parse_weather_data(self, data):
        weather_dict = data['records']['locations'][0]

        weather_location = f'{weather_dict["location"][0]["locationName"]}@{weather_dict["locationsName"]}'
        weather_desc = weather_dict['location'][0]['weatherElement'][0]['time'][0]['elementValue'][0]['value']

        return f'{weather_location}:\n{weather_desc}'


if __name__ == '__main__':
    WeatherReport(line_event_message='板橋區天氣').response()

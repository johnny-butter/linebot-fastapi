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
            'elementName': 'AT,WeatherDescription',
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

        return Weather(resp.json()).report

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


class Weather:
    def __init__(self, raw_data):
        self.city_data = raw_data['records']['locations'][0]
        self.district_data = self.city_data['location'][0]
        for element in self.district_data['weatherElement']:
            if element['elementName'] == 'AT':
                self.at_element = element
            elif element['elementName'] == 'WeatherDescription':
                self.weather_desc_element = element

    @property
    def report(self):
        report = [
            f'⚓{self.weather_location}',
            f'⌚{self.report_start_time}~{self.report_end_time}',
            f'ℹ️{self.weather_desc}體感溫度攝氏{self.weather_at}度。',
        ]

        return '\n'.join(report)

    @property
    def weather_location(self):
        return f"{self.district_data['locationName']}@{self.city_data['locationsName']}"

    @property
    def weather_at(self):
        return self.at_element['time'][0]['elementValue'][0]['value']

    @property
    def weather_desc(self):
        return self.weather_desc_element['time'][0]['elementValue'][0]['value']

    @property
    def report_start_time(self):
        start_time = datetime.strptime(self.weather_desc_element['time'][0]['startTime'], '%Y-%m-%d %H:%M:%S')
        return start_time.strftime('(%m-%d)%H:%M')

    @property
    def report_end_time(self):
        end_time = datetime.strptime(self.weather_desc_element['time'][0]['endTime'], '%Y-%m-%d %H:%M:%S')
        return end_time.strftime('(%m-%d)%H:%M')


if __name__ == '__main__':
    WeatherReport(line_event_message='板橋區天氣').response()

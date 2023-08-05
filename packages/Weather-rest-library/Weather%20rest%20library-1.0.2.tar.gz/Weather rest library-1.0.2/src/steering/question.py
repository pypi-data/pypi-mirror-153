
from src.rest_requests.rest_request import Request as req
from src.steering.answer_parser import  CurrentWeatherAnswerParser, SearchWeatherAnswerParser,FutureWeatherAnswerParser
import json
class Question():
    def __init__(self):
        self.request=req()
        self.current_weather_parser = CurrentWeatherAnswerParser()
        self.search_weather_parser = SearchWeatherAnswerParser()
        self.future_weather_parser = FutureWeatherAnswerParser()

    def get_actual_weather(self):
        temp = self.request.get_current_weather().text
        temp = temp[5: -1]
        self.current_weather_parser.parse_current_weather(json.loads(temp))
        return self.current_weather_parser
    def get_search_weather_data(self):
        temp = self.request.get_search_weather_data().text
        self.search_weather_parser.parse_search_weather_data(json.loads(temp))
        return self.search_weather_parser
    def get_future_weather(self):
        temp = self.request.get_future_weather().text
        self.future_weather_parser.parse_future_weather(json.loads(temp))
        return self.future_weather_parser


if __name__=="__main__":
    q = Question()
    t1 = q.get_data(1)
    t2 = q.get_data(2)
    t3 = q.get_data(3)
    print(t1.temp)
    print(t2.temp)
    print(t3.temp)

from src.rest_requests.rest_request_executor import RequestExecutor as re

class Request():
    def __init__(self):
        self.request_executor =re()
    def get_current_weather(self):
        url = "https://community-open-weather-map.p.rapidapi.com/weather"

        querystring = {"q": "London,uk", "lat": "0", "lon": "0", "callback": "test", "id": "2172797", "lang": "null",
                       "units": "imperial", "mode": "xml"}

        headers = {
            "X-RapidAPI-Host": "community-open-weather-map.p.rapidapi.com",
            "X-RapidAPI-Key": "ec4350f46cmshe3414fc29210337p1e4ac7jsnff32e507d3ab"
        }
        response = self.request_executor.execute_query(url,headers,querystring)
        return response
    def get_search_weather_data(self):
        url = "https://community-open-weather-map.p.rapidapi.com/find"

        querystring = {"q": "london", "cnt": "2", "mode": "null", "lon": "0", "type": "link, accurate", "lat": "0",
                       "units": "imperial, metric"}

        headers = {
            "X-RapidAPI-Host": "community-open-weather-map.p.rapidapi.com",
            "X-RapidAPI-Key": "ec4350f46cmshe3414fc29210337p1e4ac7jsnff32e507d3ab"
        }
        response = self.request_executor.execute_query(url,headers,querystring)
        return response
    def get_future_weather(self):
        url = "https://community-open-weather-map.p.rapidapi.com/forecast/daily"

        querystring = {"q": "san francisco,us", "lat": "35", "lon": "139", "cnt": "10", "units": "metric or imperial"}

        headers = {
            "X-RapidAPI-Host": "community-open-weather-map.p.rapidapi.com",
            "X-RapidAPI-Key": "ec4350f46cmshe3414fc29210337p1e4ac7jsnff32e507d3ab"
        }
        response = self.request_executor.execute_query(url,headers,querystring)
        return response

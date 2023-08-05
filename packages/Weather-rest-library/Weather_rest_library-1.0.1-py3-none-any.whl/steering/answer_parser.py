

class CurrentWeatherAnswerParser():
    def __init__(self):
        self.temperature = None
        self.temp = None

    def parse_current_weather(self,answer):
        self.temp = answer
        self.temperature = self.temp.get("main").get("temp")

class SearchWeatherAnswerParser():
    def __init__(self):
        self.temp= None
        self.temperature = None
        self. temperature_max = None
        self.temperature_min = None

    def parse_search_weather_data(self,answer):
        self.temp = answer
        self.temperature = (self.temp.get("list")[0]).get("main").get("temp")
        self.temperature_min = (self.temp.get("list")[0]).get("main").get("temp_min")
        self.temperature_max = (self.temp.get("list")[0]).get("main").get("temp_max")

class FutureWeatherAnswerParser():
    def __init__(self):
        self.temp = None
        self.temperature_list = []

    def parse_future_weather(self,answer):
        self.temp = answer
        list = self.temp.get("list")
        size = len(list)
        for x in range(size):
            self.temperature_list.append(list[x].get("temp").get("day"))

if __name__=="__main__":
    pass

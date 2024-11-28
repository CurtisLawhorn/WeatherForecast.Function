import requests

class WeatherForecast:
    def __init__(self, city):
        self.City = city.title()

    def GetForecast(self):
        API_KEY = ""
        url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={self.City}&aqi=no"
        response = requests.get(url)
        data = response.json()

        temp = round(data["current"]["temp_f"])
        feelsLike = round(data["current"]["feelslike_f"])
        tempScale = "Fahrenheit"
        wind = round(data["current"]["wind_mph"])
        windGust = round(data["current"]["gust_mph"])
        windDir = data["current"]["wind_dir"]
        windScale = "mph"
        condition = data["current"]["condition"]["text"]
        updated = data["current"]["last_updated"]
        description = f"The weather in {self.City} as of {updated} is {condition.lower()} and {temp} degrees {tempScale} with a feels like of {feelsLike} degress {tempScale}."

        data = {
            "city": self.City,
            "temp": temp,
            "tempFeel": feelsLike,
            "tempScale": tempScale,
            "wind": wind,
            "windScale": windScale,
            "windGust": windGust,
            "windDir": windDir,
            "condition": condition,
            "updated": updated,
            "description": description
        }

        return data
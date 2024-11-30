import json
from weather_forecast import WeatherForecast

class WeatherForecasts:
    def __init__(self):
        self.Forecasts = []

    def AddForecast(self, city):
        self.Forecasts.append(city)

    def DisplayCities(self):
        for forecast in self.Forecasts:
            print(forecast.City)
        print ("----------")

    def DisplayForecasts(self):
        for forecast in self.Forecasts:
            print(forecast.GetForecast())
        print ("----------")

def lambda_handler(event, context):
    weatherForecast = WeatherForecast("Clive")
    forecast = weatherForecast.GetForecast()
    return {
        'statusCode': 200,
        'body': json.dumps(forecast)
    }

def main():
    weatherForecasts = WeatherForecasts()
    weatherForecasts.AddForecast(WeatherForecast("Clive"))
    weatherForecasts.AddForecast(WeatherForecast("Ames"))
    weatherForecasts.AddForecast(WeatherForecast("Orlando"))
    weatherForecasts.AddForecast(WeatherForecast("London"))
    
    weatherForecasts.DisplayCities()
    weatherForecasts.DisplayForecasts()

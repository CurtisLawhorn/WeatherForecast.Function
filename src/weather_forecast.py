import requests
import json
#import os
#from dotenv import find_dotenv, load_dotenv
import boto3
from botocore.exceptions import ClientError

#dotenv_path = find_dotenv()
#load_dotenv(dotenv_path)
#API_KEY = os.getenv("API_KEY")

def get_api_key():
    secret_name = "Weather-API"
    region_name = "us-east-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response["SecretString"]
    data = json.loads(secret)
    return data["API_KEY"]

class WeatherForecast:
    def __init__(self, city):
        self.City = city.title()

    def GetForecast(self):
        API_KEY = get_api_key()
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
        description = f"The weather in {self.City} as of {updated} is {condition.lower()} and {temp} degrees {tempScale} with a feels like of {feelsLike} degrees {tempScale}."

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
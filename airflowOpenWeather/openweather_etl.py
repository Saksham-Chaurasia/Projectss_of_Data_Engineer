import json 
from datetime import datetime
import pandas as pd
import requests

city_name = "barabanki"
base_url = "https://api.openweathermap.org/data/2.5/weather?q="

country = "IN"
with open("credentials.txt",'r') as f:
    api_key = f.read()


full_url = base_url + city_name +","+country+"&appid="+api_key

def etl_weather_url(url):

    r = requests.get(url)
    # print(r)
    data = r.json()
    # print(data)

    def kelvin_to_celcius(temp_in_kelvin):
        temp_in_celcius=(temp_in_kelvin -273.15)
        return temp_in_celcius

    city = data["name"]
    weather_description = data["weather"][0]['description']
    temp_celcius = round(kelvin_to_celcius(data['main']["temp"]),2)
    min_temp_celcius=round(kelvin_to_celcius(data['main']["temp_min"]),2)
    max_temp_celcius=round(kelvin_to_celcius(data['main']["temp_max"]),2)
    pressure = data["main"]["pressure"]
    humidity = data["main"]["humidity"]
    wind_speed=data["wind"]["speed"]
    time_of_record=datetime.utcfromtimestamp(data['dt'] +data['timezone'])
    sunrise_time = datetime.utcfromtimestamp(data['sys']['sunrise']+data['timezone'])
    sunset_time=datetime.utcfromtimestamp(data['sys']['sunset']+data['timezone'])

    # converting into dictionary
    transformed_data = {
        "City":city,
        "Description":weather_description,
        "Temperature (F)":temp_celcius,
        "Minimum Temp (F)": min_temp_celcius,
        "Maximum Temp (F)": max_temp_celcius,
        "Pressure":pressure,
        "Humidity": humidity,
        "Wind Speed":wind_speed,
        "Time of Record": time_of_record,
        "Sunrise Time": sunrise_time,
        "Sunset Time": sunset_time

    }

    # print(transformed_data)

    transformed_data_list = [transformed_data]
    df_data =pd.DataFrame(transformed_data_list)
    # print(df_data)

    df_data.to_csv("current_weather_data_barabanki.csv",index=False)



if __name__=="__main__":
    etl_weather_url(full_url)

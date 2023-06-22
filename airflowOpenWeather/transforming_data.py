import json 
from datetime import datetime
import pandas as pd
import requests

def kelvin_to_celcius(temp_in_kelvin):
        temp_in_celcius=(temp_in_kelvin -273.15)
        return temp_in_celcius

def transform_data(task_instance):
    data =task_instance.xcom_pull(task_ids="extract_weather_data")
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

    aws_credentials = {"key": " ","secret": " ", "token": " ", }


    now = datetime.now()
    dt_string = now.strftime("%d%m%Y%H%M%S")
    dt_string = 'current_eather_data_barabanki' + dt_string
    # df_data.to_csv(f"{dt_string}.csv",index=False )
    df_data.to_csv(f"s3://bucket-name/dt_string.csv",index=False ,storage_options=aws_credentials)




    def load_data(task_instance):
          data = task_instance.xcom_pull(task_ids="transform_weather_data")
          now = datetime.now()
          dt_string=now.strftime("%d%m%Y%H%M%S")
          dt_string="barabanki_weather_data" + dt_string
          data.to_csv(f"{dt_string}.csv",index=False)
import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

#setting up the Open-Mateo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmateo = openmeteo_requests.Client(session = retry_session)

url = "https://api.open-meteo.com/v1/forecast"

params = {
    "longitude" : 151.21, 
    "latitude" : -33.87, 
    "hourly" : ["temperature_2m", "weather_code"],
    "timezone" : "Australia/Sydney",
}
responses = openmateo.weather_api(url, params = params)

response = responses[0]

print(f"Coordinates: {response.Latitude()}N, {response.Longitude()}E")
print(f"Elevation: {response.Elevation()}M asl")
print(f"Timezone difference to GMT +0: {response.UtcOffsetSeconds()}s")

#Process hourly data
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_weather_code = hourly.Variables(1).ValuesAsNumpy()

hourly_data ={
    "time" : pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end = pd.to_datetime (hourly.TimeEnd(), unit="s", utc=True),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
    )
}

hourly_data["temperature_2m"] = hourly_temperature_2m
hourly_data["weather_code"] = hourly_weather_code

hourly_dataframe = pd.DataFrame(data=hourly_data)

hourly_dataframe["time"] = hourly_dataframe["time"].dt.tz_convert("Australia/Sydney")
hourly_dataframe["temperature_2m"] = hourly_dataframe["temperature_2m"].round(1)

now = pd.Timestamp.now(tz = "Australia/Sydney")
six_hours_later = now+pd.Timedelta(hours=6)

next_6_hours = hourly_dataframe[
    (hourly_dataframe["time"]>=now) &
    (hourly_dataframe["time"]<=six_hours_later)
]   

print("\n--- Sydney Weather — Next 6 Hours ---")
for _, row in next_6_hours.iterrows():
    time_str = row["time"].strftime("%I:%M %p")
    temp = round(row["temperature_2m"], 1)
    print(f"  {time_str}  →  {temp}°C")
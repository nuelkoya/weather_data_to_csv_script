import requests
from datetime import datetime
import csv
import os

API_KEY = "your_api_key_here"
HEADERS = ["City", "Temperature (C)", "Weather Description","Humidity", "Wind Speed", "Date", "Time"]
searched_cities_data = []
FILE = "my-weather-details.csv"

# Function to get weather data for user inputted city from API
def get_weather_data(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        res = requests.get(url)
        city_data = []

        if (res.status_code != 200):
            print(f"Request Error: {res.status_code}")
        else:
            city_weather_data = res.json()
            date_time_object = datetime.fromtimestamp(city_weather_data['dt'])
            date, time = date_time_object.strftime('%d %b %Y,%I:%M%p').split(',')
            city_data.append([
                city,
                city_weather_data['main']['temp'],
                city_weather_data['weather'][0]['description'],
                city_weather_data['main']['humidity'],
                city_weather_data['wind']['speed'],
                date,
                time
            ])
            return city_data
    except requests.exceptions.RequestException as error:
        print(f'Error: {error}')


# Function to write weather data to csv file
def write_to_csv(data):
    try:
        if (os.path.exists(FILE)):
            with open(FILE, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(data)
        else:
            with open(FILE, 'w') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(HEADERS)
                writer.writerows(data)
        print('weather data saved successfully!')
    except:
        print('weather data failed to save')

    

def main():
    while True:
        city = input('Enter a city: ')
        input_city_data = get_weather_data(city)
        if input_city_data:
            write_to_csv(input_city_data)
            break
        else:
            print('Something went wrong! Make sure you entered the right city name')


if __name__ == '__main__':
    main()

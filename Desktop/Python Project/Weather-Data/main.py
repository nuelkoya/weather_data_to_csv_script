import os
import requests
from datetime import datetime
import csv
import sqlite3

API_KEY = "bf09c3306fec22e396ee9db9afb9181e"
CSV_FILE = "weather-details.csv"
HEADERS = ["City", "Temperature (C)", "Weather Description","Humidity", "Wind Speed", "Wind Speed", "Date", "Time"]
DB_FILE = "my-database.db"   


def write_to_db(weather_details):
    DB_COLUMNS = ["city", "temperature", "description", "humidity", "wind_speed", "date", "time"]

    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()

        # Create table once, if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weather_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT NOT NULL,
                temperature REAL,
                description TEXT,
                humidity INTEGER,
                wind_speed REAL,
                date TEXT,
                time TEXT
            )
        """)

        # Check if city data exists for today
        cursor.execute("""
            SELECT * FROM weather_table
            WHERE city = ? AND date = ?
        """, (weather_details[0], weather_details[-2]))  # city & date

        existing = cursor.fetchone()
        
        if existing:
            print(f"⚠️ Weather data for {weather_details[0]} already exists for {weather_details[-2]}. Skipping insert.")
            return

        # Prepare insert query
        placeholders = ", ".join(["?"] * len(DB_COLUMNS))
       
        insert_sql = f"""
            INSERT INTO weather_table ({", ".join(DB_COLUMNS)})
            VALUES ({placeholders})
        """
        
        # Insert the record
        cursor.execute(insert_sql, weather_details)
        conn.commit()

        print(f"✅ Data for {weather_details[0]} inserted successfully into {DB_FILE}.")
        cursor.execute("""
            SELECT * FROM weather_table
        """)
        print(cursor.fetchall())
        
def write_to_csv(weather_details):
    cwd = os.getcwd()
    csv_path = os.path.join(cwd, CSV_FILE)

    if os.path.exists(csv_path):
        with open(CSV_FILE, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerows([weather_details])
    else:
        with open(CSV_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            #Header Row
            writer.writerow(HEADERS)
            #Data Rows
            writer.writerows([weather_details])

def get_weather_details(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            details = response.json()
            #print(details)
            dt= datetime.fromtimestamp(details["dt"])
            date = dt.strftime("%Y-%m-%d")
            time = dt.strftime("%I:%M:%S %p")

            return [city, details["main"]["temp"], details["weather"][0]["description"], 
            details["main"]["humidity"], details["wind"]["speed"], date, time]
        
        else:
            print("Error", response.status_code)
    except requests.exceptions.RequestException as e:
        print('Error', e)

def main():
    while True:
        city = input("Enter a city: ")
        weather_details = get_weather_details(city)
        if weather_details:
            write_to_csv(weather_details)
            write_to_db(weather_details)
            break
        else:
            print("Enter a valid city")

    



if __name__ == "__main__":
    main()

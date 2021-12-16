import requests
from datetime import datetime
import pandas as pd
import sqlite3

api_key = '1394505e471df042e0488df5208f5dc3'
exclude = 'current,minutely,hourly,alerts'


def get_cities_coords(cities):
    url_to_get_city_coords = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}' # 1) city name 2) api_key
    cities_coords = {}
    for city in cities:
        coords = requests.get(url_to_get_city_coords.format(city,api_key)).json()['coord']
        cities_coords[city] = coords
    return cities_coords


def get_daily_forecast_on_week(cities_coords):
    data = []
    url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude={}&appid={}&units=metric' # 1)lat 2)lon 3)what to exclude 4)api_key 5) metric system
    try:
        for city in cities_coords.keys():
            lon = cities_coords[city]['lon']
            lat = cities_coords[city]['lat']
            data.append(requests.get(url.format(lat,lon,exclude,api_key)).json())
    except Exception as exp:
        print(exp)
    return(data)
        

def data_preparation(data,cities):
    dataframe = pd.DataFrame()
    for idx,city_data in enumerate(data):
        for day in city_data['daily']:
            dataframe = dataframe.append({
                'city': cities[idx],
                'dt': datetime.utcfromtimestamp(day['dt']).strftime('%Y-%m-%d %H:%M:%S'),
                'temp': day['temp']['day'],
                'pop': day['pop'],
                'clouds': day['clouds'],
                'pressure': day['pressure'],
                'humidity': day['humidity'],
                'wind_speed': day['wind_speed']
            }, ignore_index=True)
    return dataframe


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)

    return conn

def weather_insert(conn, weather):
    """
    Create a new project into the projects table
    :param conn:
    :param weather:
    :return: project id
    """
    sql = ''' INSERT INTO weather(city,date,temp,pop,clouds,pressure,humidity,wind_speed)
              VALUES(?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, weather)
    conn.commit()
    return cur.lastrowid

if __name__ == '__main__':
    cities = ['Lviv','Kyiv','Kharkiv','Odesa','Ternopil']
    
    cities_coords = get_cities_coords(cities)
    daily_forecast_all = get_daily_forecast_on_week(cities_coords)
    dataframe = data_preparation(daily_forecast_all,cities)

    dataframe = dataframe[dataframe.index % 8 != 0]
    print(dataframe)
    connection = create_connection('application/dev.sqlite')
    
    for i in range(len(dataframe)):    
        weather_insert(connection,weather=(
                                dataframe.iloc[i]['city'],
                                dataframe.iloc[i]['dt'],
                                dataframe.iloc[i]['temp'],
                                dataframe.iloc[i]['pop'],
                                dataframe.iloc[i]['clouds'],
                                dataframe.iloc[i]['pressure'],
                                dataframe.iloc[i]['humidity'],
                                dataframe.iloc[i]['wind_speed']))    

    print(dataframe)    
    
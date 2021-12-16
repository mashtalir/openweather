from os import X_OK
from pandas.core.frame import DataFrame
import requests
import pandas as pd
import datetime

def cities_request():
    cities = requests.get(url='http://127.0.0.1:5000/cities').json()

    print('Міста україни що вибрались для прогнозу')
    for city in cities['cities']:
        print(city)

def mean_request():
    data = {'city':'Lviv',
            'param': 'temp'}
    mean = requests.get(url='http://127.0.0.1:5000/mean',json=data).json()
    print('Середня температура для міста Львів наступного тижня = ' + str(mean['mean']) + ' C')
    
    data = {'city':'Kyiv',
            'param': 'wind_speed'}
    mean = requests.get(url='http://127.0.0.1:5000/mean',json=data).json()
    print('Середня швидкість вітру для міста Київ наступного тижня = ' + str(mean['mean']) + ' m/s')
    
    
def records():
    data = {'city': 'Lviv',
            'start_dt': str((datetime.datetime.now() + datetime.timedelta(days=1)).date()),
            'end_dt':str((datetime.datetime.now() + datetime.timedelta(days=4)).date())}
    records = requests.get(url='http://127.0.0.1:5000/records',json=data).json()
    dataframe1 = pd.DataFrame()    
    for record in records['objects']:
        dataframe1 = dataframe1.append(record,ignore_index=True)
    print(dataframe1)
    
    data = {'city': 'Kharkiv',
            'start_dt': str((datetime.datetime.now() + datetime.timedelta(days=2)).date()),
            'end_dt':str((datetime.datetime.now() + datetime.timedelta(days=5)).date())}
    records = requests.get(url='http://127.0.0.1:5000/records',json=data).json()
    dataframe2 = pd.DataFrame()    
    for record in records['objects']:
        dataframe2 = dataframe2.append(record,ignore_index=True)
    print(dataframe2)

def moving_mean():
    data = {'city':'Lviv',
            'param': 'temp'}
    
    print('moving mean '+data['param'] + ' for '+data['city'])
    moving_mean = requests.get(url='http://127.0.0.1:5000/moving_mean',json=data).json()
    dataframe1 = pd.DataFrame.from_dict(moving_mean[data['param']],orient='index',columns=[data['param']])
    print(dataframe1)
    
    data = {'city':'Odesa',
            'param': 'pressure'}
    print('\nmoving mean '+data['param'] + ' for '+data['city'])
    moving_mean = requests.get(url='http://127.0.0.1:5000/moving_mean',json=data).json()
    dataframe2 = pd.DataFrame.from_dict(moving_mean[data['param']],orient='index',columns=[data['param']])
    print(dataframe2)
        


def main():
    while True:
        print('\nChoose api number to call one\n'
              '1 - /cities\n'
              '2 - /mean\n'
              '3 - /records\n'
              '4 - /moving_mean')
        option = input()
        if option == '1':
            cities_request()
        elif option == '2':
            mean_request()
        elif option == '3':
            records()
        elif option == '4':
            moving_mean()
        elif option == '0':
            exit()
        else:
            continue

    
    
    
    








if __name__ == '__main__':
    main()
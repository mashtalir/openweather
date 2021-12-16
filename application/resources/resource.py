from datetime import datetime
from flask_restful import Resource,reqparse
from pandas.core.window import rolling
from application.models.models import Weather
from application.app import db
from flask import request, Response
import statistics
from flask import json,jsonify
import pandas as pd

def convertion_to_dict(weather_objects):
    for idx in range(len(weather_objects)):
        weather_objects[idx] = weather_objects[idx].__dict__
        del weather_objects[idx]['_sa_instance_state']
    return weather_objects


class Cities(Resource):
    
    def get(self):
        query = db.session.query(Weather.city.distinct().label("city"))
        cities = [row.city for row in query.all()]

        return {'cities': cities}

class Mean(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('city')
        parser.add_argument('param')
        data = parser.parse_args()
        objects = Weather.query.filter_by(city=data['city']).all()
        mean = statistics.mean([obj.__dict__[data['param']] for obj in objects])
        return {'mean':mean}

class Records(Resource):
    
    def find_indexes(self,weather_objects,start_dt,end_dt):
        start,end = None,None
        for idx, obj in enumerate(weather_objects):
            if obj['date'].date() == datetime.strptime(start_dt,'%Y-%m-%d').date():
                start = idx
            if obj['date'].date() == datetime.strptime(end_dt,'%Y-%m-%d').date():
                end = idx + 1
        return start,end
    
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('city')
        parser.add_argument('start_dt')
        parser.add_argument('end_dt')
        data = parser.parse_args()
        weather_objects = Weather.query.filter_by(city=data['city']).order_by(Weather.date.asc()).all()
        weather_objects = convertion_to_dict(weather_objects)

        start_idx,end_idx = self.find_indexes(weather_objects,data['start_dt'],data['end_dt'])

        
        choosed_weather_objects = jsonify({'objects' : weather_objects[start_idx:end_idx]})
        
        return choosed_weather_objects
    

class MovingMean(Resource):
    def convertion_to_df(self,weather_objects,data):
        dataframe = pd.DataFrame()
        for obj in weather_objects:
            dataframe = dataframe.append({
                    'date': str(obj['date'].date()),
                    '{}'.format(data['param']): obj[data['param']]
                }, ignore_index=True)
    
        dataframe = dataframe.set_index('date')
        return dataframe
    
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('city')
        parser.add_argument('param')
        data = parser.parse_args()
        weather_objects = Weather.query.filter_by(city=data['city']).order_by(Weather.date.asc()).all()
        weather_objects = convertion_to_dict(weather_objects)
        dataframe = self.convertion_to_df(weather_objects,data)
                
        rolling_mean_df = dataframe.rolling(window=3, min_periods=1).mean().to_json()
        rolling_mean_df = json.loads(rolling_mean_df)
        
        return rolling_mean_df

        
        

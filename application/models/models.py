import datetime

from application.app import db

class Weather(db.Model):
    __tablename__ = 'weather'
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String)
    date = db.Column(db.DateTime)
    temp = db.Column(db.Float)
    pop = db.Column(db.Float)
    clouds = db.Column(db.Integer)
    pressure = db.Column(db.Integer)
    humidity = db.Column(db.Integer)
    wind_speed = db.Column(db.Float)
    
    def __init__(self,city,date,temp,pop,clouds,pressure,humidity,wind_speed):
        self.city = city
        self.date = date
        self.temp = temp
        self.pop = pop
        self.clouds = clouds
        self.pressure = pressure
        self.humidity = humidity
        self.wind_speed = wind_speed

    def __repr__(self):
 	    return "<{} : {}>".format(self.city, self.date)


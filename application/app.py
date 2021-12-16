from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_restful import Api
from application.config import DevelopmentConfig


app = Flask(__name__)
app.config.from_object(DevelopmentConfig())
db = SQLAlchemy(app)
api = Api(app)


from application.resources.resource import Cities,Mean,MovingMean,Records

api.add_resource(Cities,'/cities')
api.add_resource(Mean,'/mean')
api.add_resource(Records,'/records')
api.add_resource(MovingMean,'/moving_mean')



@app.cli.command('create-tables')
def create_db():
    """Creates the db tables."""
    db.create_all()

@app.cli.command('drop-tables')
def drop_db():
    """Drops the db tables."""
    db.drop_all()



if __name__ == '__main__':
    app.run(debug=True)
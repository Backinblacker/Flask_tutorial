from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api, Resource
from dotenv import load_dotenv
from os import environ

load_dotenv()

# Create App instance
app = Flask(__name__)

# Add DB URI from .env
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')

# Registering App w/ Services
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)
CORS(app)
Migrate(app, db)

# Models
class Car(db.Model):
# The Primary Key makes id the unique identifier
    id = db.Column(db.Integer, primary_key = True)
# 255 is the max amount of characters, Can be set to whatever
# nullable because we don't want to add a row without a make or model
    make = db.Column(db.String(255), nullable = False)
    model = db.Column(db.String(255), nullable = False)
    year = db.Column(db.Integer)
    
    def __repr__(self):
        return f'{self.year} {self.make} {self.model}'

# Schemas
class CarSchema(ma.Schema):
    class Meta:
        fields = ("id", "make", "model", "year")

# Single Car
car_schema = CarSchema()
# Multiple Cars
cars_schema = CarSchema(many=True)

# Resources
# Majority of the code goes in this section
# Handling Multiple Cars
class CarListResource(Resource):
    def get(self):
        all_cars = Car.query.all()
# Cars Schema used to prevent NOT JSON Serialized error
        return cars_schema.dump(all_cars)
    
    def post(self):
        new_car = Car(
            make= request.json['make'],
            model= request.json['model'],
            year=request.json['year']
        )
        db.session.add(new_car)
        db.session.commit()
# Serialize a single car using the CAR schema
        return car_schema.dump(new_car)


# Routes
# "flask run" to start the program
api.add_resource(CarListResource, '/api/cars')
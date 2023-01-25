from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@host:port/database'
db = SQLAlchemy(app)

class Vendor(db.Model):
    __tablename__ = 'vendors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    location = db.Column(Geometry('POINT'))

vendor = Vendor.query.filter_by(name='vendor_name').first()
location = vendor.location

from sqlalchemy import func
# to retrieve vendors within a certain distance from a point
point = 'POINT(-73.99174 40.73587)'
vendors = db.session.query(Vendor).filter(func.ST_DWithin(Vendor.location, point, distance)).all()


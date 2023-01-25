from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry
from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@host:port/database'
db = SQLAlchemy(app)

class Vendor(db.Model):
    __tablename__ = 'vendors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    location = db.Column(Geometry('POINT'))

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    location = db.Column(Geometry('POINT'))

@app.route('/vendors/nearby/<customer_id>/<distance>')
def get_nearby_vendors(customer_id, distance):
    customer = Customer.query.filter_by(id=customer_id).first()
    if customer is None:
        return "No customer with that ID was found"
    else:
        customer_location = customer.location
        vendors = db.session.query(Vendor).filter(func.ST_DWithin(Vendor.location, customer_location, distance)).all()
        if not vendors:
            return "No vendors found near that customer"
        else:
            vendor_list = []
            for vendor in vendors:
                vendor_list.append(vendor.name)
            return vendor_list

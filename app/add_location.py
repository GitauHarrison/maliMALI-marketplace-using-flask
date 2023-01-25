from geoalchemy2.elements import WKTElemet
from app.models import User
from app import db

def add_location():
    lat = ''
    lon = ''
    location = WKTElemet(f'POINT({lon} {lat})', srid=4326)
    user = User(location=location)
    db.session.add(user)
    db.session.commit()
    return 'Success'
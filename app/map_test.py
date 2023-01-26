from geoalchemy2 import Geography
from sqlalchemy import func
from flask_googlemaps import Map
from app.ip_address import get_user_location


class Vendor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    location = db.Column(Geography(geometry_type='POINT'))

@app.route('/shops/<float:latitude>/<float:longitude>')
def shops(latitude, longitude):

    # vendor = Vendor.query.filter_by(name='vendor_name').first()
    # location = vendor.location

    point = f'POINT({longitude} {latitude})'
    vendors = Vendor.query.filter(func.ST_DWithin(Vendor.location, from_text(point), distance)).all()
    return render_template('shops.html', vendors=vendors)




@app.route('/map-bounded/')
def map_bounded():
"""Create map with all markers within bounds."""
    my_location = get_user_location()
    locations = []    # long list of coordinates
    map = Map(
        identifier="view-side",
        lat=my_location.latititude,
        lng=my_location.longitude,
        markers=[(my_location.latititude, my_location.longitude)]
    )
    return render_template('map.html', map=map)

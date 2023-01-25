from geoalchemy2 import Geography
from sqlalchemy import func



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
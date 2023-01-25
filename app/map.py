import overpy
from app.ip_address import get_user_location

user_location = get_user_location()
user_lat = user_location.latitude
user_lon = user_location.longitude

def get_shops(latitude=user_lat, longitude=user_lon):
    """Get shops around the user"""
    # Initialize the API
    api = overpy.Overpass()

    # Define the query
    query = """(
        node["shop"](around:500,{lat},{lon});
        node["building"="retail"](around:500,{lat},{lon});
        node["building"="supermarket"](around:500,{lat},{lon});
        node["healthcare"="pharmacy"](around:500,{lat},{lon});
    );out;
    """.format(lat=latitude, lon=longitude)

    # Call the API
    result = api.query(query)
    return result

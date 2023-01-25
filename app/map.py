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
        node["shop"](around:1000,{lat},{lon});
        node["building"="retail"](around:1000,{lat},{lon});
        node["building"="supermarket"](around:1000,{lat},{lon});
        node["healthcare"="pharmacy"](around:1000,{lat},{lon});
    );out;
    """.format(lat=latitude, lon=longitude)

    # Call the API
    result = api.query(query)
    return result


def get_shops_data():
    # Get shops data from Open Maps Street
    shops = get_shops(user_lat, user_lon)

    # Initialize variables
    id_counter = 0
    markers = ''

    for node in shops.nodes:

        # Create unique ID for each marker
        idd = 'shop' + str(id_counter)
        id_counter += 1

        # Check if shops have name and website in OSM
        try:
            shop_brand = node.tags['brand']
        except:
            shop_brand = 'null'

        try:
            shop_website = node.tags['website']
        except:
            shop_website = 'null'

        # Create the marker and its pop-up for each shop
        markers += "var {idd} = L.marker([{latitude}, {longitude}]);\
                    {idd}.addTo(map).bindPopup('{brand}<br>{website}');".format(idd=idd, latitude=node.lat,\
                                                                                    longitude=node.lon,
                                                                                    brand=shop_brand,\
                                                                                    website=shop_website)

        # Return data to be used to render the map on the page
    return markers

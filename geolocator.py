from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from geopy.distance import geodesic


geolocator = Nominatim(user_agent="hotel_location")

city_coords = (50.0647, 19.945)


def get_coordinates(location: str) -> tuple[float | None]:
    try:
        geo = geolocator.geocode(location, timeout=30)
        if geo:
            return geo.latitude, geo.longitude
        else:
            return None, None
    except GeocoderTimedOut:
        return None, None


def calc_distance(row):
    return geodesic(city_coords, (row[-2], row[-1])).kilometers

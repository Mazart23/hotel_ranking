from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut


geolocator = Nominatim(user_agent="hotel_location")

def get_coordinates(location: str) -> tuple[float | None]:
    try:
        geo = geolocator.geocode(location, timeout=30)
        if geo:
            return geo.latitude, geo.longitude
        else:
            return None, None
    except GeocoderTimedOut:
        return None, None
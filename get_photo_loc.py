from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def get_exif_data(image_path):
    """Extracts EXIF data from an image."""
    image = Image.open(image_path)
    exif_data = image._getexif()
    if exif_data is None:
        return None

    # Convert EXIF tag numbers to names
    labeled_exif = {TAGS.get(tag): value for tag, value in exif_data.items()}
    return labeled_exif

def get_gps_info(exif_data):
    """Extracts GPS information from EXIF data."""
    if not exif_data or 'GPSInfo' not in exif_data:
        return None

    gps_info = {}
    for key in exif_data['GPSInfo']:
        name = GPSTAGS.get(key)
        gps_info[name] = exif_data['GPSInfo'][key]

    return gps_info

def convert_to_degrees(value):
    """Converts GPS coordinates to degrees."""
    d, m, s = value
    return d + (m / 60.0) + (s / 3600.0)

def get_lat_lng(gps_info):
    """Converts GPS info to latitude and longitude."""
    if not gps_info:
        return None

    lat = gps_info.get('GPSLatitude')
    lat_ref = gps_info.get('GPSLatitudeRef')
    lng = gps_info.get('GPSLongitude')
    lng_ref = gps_info.get('GPSLongitudeRef')

    if not lat or not lng or not lat_ref or not lng_ref:
        return None

    lat = convert_to_degrees(lat)
    if lat_ref != 'N':
        lat = -lat

    lng = convert_to_degrees(lng)
    if lng_ref != 'E':
        lng = -lng

    return lat, lng



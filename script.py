from PIL import Image
import exifread

def get_decimal_from_dms(dms, ref):
    """
    Mengonversi koordinat dari format DMS (degree, minute, second) ke desimal.
    """
    degrees = dms[0].num / dms[0].den
    minutes = dms[1].num / dms[1].den / 60
    seconds = dms[2].num / dms[2].den / 3600
    decimal = degrees + minutes + seconds
    if ref in ['S', 'W']:
        decimal = -decimal
    return decimal

def extract_gps_coordinates(image_path):
    """
    Mengekstrak koordinat GPS dari metadata EXIF gambar.
    """
    try:
        with open(image_path, 'rb') as img_file:
            tags = exifread.process_file(img_file)
            
            # Mendapatkan data GPS
            gps_latitude = tags.get('GPS GPSLatitude')
            gps_latitude_ref = tags.get('GPS GPSLatitudeRef')
            gps_longitude = tags.get('GPS GPSLongitude')
            gps_longitude_ref = tags.get('GPS GPSLongitudeRef')
            
            if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
                lat = get_decimal_from_dms(gps_latitude.values, gps_latitude_ref.values)
                lon = get_decimal_from_dms(gps_longitude.values, gps_longitude_ref.values)
                return lat, lon
            else:
                return None
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return None


print(extract_gps_coordinates("img4.jpg"))
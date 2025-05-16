import piexif

def decode_bytes(value):
    try:
        return value.decode() if isinstance(value, bytes) else value
    except:
        return value

def convert_to_degrees(value):
    d = value[0][0] / value[0][1]
    m = value[1][0] / value[1][1]
    s = value[2][0] / value[2][1]
    return d + (m / 60.0) + (s / 3600.0)


image_path = "yourimage.jpg"


exif_dict = piexif.load(image_path)
for ifd_name in exif_dict:
    print(f"\n--- {ifd_name} ---")
    
    if exif_dict[ifd_name] is None:
        continue
    
    for tag in exif_dict[ifd_name]:
        tag_info = piexif.TAGS.get(ifd_name, {}).get(tag, {})
        tag_name = tag_info.get("name", f"Unknown tag {tag}")
        value = exif_dict[ifd_name][tag]
        value = decode_bytes(value)
        print(f"{tag_name:25}: {value}")

gps_data = exif_dict.get("GPS")
if gps_data:
    lat = gps_data.get(piexif.GPSIFD.GPSLatitude)
    lat_ref = gps_data.get(piexif.GPSIFD.GPSLatitudeRef)
    lon = gps_data.get(piexif.GPSIFD.GPSLongitude)
    lon_ref = gps_data.get(piexif.GPSIFD.GPSLongitudeRef)

    if lat and lon and lat_ref and lon_ref:
        lat_deg = convert_to_degrees(lat)
        lon_deg = convert_to_degrees(lon)
        if lat_ref.decode() == "S":
            lat_deg = -lat_deg
        if lon_ref.decode() == "W":
            lon_deg = -lon_deg
        print(f"\n📍 GPS Coordinates:")
        print(f"Latitude:  {lat_deg}")
        print(f"Longitude: {lon_deg}")
    else:
        print("\nGPS data is present but incomplete.")
else:
    print("\nNo GPS data found.")

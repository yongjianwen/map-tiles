import math
import os
import requests
from pathlib import Path

BASE_URL = "https://services.arcgisonline.com/arcgis/rest/services/World_Topo_Map/MapServer/tile"

# Singapore bbox
MIN_LON, MIN_LAT = 103.59, 1.16
MAX_LON, MAX_LAT = 104.10, 1.48

OUT_DIR = Path("tiles")
ZOOM_LEVELS = range(0, 15)  # adjust: 0-14 first; higher zoom = many more tiles


def lonlat_to_tile(lon, lat, z):
    lat_rad = math.radians(lat)
    n = 2 ** z

    x = int((lon + 180.0) / 360.0 * n)

    y = int(
        (1.0 - math.log(math.tan(lat_rad) + 1 / math.cos(lat_rad)) / math.pi)
        / 2.0
        * n
    )

    return x, y


for z in ZOOM_LEVELS:
    x_min, y_max = lonlat_to_tile(MIN_LON, MIN_LAT, z)
    x_max, y_min = lonlat_to_tile(MAX_LON, MAX_LAT, z)

    print(f"Zoom {z}: x {x_min}-{x_max}, y {y_min}-{y_max}")

    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            url = f"{BASE_URL}/{z}/{y}/{x}"
            path = OUT_DIR / str(z) / str(x) / f"{y}.jpg"

            if path.exists():
                continue

            path.parent.mkdir(parents=True, exist_ok=True)

            r = requests.get(url, timeout=20)

            if r.status_code == 200:
                path.write_bytes(r.content)
                print("saved", path)
            elif r.status_code == 404:
                print("missing", z, y, x)
            else:
                print("error", r.status_code, url)

import os
import sys
import json 
import requests

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from config.config import MINIO_ENDPOINT, MINIO_USER, MINIO_PASSWORD, MINIO_BUCKET, AUDIO_DIR, AVES_CLASSIFY_URL

from minio import Minio

ALLOWED_EXTENSIONS = { ".mp3", ".wav" }
LOCATIONS_FILE = os.path.join(os.path.dirname(__file__), "..", "config", "locations.json")

#MINIO CLIENT
minio_client = Minio(
    endpoint=MINIO_ENDPOINT,
    access_key=MINIO_USER,
    secret_key=MINIO_PASSWORD,
    secure=False
)

#MINIO CONNECTION 
try:
    buckets = minio_client.list_buckets()
    print("Connected to Minio")
except Exception as e:
    print(f"Error connecting to Minio: {e}")
    sys.exit(1)

print("Buckets:")
for b in buckets:
    print(f"--- {b.name}")

print()


# Check if MINIO BUCKET exits
if not minio_client.bucket_exists(MINIO_BUCKET):
    minio_client.make_bucket(MINIO_BUCKET)
    print(f"Bucket created: {MINIO_BUCKET}")
else:
    print(f"Bucket '{MINIO_BUCKET}' already exists.")

print()

# Load locations.json

with open(LOCATIONS_FILE, "r", encoding="utf-8") as f:
    locations = json.load(f)

print(f"Loaded {len(locations)} locations: {list(locations.keys())}")

# Pass through data/audio folders
for location_name in sorted(os.listdir(AUDIO_DIR)):
    location_path = os.path.join(AUDIO_DIR, location_name)

    if not os.path.isdir(location_path):
        continue

    #Get coordinates for this folder
    coords = locations.get(location_name)
    if coords is None:
        print(f"No coordinations for this location: {location_name}")
        continue
        
    print(f"--- {location_name} (lat={coords['lat']}) (lon={coords['lon']})")

    for filename in sorted(os.listdir(location_path)):
        _, ext = os.path.splitext(filename)
        if ext.lower() not in ALLOWED_EXTENSIONS:
            continue

        file_path = os.path.join(location_path, filename)
        object_key = f"{location_name}/{filename}"

        print(f"\taudio: {filename}")

        #upload to Minio
        minio_client.fput_object(MINIO_BUCKET, object_key, file_path)
        print(f"\tuploaded to Minio as '{object_key}'")

        # call classification API
        with open(file_path, "rb") as audio_file:
            files = {"file": (filename, audio_file)}
            response = requests.post(AVES_CLASSIFY_URL, files=files, timeout=120)

        response.raise_for_status()
        api_response = response.json()

        detections = api_response.get("results", [])
        print(f"\t{len(detections)} detection(s)")
        for det in detections:
            print(f"\t  - {det.get('scientific_name')} "
                  f"({det.get('common_name')}) "
                  f"conf={det.get('confidence')}")










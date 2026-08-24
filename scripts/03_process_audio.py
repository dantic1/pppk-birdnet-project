import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from config.config import MINIO_ENDPOINT, MINIO_USER, MINIO_PASSWORD

from minio import Minio

client = Minio(
    endpoint=MINIO_ENDPOINT,
    access_key=MINIO_USER,
    secret_key=MINIO_PASSWORD,
    secure=True
)

try:
    buckets = client.list_buckets()
    print("Connected to Minio")
except Exception as e:
    print(f"Error connecting to Minio: {e}")
    sys.exit(1)

for b in buckets: 
    print(f"--- {b.name}")




import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from config.config import MINIO_ENDPOINT, MINIO_USER, MINIO_PASSWORD, MINIO_BUCKET

from minio import Minio

minio_client = Minio(
    endpoint=MINIO_ENDPOINT,
    access_key=MINIO_USER,
    secret_key=MINIO_PASSWORD,
    secure=False
)

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

if not minio_client.bucket_exists(MINIO_BUCKET):
    minio_client.make_bucket(MINIO_BUCKET)
    print(f"Bucket created: {MINIO_BUCKET}")
else:
    print(f"Bucket '{MINIO_BUCKET}' already exists.")






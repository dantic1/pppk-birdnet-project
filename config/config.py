from dotenv import load_dotenv
import os

load_dotenv()

#MONGODB
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")

#Collections
COLLECTION_SPECIES = "species"
COLLECTION_OBSERVATIONS = "observations"
COLLECTION_CLASSIFICATIONS = "classifications"

#MINIO
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_USER = os.getenv("MINIO_USER")
MINIO_PASSWORD = os.getenv("MINIO_PASSWORD")
MINIO_BUCKET = os.getenv("MINIO_BUCKET")

#External API
AVES_BASE_URL = "https://aves.regoch.net"
AVES_CLASSIFY_URL = f"{AVES_BASE_URL}/api/classify"

#LOCAL PATHS
AUDIO_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "audio")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")
LOGS_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")

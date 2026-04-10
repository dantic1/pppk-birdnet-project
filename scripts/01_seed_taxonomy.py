import sys
import requests
import os
from pymongo import MongoClient, UpdateOne
from pymongo.errors import BulkWriteError

#Append for config
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from config.config import MONGO_URI, MONGO_DB, COLLECTION_SPECIES, AVES_BASE_URL

def fetch_species() -> list[dict]:
    url = f"{AVES_BASE_URL}/aves.json"

    print(f"Fetching data from {url}")

    response = requests.get(url, timeout=30)
    response.raise_for_status()
    data = response.json()

    print(f"Fetched {len(data)} species")
    
    return data

def seed_taxonomy():
    client = MongoClient(MONGO_URI)
    db = client.get_database(MONGO_DB)
    collection = db.get_collection(COLLECTION_SPECIES)

    #Check if data exist
    existing_count = collection.count_documents({}) #count all
    if existing_count > 0:
        print(f"Species collection already contains {existing_count} documents. Skipping seed!")
        client.close()
        return

    species_list = fetch_species()

    #Create index on 'key' field
    collection.create_index("key", unique=True)

    #Upsert
    operations = []

    for species in species_list:
        op = UpdateOne(
            {"key": species["key"]},
            {"$set": species},
            upsert=True
        )
        operations.append(op)

    try:
        result = collection.bulk_write(operations, ordered=False)
        print(f"Seeding complete!")
        print(f"> Inserted: {result.upserted_count}")
        print(f"> Modified: {result.modified_count}")
    except BulkWriteError as er:
        print(f"Bulk write error (some duplicates skipped): {er.details}")
    
    client.close()

if __name__ == "__main__":
    seed_taxonomy()



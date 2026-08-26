import os
import sys
from pymongo import MongoClient
import pandas as pd 

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from config.config import MONGO_URI, MONGO_DB, COLLECTION_CLASSIFICATIONS, CONFIDENCE_THRESHOLD, OUTPUT_DIR

# MONGO CLIENT
mongo_client = MongoClient(MONGO_URI)
db = mongo_client.get_database(MONGO_DB)
classifications = db.get_collection(COLLECTION_CLASSIFICATIONS)

db.command("ping")
print(f"Connected to mongoDB, database: {MONGO_DB}")

all_classifications = list(classifications.find({}))
print(f"Fetched {len(all_classifications)} classifications")

# check 
for c in all_classifications[:3]:
    print(f"  {c.get('scientific_name')} "
          f"| conf={c.get('confidence')} "
          f"| matched={c.get('matched_taxonomy')} "
          f"| location={c.get('location')}")
    
positive = []

#Filter 
for c in all_classifications:
    if c.get("confidence", 0) >= CONFIDENCE_THRESHOLD: # >= 0.7
        positive.append(c)

print(f"\nConfidence threshold: {CONFIDENCE_THRESHOLD}")
print(f"Positive classifications (>= {CONFIDENCE_THRESHOLD}): {len(positive)} of {len(all_classifications)}")

for c in positive:
    print(f"  {c.get('scientific_name')} "
          f"| conf={round(c.get('confidence'), 3)} "
          f"| matched={c.get('matched_taxonomy')}")
    
species_agg = {}

for c in positive:

    name = c.get("scientific_name")

    if name not in species_agg:
        species_agg[name] = {
            "species": name,
            "common_name": c.get("common_name"),
            "species_key": c.get("species_key"),
            "matched_taxonomy": c.get("matched_taxonomy"),
            "observation_ids": set(),
        }

    species_agg[name]["observation_ids"].add(c.get("observation_id"))

print(f"\n--- Aggregated {len(species_agg)} species ---")

for name, stats in species_agg.items():
    obs_count = len(stats["observation_ids"])
    print(f"\t{name} ({stats['common_name']}) | observations={obs_count} | matched={stats['matched_taxonomy']}")
    
#CSV
rows = []
for name, stats in species_agg.items():
    rows.append({
        "species": stats["species"],
        "common_name": stats["common_name"],
        "species_key": stats["species_key"],
        "matched_taxonomy": stats["matched_taxonomy"],
        "observation_count": len(stats["observation_ids"]),
    })

df = pd.DataFrame(rows)

os.makedirs(OUTPUT_DIR, exist_ok=True)

output_path = os.path.join(OUTPUT_DIR, "report.csv")
df.to_csv(output_path, index=False)

print(f"\nReport saved: {output_path}")
print(f"Num of species: {len(df)}")

# PPPK BirdNET Project

A data pipeline for bird observations. It identifies bird species from audio
recordings, links them with taxonomy data, and generates a CSV report.

## What it does

The pipeline has three steps:

1. **Seed taxonomy** (`01_seed_taxonomy.py`) — fetches bird species data from
   `aves.regoch.net` and stores it in MongoDB (no duplicates).
2. **Process audio** (`03_process_audio.py`) — for each audio file: uploads it
   to MinIO, sends it to the classification API, stores the request log in MinIO
   and the classification results in MongoDB (linked to taxonomy).
3. **Generate report** (`04_generate_report.py`) — reads classifications from
   MongoDB, filters by confidence, and generates a CSV with per-species statistics.

Storage: **MongoDB** (taxonomy, observations, classifications) and **MinIO**
(audio files + logs), both running as Docker containers.

## Requirements

- Docker + Docker Compose
- Python 3.13

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/dantic1/pppk-birdnet-project.git
cd pppk-birdnet-project

# 2. Virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Create the .env file (copy the template and fill in the values)
cp .env.example .env

# 4. Start the services (MongoDB + MinIO)
docker compose up -d
```

### .env

```
MONGO_USER=mongoadmin
MONGO_PASSWORD=mongoadmin123
MONGO_DB=pppk-birds
MONGO_URI=mongodb://mongoadmin:mongoadmin123@localhost:27017/pppk-birds?authSource=admin

MINIO_USER=minioadmin
MINIO_PASSWORD=minioadmin123
MINIO_ENDPOINT=localhost:9000
MINIO_BUCKET=pppk-birds-audio
```

## Audio files

Audio files go into `data/audio/<location>/`, where each folder is one location.
Location coordinates are defined in `config/locations.json`:

```json
{
  "labin": { "lat": 45.091395, "lon": 14.123601 },
  "vis":   { "lat": 43.043421, "lon": 16.16551 }
}
```

Supported formats: `.mp3` and `.wav`. Short recordings (~10–20 s) are recommended.

## Running

Run the whole pipeline with a single command (via Snakemake):

```bash
snakemake --cores 1
```

Or run the scripts individually:

```bash
python3 scripts/01_seed_taxonomy.py
python3 scripts/03_process_audio.py
python3 scripts/04_generate_report.py
```

The result (`report.csv`) is saved to the `output/` folder.

## Inspecting results

- **MongoDB** — `docker exec -it pppk_birdnet_mongodb mongosh -u mongoadmin -p mongoadmin123 --authenticationDatabase admin`
- **MinIO console** — http://localhost:9001 (login: `minioadmin` / `minioadmin123`)

## GitHub Actions

The pipeline can also be run manually in the cloud:
**Actions** tab → *PPPK BirdNET Pipeline* → *Run workflow*.
Credentials are read from GitHub Secrets.

## Tech stack

Python · MongoDB · MinIO · Docker Compose · Snakemake · GitHub Actions

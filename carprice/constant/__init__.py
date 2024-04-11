import os
from datetime import datetime

PIPELINE_NAME: str = "carprice"
ARTIFACT_DIR: str = "artifacts"

MONGODB_URL_KEY = "MONGODB_URL"

DATABASE_NAME = "iNeuron"
COLLECTION_NAME = "car"

# common file name
FILE_NAME: str = "car.csv"
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

BUCKET_NAME = "carprice-2024"

SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")


"""
Data Ingestion related constants start with DATA_INGESTION VAR NAME
"""
DATA_INGESTION_COLLECTION_NAME: str = "car"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURED_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2

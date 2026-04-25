import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient, models

load_dotenv()

COLLECTION_NAME = "financial"
QDRANT_URL = os.getenv("QDRANT_URL")

def run_migration():
    client = QdrantClient(url=QDRANT_URL)
    
    if not client.collection_exists(COLLECTION_NAME):
        print(f"Collection {COLLECTION_NAME} does not exist. Skipping migration.")
        return

    fields_to_index = [
        "metadata.ticker",
        "metadata.form_type",
        "metadata.source"
    ]
    
    for field in fields_to_index:
        print(f"Creating KEYWORD index for {field}...")
        client.create_payload_index(
            collection_name=COLLECTION_NAME,
            field_name=field,
            field_schema=models.PayloadSchemaType.KEYWORD,
        )
    
    print("Migration completed successfully.")

if __name__ == "__main__":
    run_migration()

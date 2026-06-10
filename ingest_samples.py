import os
import glob
import sys

# Ensure src is in python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from signalnoise.services.ingestion_service import IngestionService
from signalnoise.database.connection import SessionLocal
from signalnoise.database.entities.document_entity import DocumentEntity
from signalnoise.rag.vectorstore import VectorStore

def clear_db():
    print("Clearing existing database...")
    # Clear Postgres  
    session = SessionLocal()
    try:
        from signalnoise.database.models import SignalRecord, TrendRecord, RiskRecord
        session.query(SignalRecord).delete()
        session.query(TrendRecord).delete()
        session.query(RiskRecord).delete()
        session.query(DocumentEntity).delete()
        session.commit()
        print("PostgreSQL cleared successfully.")
    except Exception as e:
        print("Failed to clear PostgreSQL:", e)
    finally:
        session.close()

    # Clear Chroma
    try:
        vectorstore = VectorStore()
        chroma_client = vectorstore.get_vectorstore()
        all_ids = chroma_client.get()["ids"]
        if all_ids:
            chroma_client.delete(ids=all_ids)
        print("ChromaDB cleared successfully.")
    except Exception as e:
        print("Failed to clear ChromaDB:", e)

def ingest_all():
    ingestion = IngestionService()
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    
    # Categories of documents to ingest
    categories = [
        "customer_escalation",
        "operational_outage",
        "team_burnout",
        "dependency_risk"
    ]
    
    total_ingested = 0
    for cat in categories:
        cat_dir = os.path.join(data_dir, cat)
        if not os.path.exists(cat_dir):
            continue
        # Ingest first 3 files of each category
        files = glob.glob(os.path.join(cat_dir, "*.*"))
        print(f"\nIngesting category: {cat} (found {len(files)} files)")
        for file_path in files[:3]:
            try:
                ingestion.ingest(file_path)
                print(f"Ingested: {os.path.basename(file_path)}")
                total_ingested += 1
            except Exception as e:
                print(f"Failed to ingest {os.path.basename(file_path)}: {e}")
                
    print(f"\nIngested {total_ingested} sample documents successfully.")

if __name__ == "__main__":
    clear_db()

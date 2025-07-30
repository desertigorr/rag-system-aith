import os
from dotenv import load_dotenv

load_dotenv()

QDRANT_URL = os.environ.get("QDRANT_URL")
QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY")
openrouter_api = os.environ.get("openrouter_api")
COLLECTION_NAME = os.environ.get("COLLECTION_NAME")

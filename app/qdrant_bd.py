from qdrant_client import QdrantClient
from qdrant_client.http import models
from app.api import QDRANT_API_KEY, QDRANT_URL, COLLECTION_NAME
from app.rag_data import get_info
from selenium import webdriver
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY    
)

print(client.get_collections())  # проверка подключения

urls=["https://ai.itmo.ru/","https://ai.itmo.ru/junior_ml_contest", "https://ai.itmo.ru/projects"]

driver = webdriver.Chrome()

data = []


print(f"================ Начинаем обработку urls ===================")
for url in urls:
    parsed_data = str(get_info(driver, url))
    data.append(parsed_data)
    print(f"Источник {url} загружен.")
print(f"================= Закончили обработку urls ==================")

embeddings = HuggingFaceEmbeddings(
    model_name="Qodo/Qodo-Embed-1-1.5B",
    model_kwargs={"trust_remote_code": True}
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300, 
    chunk_overlap=50, 
    add_start_index=True
)

def split_text_chunks(text_array, splitter):
    all_splits = []
    for obj in text_array:
        all_splits.extend(splitter.split_text(obj))
    return all_splits

proceed_texts = split_text_chunks(data, text_splitter)

def add_texts_to_qdrant(texts, source_tag="generic"):

    vectors = embeddings.embed_documents(texts)  # считаем эмбеддинги пачкой
    source_tag = "talent hub website"
    points = []
    for idx, (vector, text) in enumerate(zip(vectors, texts)):
        payload = {"text": text, "source": source_tag}
        points.append(models.PointStruct(
            id=idx,
            vector=vector,
            payload=payload
        ))

    client.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"Загружено {len(points)} чанков в коллекцию {COLLECTION_NAME}")

add_texts_to_qdrant(proceed_texts)
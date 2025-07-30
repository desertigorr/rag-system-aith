from langchain_huggingface import HuggingFaceEmbeddings
from app.api import openrouter_api, QDRANT_API_KEY, QDRANT_URL, COLLECTION_NAME
from qdrant_client import QdrantClient
from openai import OpenAI

embeddings = HuggingFaceEmbeddings(
    model_name="Qodo/Qodo-Embed-1-1.5B",
    model_kwargs={"trust_remote_code": True}
)

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY    
)

def embed_user_query(query):
    query_vector = embeddings.embed_query(query)
    return query_vector

def search_by_vector(query, collection, limit):
    results = client.search(
        collection_name=collection,
        query_vector=query,
        limit=limit,
        with_payload=True
    )
    return results

def user_query_search(query, collection, limit):
    vector = embed_user_query(query)
    results = search_by_vector(vector, collection, limit)
    return results

# res = user_query_search(user_query, COLLECTION_NAME)

# print(res[0].payload["text"])


def answer_with_context(query, qdrant_collection, limit, api_key=openrouter_api):

    res = user_query_search(query, qdrant_collection, limit)
    context = ''
    for i in res:
        print(i.score)
        context += "\n"
        context += f"{i.payload['text']} " 
    print(context)

    prompt = (
        f"""
            Ты — интеллектуальный ассистент, задача которого - отвечать на вопросы для абитуриентов магистратуры AI Talent Hub.
            Отвечай на вопрос пользователя вежливо, максимально точно, используя факты из предоставленного тебе контекста из базы знаний.
            Не упоминай существование "контекста" в диалоге с пользователем. При генерации ответа старайся уложиться в 5-6 предложений или меньше.
            Если ответ на вопрос в базе знаний не найден, или если вопрос не относится к теме:
            - скажи, что не можешь дать ответ на этот вопрос.
            - предложи пользователю обратиться по контактам.
            
            Контакты:
            - Почта: aitalents@itmo.ru
            - VK: https://vk.com/aitalenthub
            - Telegram: https://t.me/abit_AI_talent_hub

            Вопрос пользователя: {query}

            Контекст (виден только тебе):
            {context}

            Ответ:
        """
    )

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    completion = client.chat.completions.create(
        model="qwen/qwen3-235b-a22b-2507:free",
        # model="mistralai/mistral-small-3.2-24b-instruct:free",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )

    answer = completion.choices[0].message.content
    return answer

if __name__ == "__main__":
    user_query = "Сколько бюджетых мест"
    ans = answer_with_context(user_query, COLLECTION_NAME, 5)
    print(ans)

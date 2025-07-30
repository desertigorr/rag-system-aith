# RAG for AI Talent Hub

Это учебный проект, все права принадлежат Хабу, вся информация взята из открытых источников)

## Стек

- *Beautiful Soup*, *Selenium* для парсинга
- *langchain_text_splitters*, *langchain_huggingface* embeddings, *qdrant* для создания и хранения эмбеддингов
- *openrouter.ai*, *OpenAI* для использования LLM
- *FastAPI* для создания API-сервиса
- *Docker* для контейнеризации

## Модели

- Embeddings: Qodo/Qodo-Embed-1-1.5B
- Query Rephrasal: mistralai/mistral-small-3.2-24b-instruct:free
- Answer Generation: qwen/qwen3-235b-a22b-2507:free

## Пайплайн
1. Парсинг открытых источников (сайты Talent Hub'a) (rag_data.py)
2. Очистка html-кода сайтов от тегов и ненужных конструкций (qdrant_bd.py)
3. Чанкование текста, создание эмбеддингов и загрузка в qdrant (qdrant_bd.py)
4. Дополнение пользовательского запроса для лучшего семантического поиска (rephrasal_agent.py)
5. Сематнический поиск, генерация ответа (query.py)

## Как запустить
### Локально
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```
или
```docker
docker compose up --build
```
только нужно юзать свои ключи для qdrant и openrouter/openai

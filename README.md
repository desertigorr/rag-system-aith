# RAG for AI Talent Hub

Это учебный проект, все права принадлежат Хабу, вся информация взята из открытых источников)

## Стек

- ``Beautiful Soup``, ``Selenium`` для парсинга
- ``langchain_text_splitters``, ``langchain_huggingface embeddings``, ``qdrant`` для создания и хранения эмбеддингов
- ``openrouter.ai``, ``OpenAI`` для использования LLM
- ``FastAPI`` для создания API-сервиса
- ``Docker`` для контейнеризации

## Модели

- Embeddings: ``Qodo/Qodo-Embed-1-1.5B``
- Query Rephrasal: ``mistralai/mistral-small-3.2-24b-instruct:free``
- Answer Generation: ``qwen/qwen3-235b-a22b-2507:free``

## Пайплайн
1. Парсинг открытых источников (сайты Talent Hub'a) (rag_data.py)
2. Очистка html-кода сайтов от тегов и ненужных конструкций (qdrant_bd.py)
3. Чанкование текста, создание эмбеддингов и загрузка в qdrant (qdrant_bd.py)
4. Дополнение пользовательского запроса для лучшего семантического поиска (rephrasal_agent.py)
5. Сематнический поиск, генерация ответа (query.py)

## Структура проекта
<pre>
test-ai-agent/
├── app/
│   ├── __init__.py               # для докера
│   ├── api.py                    # API endpoints из .env
│   ├── main.py                   # Инициализация API-сервиса
│   ├── qdrant_bd.py              # Парсинг, создание и загрузка эмбеддингов в Qdrant
│   ├── qdrant_shenanigans.py     # Вспомогательные функции для работы с Qdrant
│   ├── query.py                  # Поиск и генерация ответа
│   ├── rag_data.py               # Функции для парсинга
│   ├── rephrase_agent.py         # Переформулировка запросов пользователя (для улучшения семантического поиска по бд)
├── .env                          # Секретики)
├── docker-compose.yml           # docker compose конфигурация
├── Dockerfile                   # Файл сборки для докера
├── requirements.txt             # Зависимости
</pre>

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

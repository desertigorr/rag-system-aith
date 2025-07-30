from app.api import openrouter_api
from openai import OpenAI


def rephrase_user_query(query, api_key=openrouter_api):

    prompt = (
        f"""
            Перефразируй вопрос пользователя 3 разными способами, сохраняя смысл, 
            чтобы улучшить семантический поиск по базе знаний о магистратуре AI Talent Hub.
            Верни 3 варианта в виде списка, без пояснений.

            Вопрос: "{query}"
        """

    )

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    completion = client.chat.completions.create(
        model="mistralai/mistral-small-3.2-24b-instruct:free",
        messages=[
            {"role": "system", "content": prompt}
        ],
        max_tokens=100
    )

    answer = completion.choices[0].message.content
    print(answer)
    return f"{query} \n {answer}"

# if __name__ == "__main__":
#     user_query = ""
#     print(rephrase_user_query(user_query))

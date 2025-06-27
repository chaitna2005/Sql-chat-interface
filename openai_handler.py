from openai import OpenAI
import os
from dotenv import load_dotenv
from sql_handler import get_schema_description

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def english_to_sql(user_input):
    schema_prompt = get_schema_description()
    full_prompt = f"{schema_prompt}\n{user_input}"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": full_prompt}]
    )

    # Extract tokens info
    usage = response.usage
    token_info = (
        f"Prompt Tokens: {usage.prompt_tokens}, "
        f"Completion Tokens: {usage.completion_tokens}, "
        f"Total Tokens: {usage.total_tokens}"
    )

    # The generated SQL query
    sql_query = response.choices[0].message.content.strip()

    return sql_query, token_info


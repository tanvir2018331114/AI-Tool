from config import settings
import openai
import os

openai.api_key = settings.openai_api_key

def get_embedding(text: str) -> list[float]:
    response = openai.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

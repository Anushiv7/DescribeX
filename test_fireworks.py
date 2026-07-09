import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(".env")
api_key = os.getenv("DESCRIBEX_FIREWORKS_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.fireworks.ai/inference/v1"
)

try:
    models = client.models.list().data
    print("--- RAW MODEL METADATA ---")
    for model in models:
        print(f"Model ID: {model.id}")
        print("Raw metadata snippet:")
        print(json.dumps(model.model_dump(), indent=2))
        print("-" * 40)
except Exception as e:
    print("Failed to fetch model metadata:", e)



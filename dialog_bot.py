#Здесь мы подключаем модель ИИ, которая находится на ХаггингФейс репозитории. Пользуемся простым запросом ответа от модели.

import requests

API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
headers = {"Authorization": "Bearer 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"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()
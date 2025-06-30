import json
from typing import List, Dict

import aiohttp

from utils.regex import clean_response


class OllamaService:
    def __init__(self, ollama_url: str, model_name: str):
        self.ollama_url = ollama_url
        self.model_name = model_name

    async def query_ollama(self, messages: List[Dict[str, str]], current_msg_id: int) -> str:
        # Преобразуем историю сообщений в формат OLLAMA
        ollama_messages = []
        for msg in messages:
            # OLLAMA использует поле 'content' и 'role' (user/assistant/system)
            ollama_messages.append({
                'role': msg['role'],
                'content': msg['content']
            })
        payload = {
            "model": self.model_name,
            "messages": ollama_messages,
            "stream": False  # Мы хотим сразу получить полный ответ
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.ollama_url, json=payload) as resp:
                    if resp.status == 200:
                        response_data = await resp.json()
                        payload = {
                            "response_text": str(clean_response(response_data['message']['content'])),
                            "status": "pending"
                        }
                        await session.patch(f"http://api:5466/update_message/{current_msg_id}",
                                            json=payload)
                        return response_data['message']['content']
                    else:
                        error = await resp.text()
                        print(error)
                        return "Извините, произошла ошибка при обработке запроса."
        except Exception as e:
            return "Не удалось подключиться к модели. Попробуйте позже."


async def get_prompt(history, new_question):
    return [
        # Системный промпт с инструкцией
        {
            "role": "system",
            "content": (
                    "Ты — ассистент. Анализируй всю историю диалога, но отвечай "
                    "ТОЛЬКО на последний вопрос пользователя. Предыдущие сообщения — "
                    "только для контекста.\n\n"
                    "Текущий диалог:\n" +
                    "\n".join(f"{msg['role']}: {msg['content']}" for msg in history)
            )
        },
        # Последний вопрос
        {"role": "user", "content": new_question}
    ]
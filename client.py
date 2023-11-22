from typing import Any

import openai

from config import settings


class OpenAIClient:
    def __init__(self) -> None:
        self.openai = openai

    def get_chat_completion(self, prompt: str, params: dict[str, Any] | None = None) -> str:
        messages = [
            {"role": "system", "content": settings.system_message},
            {"role": "user", "content": prompt},
        ]

        response = self.openai.ChatCompletion.create(
            engine=settings.openai_engine,
            messages=messages,
            max_tokens=params.get("max_tokens", settings.max_tokens),
            temperature=params.get("temperature", settings.temperature),
            frequency_penalty=params.get("frequency_penalty", settings.frequency_penalty),
            presence_penalty=params.get("presence_penalty", settings.presence_penalty),
            top_p=params.get("top_p", settings.top_p),
            stop=params.get("stop", settings.stop),
        )

        return response.choices[0].text

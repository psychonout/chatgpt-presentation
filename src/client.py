from typing import Any

from openai import OpenAI

from config import settings


class OpenAIClient:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.openai_api_key)

    def get_chat_completion(self, prompt: str, params: dict[str, Any] | None = None) -> str:
        messages = [
            {"role": "system", "content": params.get("system_message", settings.system_message)},
            {"role": "user", "content": prompt},
        ]

        response = self.client.chat.completions.create(
            messages=messages,
            engine=params.get("text_engine", settings.text_engine),
            temperature=params.get("temperature", settings.temperature),
        )

        return response.choices[0].text

    def get_generated_image(self, prompt: str, params: dict[str, Any] | None = None) -> str:
        response = self.client.images.generate(
            prompt=prompt,
            model=params.get("image_model", settings.image_model),
            size=params.get("image_size", settings.image_size),
            quality=params.get("image_quality", settings.image_quality),
        )

        return response.data[0].url

    def get_response(self, prompt: str, params: dict[str, Any] | None = None) -> str:
        if params.get("mode") and params["mode"] == "image":
            return self.get_generated_image(prompt, params)

        return self.get_chat_completion(prompt, params)

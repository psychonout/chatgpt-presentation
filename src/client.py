from typing import Any

from openai import OpenAI
from PIL import Image

from config import settings
from utils import download_file


class OpenAIClient:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.openai_api_key)

    def get_chat_completion(self, prompt: str, params: dict[str, Any]) -> str:
        messages = [
            {"role": "system", "content": params.get("system_message", settings.system_message)},
            {"role": "user", "content": prompt},
        ]

        response = self.client.chat.completions.create(
            messages=messages,
            model=params.get("text_engine", settings.text_engine),
            temperature=params.get("temperature", settings.temperature),
        )

        return response.choices[0]["text"]

    def get_generated_image(self, prompt: str, params: dict[str, Any]) -> str | None:
        response = self.client.images.generate(
            prompt=prompt,
            model=params.get("image_model", settings.image_model),
            size=params.get("image_size", settings.image_size),
            quality=params.get("image_quality", settings.image_quality),
        )

        return response.data[0]["url"]

    def get_response(self, prompt: str, params: dict[str, Any]) -> str | Image.Image:
        if params.get("mode") and params["mode"] == "image":
            image_url = self.get_generated_image(prompt, params)
            if not image_url:
                return "Sorry, I couldn't generate an image for you. Please try again."
            filename = download_file(image_url)
            return Image.open(filename)

        return self.get_chat_completion(prompt, params)

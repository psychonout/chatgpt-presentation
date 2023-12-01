import os

from PIL import Image
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str

    system_message: str = "You are a helpful assistant."
    temperature: float = 0.7
    text_engine: str = "gpt-3.5-turbo"

    image_model: str = "image-alpha-001"
    image_size: str = "1024x1024"
    image_quality: str = "standard"

    avatar: Image.Image = Image.open(os.path.join(os.getcwd(), "avatar.png"))

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


def get_settings():
    return Settings()  # type: ignore


settings = get_settings()

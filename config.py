from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str

    openai_engine: str = "gpt-3.5-turbo"
    system_message = "You are a helpful assistant."
    max_tokens = 1024
    temperature = 0.7
    frequency_penalty = 0
    presence_penalty = 0
    top_p = 1
    stop = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


def get_settings():
    return Settings()  # type: ignore


settings = get_settings()

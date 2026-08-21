from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Chatbot — OPCIÓN ACTIVA
    GROQ_API_KEY: str = ""

    # Chatbot — OPCIÓN FUTURA (OpenAI con billing)
    # OPENAI_API_KEY: str = ""

    class Config:
        env_file = ".env"

settings = Settings()

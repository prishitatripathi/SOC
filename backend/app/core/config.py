from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./backend/data/probe_soc.db"
    ollama_url: str = "http://localhost:11434"

settings = Settings()

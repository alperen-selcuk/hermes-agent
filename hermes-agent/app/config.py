from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    llm_provider: str = "ollama"          # "ollama" | "openai"

    # Ollama
    ollama_base_url: str = "http://ollama:11434"
    ollama_model: str = "hermes3:8b"

    # OpenAI (llm_provider=openai ise)
    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-4o"

    # Agent
    agent_system_prompt_file: str = "/app/prompts/system.txt"
    max_iterations: int = 10
    log_level: str = "INFO"

    @property
    def log_level_resolved(self) -> str:
        return self.log_level if self.log_level.strip() else "INFO"
    secret_key: str = "changeme-use-strong-secret-in-prod"

    class Config:
        env_file = ".env"


settings = Settings()

"""Application configuration loaded from environment variables."""

from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    # HuggingFace
    hf_api_token: str = ""
    hf_model: str = "meta-llama/Meta-Llama-3-8B-Instruct"
    hf_fallback_model: str = "Qwen/Qwen2.5-72B-Instruct"

    # Database
    db_path: str = str(Path(__file__).resolve().parent.parent / "ncert_tutor.db")

    # Teacher auth
    teacher_default_password: str = "teach123"
    secret_key: str = "change_this_in_production"

    # Server
    backend_host: str = "127.0.0.1"
    backend_port: int = 8000
    frontend_port: int = 8501

    # Paths
    project_root: str = str(Path(__file__).resolve().parent.parent)

    model_config = {"env_file": str(Path(__file__).resolve().parent.parent / ".env")}


settings = Settings()

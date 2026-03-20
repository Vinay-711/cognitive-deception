from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "COGNITIVE DECEPTION"
    app_env: str = "development"
    api_prefix: str = "/api/v1"

    database_url: str = "sqlite:///./cognitive_deception.db"
    redis_url: str = "redis://localhost:6379/0"
    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_topic: str = "honeypot-events"
    elasticsearch_url: str = "http://localhost:9200"
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "changeme"

    use_llm: bool = False
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    enable_kafka: bool = False
    enable_elastic: bool = False
    enable_neo4j: bool = False
    enable_redis: bool = False

    demo_auto_seed: bool = True

    resilience_interval_seconds: int = 60
    session_idle_timeout_seconds: int = 900

    # Safety: honeypot never executes attacker commands; only simulates output.
    max_command_length: int = 512
    max_session_events: int = 200

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()

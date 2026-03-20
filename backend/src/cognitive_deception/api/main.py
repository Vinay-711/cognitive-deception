import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from cognitive_deception.api.routes import router
from cognitive_deception.core.config import get_settings
from cognitive_deception.core.logging import configure_logging
from cognitive_deception.models.db import Base, engine
from cognitive_deception.models.entities import AttackEvent, AttackSession, ThreatReport  # noqa: F401
from cognitive_deception.services.resilience import run_resilience_loop, shutdown_resilience_loop

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    configure_logging()
    Base.metadata.create_all(bind=engine)
    resilience_task = await run_resilience_loop()
    yield
    await shutdown_resilience_loop(resilience_task)


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix=settings.api_prefix)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "platform": settings.app_name,
        "status": "online",
        "mission": "autonomous cyber deception and threat intelligence",
    }

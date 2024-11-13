from src.config import settings
from src.data_access.db_connector import db_session
from src.presentation.routers import router

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from typing import AsyncGenerator, Any
import asyncio
import logging


logger = logging.getLogger(__name__)


def setup_logging() -> None:
    logging.getLogger("pika").setLevel(logging.WARNING)
    logging.basicConfig(
        level=logging.INFO,
        format=(
            '[%(asctime)s] %(levelname)s - %(filename)s'
            '[%(lineno)d]: %(message)s'
        )
    )

setup_logging()
app = FastAPI()
app.include_router(router)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        "main:app",
        host='127.0.0.1',
        port=8000
    )

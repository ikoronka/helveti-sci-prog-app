import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db_handler import HouseRentDatabase
from llm_service import LLMService
from routers import data, filters, insight

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = HouseRentDatabase(db_name=os.environ.get("DB_PATH", "house_rent.db"))
    logger.info("Loading dataset...")
    app.state.df = db.get_data()
    logger.info("Dataset loaded: %d rows", len(app.state.df))
    app.state.llm = LLMService()
    yield


app = FastAPI(title="Helveti House Rent API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(filters.router, prefix="/api")
app.include_router(data.router, prefix="/api")
app.include_router(insight.router, prefix="/api")

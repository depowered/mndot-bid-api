import os
from pathlib import Path

from fastapi import FastAPI

from mndot_bid_api import routers
from mndot_bid_api.db import database
from mndot_bid_api.db.load_sample_records import load_sample_records

MODE = os.getenv("MODE")
DEVELOPMENT_DATABASE_URL = os.getenv("DEVELOPMENT_DATABASE_URL")
PRODUCTION_DATABASE_URL = os.getenv("PRODUCTION_DATABASE_URL")


app = FastAPI(swagger_ui_parameters={"defaultModelsExpandDepth": -1})


@app.on_event("startup")
def startup_event():
    dev_db_exists = Path("./data/dev-api.db").exists()

    if not MODE or MODE not in ["development", "production"]:
        raise ValueError(
            "Environment variable MODE is invalid. Valid values: development, production"
        )

    if MODE == "development":
        database.init_sqlite_db(url=DEVELOPMENT_DATABASE_URL)
        if not dev_db_exists:
            load_sample_records()

    database.init_sqlite_db(url=PRODUCTION_DATABASE_URL)


@app.get("/", include_in_schema=False)
def read_root():
    return {"server status": "Running"}


app.include_router(routers.contract_router)
app.include_router(routers.bidder_router)
app.include_router(routers.bid_router)
app.include_router(routers.invalid_bid_router)
app.include_router(routers.item_router)
app.include_router(routers.etl_router)

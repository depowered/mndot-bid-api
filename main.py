import os

from fastapi import FastAPI

from mndot_bid_api import routers
from mndot_bid_api.db import database

DB_FILE = str(os.getenv("DB_FILE"))
DB_URL = f"sqlite:///data/{DB_FILE}"


app = FastAPI(swagger_ui_parameters={"defaultModelsExpandDepth": -1})


@app.on_event("startup")
def startup_event():
    database.init_sqlite_db(url=DB_URL)


@app.get("/", include_in_schema=False)
def read_root():
    return {"server status": "Running"}


app.include_router(routers.contract_router)
app.include_router(routers.bidder_router)
app.include_router(routers.bid_router)
app.include_router(routers.invalid_bid_router)
app.include_router(routers.item_router)
app.include_router(routers.etl_router)

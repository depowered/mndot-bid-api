from sqlite3 import SQLITE_ALTER_TABLE

from fastapi import FastAPI

from mndot_bid_api.db import database
from mndot_bid_api.routers import bidders, bids, contracts

SQLALCHEMY_DATABASE_URL = "sqlite:///data/api.db"
# SQLALCHEMY_DATABASE_URL = "sqlite:///data/sample.db"


app = FastAPI()


@app.on_event("startup")
def startup_event():
    database.init_sqlite_db(url=SQLALCHEMY_DATABASE_URL)


@app.get("/", include_in_schema=False)
def read_root():
    return {"server status": "Running"}


app.include_router(contracts.router)
app.include_router(bidders.router)
app.include_router(bids.router)

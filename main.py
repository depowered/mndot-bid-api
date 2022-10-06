from pathlib import Path

from fastapi import FastAPI

from mndot_bid_api.db import database, sample_data
from mndot_bid_api.routers import bidders, bids, contracts, items

SQLALCHEMY_DATABASE_URL = "sqlite:///data/api.db"


app = FastAPI()


@app.on_event("startup")
def startup_event():
    if not Path("./data/api.db").exists():
        database.init_sqlite_db(url=SQLALCHEMY_DATABASE_URL)
        sample_data.load_sample_data()
    else:
        database.init_sqlite_db(url=SQLALCHEMY_DATABASE_URL)


@app.get("/", include_in_schema=False)
def read_root():
    return {"server status": "Running"}


app.include_router(contracts.router)
app.include_router(bidders.router)
app.include_router(bids.router)
app.include_router(items.router)

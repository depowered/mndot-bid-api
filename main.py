from fastapi import FastAPI

from mndot_bid_api.db.create_db import create_db
from mndot_bid_api.db.engine import init_db
from mndot_bid_api.routers import contracts, bidders, bids

app = FastAPI()

DB_FILE = "sqlite:///sample.db"
# create_db(DB_FILE)


@app.on_event("startup")
def startup_event():
    init_db(DB_FILE)


@app.get("/")
def read_root():
    return {"server status": "Running"}


app.include_router(contracts.router)
app.include_router(bidders.router)
app.include_router(bids.router)

import json
from pathlib import Path

from fastapi import FastAPI

from mndot_bid_api.db import database, sample_data
from mndot_bid_api.routers import bidders, bids, contracts, items

DEVELOPMENT_DATABASE_URL = "sqlite:///data/dev-api.db"
PRODUCTION_DATABASE_URL = "sqlite:///data/prod-api.db"

DEVELOPMENT_MODE = True


app = FastAPI()


@app.on_event("startup")
def startup_event():
    dev_db_exists = Path("./data/dev-api.db").exists()

    if DEVELOPMENT_MODE:
        database.init_sqlite_db(url=DEVELOPMENT_DATABASE_URL)
        if not dev_db_exists:
            sample_data.load_sample_data()
    else:
        database.init_sqlite_db(url=PRODUCTION_DATABASE_URL)


@app.get("/", include_in_schema=False)
def read_root():
    return {"server status": "Running"}


app.include_router(contracts.router)
app.include_router(bidders.router)
app.include_router(bids.router)
app.include_router(items.router)

with open("./openapi.json", "w") as f:
    f.write(json.dumps(app.openapi()))

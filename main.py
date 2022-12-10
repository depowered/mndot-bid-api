import os

from fastapi import FastAPI

from mndot_bid_api import routers
from mndot_bid_api.db import database

DB_FILE = str(os.getenv("DB_FILE"))
DB_URL = f"sqlite:///data/{DB_FILE}"

description = """
### Purpose
Backend service for extracting bid information from MnDOT's published 
[abstracts](https://www.dot.state.mn.us/bidlet/abstract.html) and providing 
create, read, update and delete operations to manage the extracted data.

### Route Categories
**contract**: General project data for a particular abstract including letting date, 
SP Number, MnDOT District, etc.

**bidder**: ID and name of prime contractors that have submitted a bid proposal that 
was ranked as the three lowest bid proposals.

**bid**: Invididual bid records including engineers estimates, winning bidder, and losing bidders.

**invalid_bid**: Bid records for items that do not conform to the MnDOT Standard Specifications.

**item**: Items defined in the MnDOT Standard Specifications.

**etl**: Extract, Transform, Load operations that modify the database records based on CSV uploads 
for MnDOT Standard Specification item lists or published abstracts.

### Contract
Created and maintained by: [devin@powergeospatial.xyz](mailto:devin@powergeospatial.xyz)

"""


app = FastAPI(
    title="MnDOT Bid API",
    description=description,
    version="0.2.0",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)


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

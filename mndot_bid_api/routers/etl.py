import fastapi

from mndot_bid_api import db, schema
from mndot_bid_api.etl.pipeline.item_list import item_list_etl_pipeline
from mndot_bid_api.operations.crud_interface import CRUDInterface

etl_router = fastapi.APIRouter(prefix="/etl", tags=["etl"])


@etl_router.post(
    "/", status_code=fastapi.status.HTTP_200_OK, response_model=schema.ItemListETL
)
def api_item_list_etl(
    csv: fastapi.UploadFile = fastapi.File(...),
    item_interface: CRUDInterface = fastapi.Depends(db.get_item_interface),
):

    return item_list_etl_pipeline(csv, item_interface)

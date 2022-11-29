import fastapi

from mndot_bid_api import auth, db, schema
from mndot_bid_api.etl.pipeline.abstract import abstract_etl_pipeline
from mndot_bid_api.etl.pipeline.item_list import item_list_etl_pipeline
from mndot_bid_api.operations.crud_interface import CRUDInterface

etl_router = fastapi.APIRouter(prefix="/etl", tags=["etl"])


@etl_router.post(
    "/item_list/",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=schema.ItemListETL,
)
def api_item_list_etl(
    csv: fastapi.UploadFile = fastapi.File(...),
    item_interface: CRUDInterface = fastapi.Depends(db.get_item_interface),
    api_key: auth.APIKeyHeader = fastapi.Depends(auth.authorize_api_key),
):

    return item_list_etl_pipeline(csv, item_interface)


@etl_router.post(
    "/abstract/",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=schema.AbstractETL,
)
def api_abstract_etl(
    csv: fastapi.UploadFile = fastapi.File(...),
    contract_interface: CRUDInterface = fastapi.Depends(db.get_contract_interface),
    bid_interface: CRUDInterface = fastapi.Depends(db.get_bid_interface),
    invalid_bid_interface: CRUDInterface = fastapi.Depends(
        db.get_invalid_bid_interface
    ),
    bidder_interface: CRUDInterface = fastapi.Depends(db.get_bidder_interface),
    item_interface: CRUDInterface = fastapi.Depends(db.get_item_interface),
    api_key: auth.APIKeyHeader = fastapi.Depends(auth.authorize_api_key),
):

    return abstract_etl_pipeline(
        csv,
        contract_interface,
        bid_interface,
        invalid_bid_interface,
        bidder_interface,
        item_interface,
    )

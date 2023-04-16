from mndot_bid_api import exceptions, schema
from mndot_bid_api.operations.crud_interface import CRUDInterface

def read_abstract_etl_status(etl_id: int, abstract_etl_status_interface: CRUDInterface) -> schema.AbstractETLStatusResult:
    try:
        record = abstract_etl_status_interface.read_by_id(etl_id)
    
    except exceptions.RecordNotFoundError as exc:
        exceptions.raise_http_404(model_name="AbstractETLStatus", id=etl_id, exc=exc)

    result = schema.AbstractETLStatusResult(**record)

    return result
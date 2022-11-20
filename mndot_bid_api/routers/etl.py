import fastapi


etl_router = fastapi.APIRouter(prefix="/etl", tags=["etl"])


@etl_router.post(
    "/",
    status_code=fastapi.status.HTTP_200_OK,
)
def api_item_list_etl(csv: fastapi.UploadFile = fastapi.File(...)):
    # Extract: Read the file into a dataframe matching a pandera schema
    # Transform: Morph the input into the output pandera schema
    # Load: Iteratively post records to the create item route

    return {"file": csv.filename}
